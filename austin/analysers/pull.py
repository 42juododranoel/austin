from austin.analysers.mixins import IssueAnalyserMixin
from austin.github import GithubApi


class PullAnalyser(IssueAnalyserMixin):
    DAYS_TO_BECOME_STALE = 30

    def __init__(self, owner, repo, branch, start_date, end_date):
        self.api = GithubApi()

        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.start_date = start_date
        self.end_date = end_date

    @property
    def base_search_parameters(self):
        return {
            'repo': f'{self.owner}/{self.repo}',
            'base': self.branch,
            'type': 'pr',
        }

    def analyze(self):
        return super()._analyze()
