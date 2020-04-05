from datetime import date
from unittest.mock import patch
import unittest

from austin.utils import (
    get_owner_and_repo,
    get_end_date_for_stale,
    get_github_date_filter,
)


class TestGetOwnerAndRepo(unittest.TestCase):
    def test_handle_https_github(self):
        owner, repo = get_owner_and_repo('https://github.com/django/django')

        self.assertTupleEqual((owner, repo), ('django', 'django'))

    def test_handle_http_github(self):
        owner, repo = get_owner_and_repo('http://github.com/octocat/Hello-World')

        self.assertTupleEqual((owner, repo), ('octocat', 'Hello-World'))


class TestGetGithubDateFilter(unittest.TestCase):
    def test_start_date_gt(self):
        date = get_github_date_filter(start_date='2020-02-02')

        self.assertEqual(date, '>2020-02-02')

    def test_end_date_lt(self):
        date = get_github_date_filter(end_date='2020-02-02')

        self.assertEqual(date, '<2020-02-02')

    def test_start_end_range(self):
        date = get_github_date_filter(
            start_date='2010-01-01',
            end_date='2020-02-02',
        )

        self.assertEqual(date, '2010-01-01..2020-02-02')


class TestGetEndDateForStale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.date_patcher = patch('austin.utils.date')
        cls.patched_date = cls.date_patcher.start()
        cls.patched_date.today.return_value = date(2020, 2, 3)

    @classmethod
    def tearDownClass(cls):
        cls.date_patcher.stop()

    def test_dont_subract_days_from_end_date_when_old(self):
        end_date = get_end_date_for_stale(end_date='2000-01-01', days_to_become_stale=100)

        self.assertEqual(end_date, '2000-01-01')

    def test_subract_days_from_end_date_when_recent(self):
        end_date = get_end_date_for_stale(end_date='2020-02-02', days_to_become_stale=2)

        self.assertEqual(end_date, '2020-02-01')

    def test_subract_days_from_now_when_end_date_none(self):
        end_date = get_end_date_for_stale(end_date=None, days_to_become_stale=2)

        self.assertEqual(end_date, '2020-02-01')
