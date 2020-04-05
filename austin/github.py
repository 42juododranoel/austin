from urllib.parse import quote
import json
import urllib.request


class GithubApi:
    BASE_URL = 'https://api.github.com'

    def __init__(self):
        with open('.token') as file:
            self.token = file.read().strip()

    def _encode_parameters(self, endpoint, parameters):
        url = f'{self.BASE_URL}{endpoint}'
        if parameters:
            key_value_pairs = [
                f'{key}={value}'
                for key, value in parameters.items()
                if value
            ]
            url += '?' + '&'.join(key_value_pairs)
        return url

    def _create_request(self, url):
        request = urllib.request.Request(url)
        request.add_header('Authorization', 'token ' + self.token)
        return request

    def _parse_response(self, response):
        response_headers = dict(response.headers)

        response_binary_content = response.read()
        response_content = response_binary_content.decode('utf-8')
        response_json = json.loads(response_content)

        return response_json, response_headers

    def get(self, endpoint, **parameters):
        url = self._encode_parameters(endpoint, parameters)
        request = self._create_request(url)
        response = urllib.request.urlopen(request)
        return self._parse_response(response)

    def search_issues(self, q, per_page=1):
        parameters = {'q': quote(q), 'per_page': per_page}
        endpoint = '/search/issues'
        return self.get(endpoint, **parameters)

    def repos_commits(self, owner, repo, sha=None, since=None, until=None, page=1):
        parameters = {'sha': sha, 'since': since, 'until': until, 'page': page}
        endpoint = f'/repos/{owner}/{repo}/commits'
        return self.get(endpoint, **parameters)
