from ast import literal_eval
from collections import Counter

from austin.github import GithubApi


class ContributorAnalyser:
    TOP_CONTRIBUTORS_LIMIT = 30

    def __init__(self, owner, repo, branch, start_date, end_date):
        self.api = GithubApi()

        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.start_date = start_date
        self.end_date = end_date

    def _populate_counter(self, commit_counter, repos_commits_json):
        for commit in repos_commits_json:
            if commit['author']:  # Only verified commits
                login = commit['author']['login']
                commit_counter[login] += 1

    def _get_top_contributors(self):
        commit_counter = Counter()

        since = self.start_date + 'T00:00:00+00:00' if self.start_date else None
        until = self.end_date + 'T00:00:00+00:00' if self.end_date else None

        json, headers = self.api.repos_commits(self.owner, self.repo, self.branch, since, until)
        self._populate_counter(commit_counter, json)

        if 'Link' in headers:
            last_page_url = headers['Link'].split(', ')[-1]
            temporary_string = last_page_url.replace('>; rel="last"', '')
            temporary_string = temporary_string[temporary_string.find('page=') + 5:]
            last_page_number = literal_eval(temporary_string)

            for page_number in range(2, last_page_number + 1):
                json, headers = self.api.repos_commits(
                    self.owner, self.repo, self.branch, since, until, page_number
                )
                self._populate_counter(commit_counter, json)

        top_contributors = commit_counter.most_common(self.TOP_CONTRIBUTORS_LIMIT)
        return top_contributors

    def analyze(self):
        info = {}
        info['top'] = self._get_top_contributors()
        return info
