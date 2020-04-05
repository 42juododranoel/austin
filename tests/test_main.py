from unittest.mock import patch
import unittest

from austin.main import main

EXPECTED_INFO = {
    'contributors': {
        'top': [
            ['spiderman', 42],
            ['batman', 27],
        ]
    },
    'pulls': {
        'open_count': 1,
        'closed_count': 2,
        'stale_count': 3,
    },
    'issues': {
        'open_count': 1,
        'closed_count': 2,
        'stale_count': 3,
    }
}


class TestMain(unittest.TestCase):
    def setUp(self):
        self.contributor_analyser_analyze_patcher = patch('austin.main.ContributorAnalyser.analyze')
        self.patched_contributor_analyser_analyze = self.contributor_analyser_analyze_patcher.start()
        self.patched_contributor_analyser_analyze.return_value = EXPECTED_INFO['contributors']

        self.pull_analyser_analyze_patcher = patch('austin.main.PullAnalyser.analyze')
        self.patched_pull_analyser_analyze = self.pull_analyser_analyze_patcher.start()
        self.patched_pull_analyser_analyze.return_value = EXPECTED_INFO['pulls']

        self.issue_analyser_analyze_patcher = patch('austin.main.IssueAnalyser.analyze')
        self.patched_issue_analyser_analyze = self.issue_analyser_analyze_patcher.start()
        self.patched_issue_analyser_analyze.return_value = EXPECTED_INFO['issues']

    def tearDown(self):
        self.contributor_analyser_analyze_patcher.stop()
        self.pull_analyser_analyze_patcher.stop()
        self.issue_analyser_analyze_patcher.stop()

    def test_return_info(self):
        info = main(
            url='https://github.com/octocat/Hello-World',
            branch='master',
            start_date='2020-01-01',
            end_date='2020-02-02',
        )

        self.assertEqual(info, EXPECTED_INFO)
