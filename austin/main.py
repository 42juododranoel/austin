from austin.analysers import (
    ContributorAnalyser,
    IssueAnalyser,
    PullAnalyser,
)
from austin.utils import get_owner_and_repo


def main(url, branch=None, start_date=None, end_date=None):
    """Analyze Github repository and return info"""

    owner, repo = get_owner_and_repo(url)

    info = {}

    contributor_analyser = ContributorAnalyser(owner, repo, branch, start_date, end_date)
    info['contributors'] = contributor_analyser.analyze()

    pull_analyser = PullAnalyser(owner, repo, branch, start_date, end_date)
    info['pulls'] = pull_analyser.analyze()

    issue_analyser = IssueAnalyser(owner, repo, start_date, end_date)
    info['issues'] = issue_analyser.analyze()

    return info
