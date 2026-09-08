import unittest

from task_adapters import (
    ADAPTER_MAPPINGS,
    CANONICAL_OPERATIONS,
    check_tools,
    get_mapping,
    get_operation_calls,
)


class TaskAdapterMappingTests(unittest.TestCase):
    def test_supported_adapters_map_every_canonical_operation(self):
        for adapter_id, mapping in ADAPTER_MAPPINGS.items():
            with self.subTest(adapter_id=adapter_id):
                self.assertEqual(set(mapping.operations), set(CANONICAL_OPERATIONS))
                self.assertTrue(all(mapping.operations.values()))

    def test_github_issue_writes_use_the_installed_plugin_interface(self):
        create = get_operation_calls("github-issues", "create")
        transition = get_operation_calls("github-issues", "transition")
        self.assertEqual(create[0].tool, "issue_write")
        self.assertIn(("method", "create"), create[0].fixed_arguments)
        self.assertIn(("method", "update"), transition[0].fixed_arguments)
        self.assertEqual(get_mapping("github-issues").dependency, "plugin:github")

    def test_gitlab_issue_writes_use_the_installed_plugin_interface(self):
        self.assertEqual(
            get_operation_calls("gitlab-issues", "create")[0].tool,
            "save_work_item",
        )
        self.assertEqual(
            get_operation_calls("gitlab-issues", "comment")[0].tool,
            "save_note",
        )
        self.assertEqual(get_mapping("gitlab-issues").dependency, "plugin:gitlab")

    def test_unknown_adapter_or_operation_is_rejected(self):
        with self.assertRaises(ValueError):
            get_mapping("missing")
        with self.assertRaises(ValueError):
            get_operation_calls("github-issues", "delete")

    def test_tool_check_accepts_namespaced_plugin_tools_and_reports_missing(self):
        available = {
            "mcp__github__issue_write",
            "mcp__github__add_issue_comment",
        }
        self.assertTrue(check_tools("github-issues", ("create", "comment"), available).ok)
        check = check_tools("github-issues", ("fetch",), available)
        self.assertFalse(check.ok)
        self.assertEqual(check.missing, ("issue_read",))


if __name__ == "__main__":
    unittest.main()
