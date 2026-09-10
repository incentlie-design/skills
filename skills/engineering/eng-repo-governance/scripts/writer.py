#!/usr/bin/env python3
"""Run a foreground writer under a POSIX lock in one Git worktree (stdlib only)."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def run(branch, base, owner, command):
    import fcntl

    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    if Path.cwd().resolve() != root:
        raise ValueError("run from the intended worktree root")
    actual = git("symbolic-ref", "--quiet", "--short", "HEAD")
    if actual != branch or actual in {"main", "master"}:
        raise ValueError("branch mismatch or protected stable branch")
    if len(base) != 40 or any(c not in "0123456789abcdef" for c in base):
        raise ValueError("base must be an exact full commit SHA")
    if git("rev-parse", f"{base}^{{commit}}") != base:
        raise ValueError("base is not a commit")
    subprocess.run(["git", "merge-base", "--is-ancestor", base, "HEAD"], check=True)
    if not command or not owner.strip():
        raise ValueError("a foreground command and writer identity are required")
    # --git-path resolves to this worktree's administrative directory, not the
    # common directory: independent branches do not contend for a global lease.
    lock_path = Path(git("rev-parse", "--git-path", "governance-writer.lock"))
    with lock_path.open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError("another foreground writer owns this worktree") from exc
        # Never unlink a lock inode: a competing process may already have it open.
        lock.seek(0)
        lock.truncate()
        json.dump({"owner": owner, "pid": os.getpid(), "branch": branch,
                   "base": base, "head": git("rev-parse", "HEAD")}, lock)
        lock.flush()
        # The child inherits the lock so an interrupted launcher cannot release
        # ownership while its foreground child is still writing.
        return subprocess.run(command, pass_fds=(lock.fileno(),)).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        return run(args.branch, args.base, args.owner, command)
    except (ValueError, OSError, subprocess.CalledProcessError, ImportError) as exc:
        print(f"writer: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
