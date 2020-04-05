from austin.analysers.mixins import IssueAnalyserMixin
from austin.github import GithubApi


class IssueAnalyser(IssueAnalyserMixin):
    DAYS_TO_BECOME_STALE = 14

    def __init__(self, owner, repo, start_date, end_date):
        self.api = GithubApi()

        self.owner = owner
        self.repo = repo
        self.start_date = start_date
        self.end_date = end_date

    @property
    def base_search_parameters(self):
        return {
            'repo': f'{self.owner}/{self.repo}',
            'type': 'issue',
        }

    def analyze(self):
        return super()._analyze()
