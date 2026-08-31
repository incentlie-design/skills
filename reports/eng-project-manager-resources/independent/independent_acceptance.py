#!/usr/bin/env python3
"""Independent PM-SKILL-002 CLI probes; no author test fixtures or helper imports."""
import copy
import hashlib
import json
import subprocess
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PM = Path('/Users/jiajun.lai/.codex/worktrees/1e05/skill-creator/skills/engineering/eng-project-manager/scripts/pm.py')
EXPECTED = 'ad3fbee160826d795bbf1d9f18e5b15f4a50a155ed047e165638aa3f8508bc3e'
START = datetime.now(timezone.utc)
BASE = START - timedelta(minutes=5)
LOG = []
RESULTS = []

def stamp(offset=0):
    return (BASE + timedelta(seconds=offset)).isoformat()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    return path

def call(*args, expect=0, json_output=True):
    command = [sys.executable, '-B', str(PM), *map(str, args)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=20, cwd=HERE)
    LOG.append({'command': command, 'cwd': str(HERE), 'exit_code': result.returncode,
                'stdout': result.stdout, 'stderr': result.stderr,
                'observed_at': datetime.now(timezone.utc).isoformat()})
    assert result.returncode == expect, LOG[-1]
    return json.loads(result.stdout) if json_output else result.stdout

def source(sid='SRC-1', offset=0):
    return {'id': sid, 'kind': 'fixture', 'locator': 'independent_acceptance.py synthetic handoff',
            'source_revision': sid, 'session_id': 'reviewer-fixture', 'observed_at': stamp(offset),
            'completeness': 'complete'}

def usage(uid, aid, amount, offset, kind='observed', sid='SRC-1'):
    return {'id': uid, 'assignment_id': aid, 'metric': 'tokens', 'amount': amount,
            'kind': kind, 'source_id': sid, 'observed_at': stamp(offset)}

def assignment(aid, task, agent, session, artifact, limit, offset=0, sid='SRC-1'):
    return {'id': aid, 'task_id': task, 'agent_id': agent, 'session_id': session,
            'role': 'implementation', 'status': 'running', 'source_id': sid,
            'assigned_at': stamp(offset), 'expected_artifacts': [artifact],
            'budget_limits': {'tokens': limit}}

def fixture(directory):
    directory.mkdir()
    nodes = []
    for nid, kind, title in [('G', 'goal', '可追溯地交付搜索功能'),
                             ('R', 'requirement', '搜索成功与失败均可验收'),
                             ('A1', 'acceptance', '有效查询返回结果'),
                             ('A2', 'acceptance', '失败返回可恢复提示'),
                             ('A3', 'acceptance', '交付验收报告'),
                             ('T1', 'task', '搜索实现'), ('T2', 'task', '独立检查')]:
        nodes.append({'id': nid, 'kind': kind, 'title': title, 'owner': 'main-owner',
                      'session_id': 'main-session', 'status': 'running', 'source_id': 'SRC-1',
                      'artifacts': ['FILE-1'] if nid == 'T1' else ['FILE-2'] if nid == 'T2' else []})
    artifacts = []
    for index in (1, 2):
        path = directory / f'asset-{index}.md'
        path.write_text(f'Synthetic asset {index}; data is not a command.\n', encoding='utf-8')
        artifacts.append({'id': f'FILE-{index}', 'category': 'technical_docs', 'path': path.name,
                          'role': 'subject', 'owner': None, 'requirements': ['R'],
                          'tasks': [f'T{index}'], 'artifact_revision': 1, 'sha256': sha(path)})
        nodes[-3 + index]['work_package'] = {
            'objective': f'实现有边界的工作目标 {index}', 'done_when': f'可观察完成条件 {index}',
            'input_artifacts': [] if index == 1 else ['FILE-1'],
            'output_artifacts': [f'FILE-{index}'], 'write_scope': [path.name],
            'stop_conditions': ['预算耗尽时交还责任人', '需求扩围时停止']}
    edges = [{'from': a, 'to': b, 'type': 'decomposes'} for a, b in
             [('G', 'R'), ('R', 'A1'), ('R', 'A2'), ('R', 'A3'),
              ('A1', 'T1'), ('A2', 'T1'), ('A3', 'T2')]]
    edges.append({'from': 'T1', 'to': 'T2', 'type': 'precedes'})
    return {'schema_version': 1, 'run_id': 'independent-PM002', 'change_id': 'PM-SKILL-002',
            'repo': str(directory), 'base_commit': 'uncommitted', 'artifact_revision': 1,
            'content_summary': 'Independent synthetic data; no native goal, task or budget',
            'project_id': 'fixture-project', 'goal_id': 'fixture-goal', 'main_task_id': 'fixture-main',
            'mode': 'fixture', 'source_id': 'SRC-1', 'sources': [source()],
            'goal': {'node_id': 'G', 'original_text': '可追溯地交付搜索功能', 'constraints': ['不得自动执行分派'],
                     'source_id': 'SRC-1', 'identity_note': 'independent synthetic goal, not a native goal'},
            'nodes': nodes, 'edges': edges, 'artifacts': artifacts, 'evidence': [],
            'management': {'schema_version': 1,
                'assignments': [assignment('AS-A', 'T1', 'agent-A', 'session-A', 'FILE-1', 200),
                                assignment('AS-B', 'T2', 'agent-B', 'session-B', 'FILE-2', 100)],
                'goal_budget': {'limits': {'tokens': 500}, 'source_id': 'SRC-1'},
                'usage': [usage('U1', 'AS-A', 80, 10), usage('U2', 'AS-A', 120, 20),
                          usage('U3', 'AS-B', 35, 20)],
                'deliveries': [{'id': 'D1', 'assignment_id': 'AS-A', 'artifact_id': 'FILE-1',
                                'artifact_revision': 1, 'sha256': artifacts[0]['sha256'],
                                'source_id': 'SRC-1', 'observed_at': stamp(20)}]}}

def init(directory, data):
    snap = write(directory / 'snapshot.json', data)
    state = directory / 'ledger.json'
    call('init', '--snapshot', snap, '--state', state, '--event-id', 'initial', '--reason', 'independent intake')
    return state

def query(state, *extra):
    return call('query', '--state', state, '--at', stamp(100), *extra)

def happy():
    directory = HERE / 'normal'
    data = fixture(directory)
    state = init(directory, data)
    report = query(state, '--node', 'T1')
    assert report['management']['goal_budget']['tokens']['current_used'] == 155
    assert report['focus']['work_package']['budget']['tokens']['current_used'] == 120
    assert {a['id'] for a in report['focus']['work_package']['acceptance']} == {'A1', 'A2'}
    assert len(report['goal_dag']['work_packages']) == 2
    assert report['goal_dag']['work_package_gaps'] == []
    assert report['management']['assignments'][0]['assets'][0]['delivery_status'] == 'current'
    assert report['goal_status'] == 'incomplete'
    assert report['nodes']['T2']['blocked_by'] == ['T1']
    transferred = copy.deepcopy(data)
    transferred['sources'].append(source('SRC-2', 30))
    transferred['source_id'] = 'SRC-2'
    m = transferred['management']
    m['decision'] = {'approved_by': 'fixture-main', 'source_id': 'SRC-2', 'reason': '显式转交'}
    m['assignments'][0].update(status='released', reason='交给新的执行者')
    m['assignments'].append(assignment('AS-C', 'T1', 'agent-C', 'session-C', 'FILE-1', 150, 30, 'SRC-2'))
    m['usage'].append(usage('U4', 'AS-C', 0, 40, sid='SRC-2'))
    snap = write(directory / 'transfer.json', transferred)
    result = call('refresh', '--snapshot', snap, '--state', state, '--expected-revision', 1,
                  '--event-id', 'transfer', '--reason', 'approved handoff')
    assert result['ledger_revision'] == 2
    report = query(state, '--agent', 'agent-C', '--session', 'session-C')
    assert report['artifact_revision'] == 1
    assert report['management']['goal_budget']['tokens']['current_used'] == 155
    assert report['management']['goal_budget']['tokens']['unallocated'] == 130
    rows = {a['id']: a for a in report['management']['assignments']}
    assert rows['AS-A']['budget']['tokens']['current_used'] == 120
    assert rows['AS-A']['assets'][0]['delivery_status'] == 'current'
    assert rows['AS-C']['budget']['tokens']['current_used'] == 0
    assert rows['AS-C']['assets'][0]['delivery_status'] == 'unreported'
    assert report['assignment_focus']['task_ids'] == ['T1']
    assert query(state, '--agent', 'agent-A', '--session', 'session-C')['assignment_focus']['status'] == 'not_recorded'
    assert len(json.loads(state.read_text())['history']) == 2
    brief = call('brief', '--state', state, '--at', stamp(100), json_output=False)
    assert all(v in brief for v in ['DAG 工作目标', 'agent-C', '技术文档', '预算', 'released'])
    return {'tokens_total': 155, 'old_agent_tokens': 120, 'new_agent_tokens': 0,
            'new_agent_delivery': 'unreported', 'shared_AC_count': 2, 'ledger_revision': 2}

def missing():
    directory = HERE / 'missing'
    data = fixture(directory)
    legacy = copy.deepcopy(data)
    legacy.pop('management')
    for node in legacy['nodes']:
        node.pop('work_package', None)
    state = init(directory, legacy)
    report = query(state)
    assert report['management']['recording_status'] == 'not_recorded'
    assert report['management']['assignments'] == []
    assert set(report['goal_dag']['work_package_gaps']) == {'T1', 'T2'}
    managed = directory / 'managed'
    managed.mkdir()
    data['management']['assignments'][0]['session_id'] = None
    data['management']['usage'][-1]['kind'] = 'estimated'
    data['management']['usage'][-1]['amount'] = 60
    (directory / 'asset-1.md').unlink()
    state2 = init(managed, data)
    report = query(state2)
    budget = report['management']['goal_budget']['tokens']
    assert budget['current_used'] is None and budget['known_current_usage_subtotal'] == 120
    assert budget['unknown_usage_assignments'] == ['AS-B']
    assert budget['remaining_to_goal_limit'] is None
    assert report['management']['assignments'][1]['budget']['tokens']['estimated_used'] == 60
    assert report['management']['assignments'][0]['assets'][0]['delivery_status'] == 'stale_or_unverified'
    assert any('assignee_identity_incomplete' in a['reasons'] for a in report['management']['alerts'])
    stale = call('query', '--state', state2, '--at', stamp(60 * 60 * 48))
    assert stale['management']['goal_budget']['tokens']['current_used'] is None
    assert stale['management']['assignments'][0]['budget']['tokens']['reported_used'] == 120
    return {'legacy': 'not_recorded', 'unknown_total': None, 'known_subtotal': 120,
            'estimated_not_spent': 60, 'missing_delivery': 'stale_or_unverified', 'stale_keeps_history': 120}

def boundary():
    directory = HERE / 'boundary'
    data = fixture(directory)
    state = init(directory, data)
    original = state.read_bytes()
    errors = {}
    mutations = {}
    invalid = copy.deepcopy(data)
    invalid['nodes'][-2]['work_package']['write_scope'] = ['../outside']
    mutations['unsafe_scope'] = invalid
    invalid = copy.deepcopy(data)
    invalid['edges'].append({'from': 'T2', 'to': 'T1', 'type': 'precedes'})
    mutations['cycle'] = invalid
    invalid = copy.deepcopy(data)
    invalid['management']['usage'].append(usage('REGRESS', 'AS-A', 100, 25))
    mutations['cumulative_regression'] = invalid
    invalid = copy.deepcopy(data)
    invalid['management']['assignments'][0]['task_id'] = 'FOREIGN-TASK'
    mutations['foreign_task'] = invalid
    invalid = copy.deepcopy(data)
    invalid['management']['assignments'][0]['agent_id'] = 'silent-replacement'
    mutations['rewrite_assignee'] = invalid
    invalid = copy.deepcopy(data)
    invalid['management']['assignments'][0]['budget_limits']['tokens'] = 2000
    mutations['unapproved_budget'] = invalid
    invalid = copy.deepcopy(data)
    invalid['goal']['original_text'] = 'overwrite original intent'
    mutations['rewrite_goal'] = invalid
    for label, mutated in mutations.items():
        snap = write(directory / f'{label}.json', mutated)
        result = call('refresh', '--snapshot', snap, '--state', state, '--expected-revision', 1,
                      '--event-id', label, '--reason', 'must reject invalid input', expect=2)
        assert result['status'] == 'needs_input'
        assert state.read_bytes() == original
        errors[label] = result['error']
    assert not (HERE / 'outside').exists()
    assert not list(directory.glob('*.lock'))
    return {'rejections': errors, 'ledger_unchanged': True}

assert sha(PM) == EXPECTED, 'candidate drift before execution'
for label, scenario in [('normal', happy), ('missing_failure', missing), ('boundary', boundary)]:
    try:
        observed = scenario()
        RESULTS.append({'case': label, 'status': 'pass', 'observations': observed})
    except Exception:
        RESULTS.append({'case': label, 'status': 'fail', 'traceback': traceback.format_exc()})
    print(json.dumps(RESULTS[-1], ensure_ascii=False), flush=True)
summary = {'run_id': 'PM-SKILL-002-independent', 'started_at': START.isoformat(),
           'ended_at': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
           'tested_script': str(PM), 'sha256_before': EXPECTED, 'sha256_after': sha(PM),
           'test_sha256': sha(Path(__file__)), 'execution_origin': 'executed',
           'data_origin': 'independent synthetic fixture; not real native goals or metering',
           'cases': RESULTS, 'commands': LOG}
write(HERE / 'execution.json', summary)
assert summary['sha256_after'] == EXPECTED, 'candidate drift after execution'
sys.exit(0 if len(RESULTS) == 3 and all(r['status'] == 'pass' for r in RESULTS) else 1)
