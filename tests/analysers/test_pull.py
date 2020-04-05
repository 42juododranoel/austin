from ast import literal_eval
from unittest.mock import patch
import unittest

from austin.analysers import PullAnalyser
from austin.github import GithubApi


class TestPullAnalyserClassAndSimpleMethods(unittest.TestCase):
    def setUp(self):
        self.analyser = PullAnalyser('octocat', 'Hello-World', 'master', '2020-01-01', '2020-02-02')

        self.repos_commits_patcher = patch('austin.github.GithubApi.search_issues')
        self.patched_repos_commits = self.repos_commits_patcher.start()
        with open('tests/fixtures/search_issues.json', 'r') as file:
            self.patched_repos_commits.return_value = (literal_eval(file.read()), {})

    def tearDown(self):
        self.repos_commits_patcher.stop()

    def test_instantiate_github_api(self):
        self.assertTrue(isinstance(self.analyser.api, GithubApi))

    def test_init_attributes(self):
        self.assertEqual(self.analyser.owner, 'octocat')
        self.assertEqual(self.analyser.repo, 'Hello-World')
        self.assertEqual(self.analyser.branch, 'master')
        self.assertEqual(self.analyser.start_date, '2020-01-01')
        self.assertEqual(self.analyser.end_date, '2020-02-02')

    def test_days_to_become_stale(self):
        self.assertEqual(self.analyser.DAYS_TO_BECOME_STALE, 30)

    def test_base_search_parameters(self):
        self.assertEqual(
            self.analyser.base_search_parameters,
            {'base': 'master', 'repo': 'octocat/Hello-World', 'type': 'pr'}
        )

    def test_analyze(self):
        info = self.analyser.analyze()

        self.assertEqual(info, {'open_count': 43, 'closed_count': 43, 'stale_count': 43})
