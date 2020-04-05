from ast import literal_eval
from collections import Counter
from unittest.mock import patch
import unittest

from austin.analysers import ContributorAnalyser
from austin.github import GithubApi

EXPECTED_TOP_CONTRIBUTORS = [('charettes', 6), ('felixxm', 3), ('matheuscmotta', 3), ('007gzs', 2), ('vdboor', 2), ('claudep', 1), ('Hansikk', 1), ('carltongibson', 1), ('kimbo', 1), ('cmackenziek', 1), ('rohitjha941', 1), ('Valze', 1), ('dorosch', 1), ('coltonbh', 1), ('hramezani', 1), ('cool-RR', 1), ('Taoup', 1), ('adamchainz', 1)]


class TestContributorAnalyserClassAndSimpleMethods(unittest.TestCase):
    def setUp(self):
        self.analyser = ContributorAnalyser('octocat', 'Hello-World', 'master', '2020-01-01', '2020-02-02')

    def test_instantiate_github_api(self):
        self.assertTrue(isinstance(self.analyser.api, GithubApi))

    def test_init_attributes(self):
        self.assertEqual(self.analyser.owner, 'octocat')
        self.assertEqual(self.analyser.repo, 'Hello-World')
        self.assertEqual(self.analyser.branch, 'master')
        self.assertEqual(self.analyser.start_date, '2020-01-01')
        self.assertEqual(self.analyser.end_date, '2020-02-02')

    def test_top_contributors_limit(self):
        self.assertEqual(self.analyser.TOP_CONTRIBUTORS_LIMIT, 30)

    def test_populate_counter(self):
        json = [
            {'author': {'login': 'foo'}},
            {'author': {'login': 'foo'}},
            {'author': {'login': 'bar'}},
        ]
        counter = Counter()

        self.analyser._populate_counter(counter, json)

        self.assertEqual(counter.most_common(30), [('foo', 2), ('bar', 1)])


class TestAnalyze(unittest.TestCase):
    def setUp(self):
        self.analyser = ContributorAnalyser('octocat', 'Hello-World', 'master', '2020-01-01', '2020-02-02')

        self.get_top_contributors_patcher = patch('austin.analysers.contributor.ContributorAnalyser._get_top_contributors')
        self.patched_get_top_contributors = self.get_top_contributors_patcher.start()
        self.patched_get_top_contributors.return_value = [['timgraham', 3292], ['adrianholovaty', 2769], ['malcolmt', 1865]]

    def tearDown(self):
        self.get_top_contributors_patcher.stop()

    def test_analyze(self):
        info = self.analyser.analyze()

        self.assertEqual(info, {'top': [['timgraham', 3292], ['adrianholovaty', 2769], ['malcolmt', 1865]]})


class TestGetTopContributors(unittest.TestCase):
    def setUp(self):
        self.analyser = ContributorAnalyser('octocat', 'Hello-World', 'master', '2020-01-01', '2020-02-02')

        self.repos_commits_patcher = patch('austin.github.GithubApi.repos_commits')
        self.patched_repos_commits = self.repos_commits_patcher.start()
        with open('tests/fixtures/repos_commits.json', 'r') as file:
            self.patched_repos_commits.return_value = (literal_eval(file.read()), {})

    def tearDown(self):
        self.repos_commits_patcher.stop()

    def test_analyze(self):
        info = self.analyser._get_top_contributors()

        self.assertEqual(info, EXPECTED_TOP_CONTRIBUTORS)
