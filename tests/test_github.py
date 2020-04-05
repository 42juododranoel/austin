from tempfile import TemporaryFile
from unittest.mock import patch, mock_open
from urllib.request import Request
import unittest

from austin.github import GithubApi


class TestGithubApiClassAndSimpleMethods(unittest.TestCase):
    def setUp(self):
        self.open_patcher = patch('austin.github.open', mock_open(read_data='\n  \nfoobar42\n'))
        self.patched_open = self.open_patcher.start()

        self.response_patcher = patch('http.client.HTTPResponse')
        self.patched_response = self.response_patcher.start()

        self.patched_response = TemporaryFile()
        self.patched_response.write(b'{"foobar": 42}')
        self.patched_response.seek(0)
        self.patched_response.headers = {}

        self.api = GithubApi()

    def tearDown(self):
        self.open_patcher.stop()
        self.response_patcher.stop()
        self.patched_response.close()

    def test_base_url(self):
        self.assertEqual(GithubApi.BASE_URL, 'https://api.github.com')

    def test_token(self):
        self.assertEqual(self.api.token, 'foobar42')

    def test_encode_parameteres(self):
        url = self.api._encode_parameters('/foo', {'bar': 42, 'baz': None})

        self.assertEqual(url, 'https://api.github.com/foo?bar=42')

    def test_create_request(self):
        request = self.api._create_request('https://api.github.com/foo')

        self.assertTrue(isinstance(request, Request))
        self.assertEqual(dict(request.headers)['Authorization'], 'token foobar42')

    def test_parse_response(self):
        json, headers = self.api._parse_response(self.patched_response)

        self.assertEqual(json, {'foobar': 42})
        self.assertEqual(headers, {})


class TestGet(unittest.TestCase):
    def setUp(self):
        self.open_patcher = patch('austin.github.open', mock_open(read_data='\n  \nfoobar42\n'))
        self.patched_open = self.open_patcher.start()

        self.api = GithubApi()

        self.patched_response = TemporaryFile()
        self.patched_response.write(b'{"foobar": 42}')
        self.patched_response.seek(0)
        self.patched_response.headers = {}

        self.request_patcher = patch('austin.github.urllib.request.Request')
        self.patched_request = self.request_patcher.start()

        self.urlopen_patcher = patch('austin.github.urllib.request.urlopen')
        self.patched_urlopen = self.urlopen_patcher.start()
        self.patched_urlopen.return_value = self.patched_response

    def tearDown(self):
        self.open_patcher.stop()
        self.urlopen_patcher.stop()
        self.request_patcher.stop()
        self.patched_response.close()

    def test_call_urlopen(self):
        self.api.get('/foo/bar')

        self.patched_urlopen.assert_called_once()


class TestMethodWrappers(unittest.TestCase):
    def setUp(self):
        self.open_patcher = patch('austin.github.open', mock_open(read_data='\n  \nfoobar42\n'))
        self.patched_open = self.open_patcher.start()

        self.api = GithubApi()

        self.get_patcher = patch('austin.github.GithubApi.get')
        self.patched_get = self.get_patcher.start()

    def tearDown(self):
        self.open_patcher.stop()
        self.get_patcher.stop()

    def test_search_issues(self):
        self.api.search_issues(
            q='!@#$',
            per_page=42,
        )

        self.patched_get.assert_called_once_with(
            '/search/issues',
            per_page=42,
            q='%21%40%23%24'
        )

    def test_repos_commits(self):
        self.api.repos_commits(
            'octocat',
            'Hello-World',
            'master',
            '2020-02-02T00:00:00+00:00',
            '2020-03-03T00:00:00+00:00',
            1
        )

        self.patched_get.assert_called_once_with(
            '/repos/octocat/Hello-World/commits',
            page=1,
            sha='master',
            since='2020-02-02T00:00:00+00:00',
            until='2020-03-03T00:00:00+00:00',
        )
