from datetime import date, datetime, timedelta


def get_owner_and_repo(url):
    """Parse Github repo URL to grab owner and repo"""
    no_http_github_url = url.replace('http://github.com/', '')
    no_https_github_url = no_http_github_url.replace('https://github.com/', '')
    owner, repo = no_https_github_url.split('/')
    return owner, repo


def get_end_date_for_stale(end_date, days_to_become_stale):
    """
    Determine `end_date` for stale issues and pulls

    If today is 2020-02-03, `end_date` is 2020-02-02,
    and any issue must be at least two days old to be considered stale,
    then we need to change our `end_date` by subtracting `days_to_become_stale`
    from current date. This function does this and handles some special cases
    """
    now = date.today()  # datetime.date(2020, 2, 20)
    stale_after_this_date = now - timedelta(days=days_to_become_stale)  # datetime.date(2020, 1, 10)

    if not end_date:
        end_date = str(stale_after_this_date)  # '2020-02-20'
    else:
        end_date_datetime_object = datetime.strptime(end_date, '%Y-%m-%d')  # datetime.datetime(2020, 2, 20, 0, 0)
        end_date_date_object = end_date_datetime_object.date()  # datetime.date(2020, 2, 20)

        if end_date_date_object > stale_after_this_date:
            end_date = str(stale_after_this_date)

    return end_date


def get_github_date_filter(start_date=None, end_date=None):
    """Get filter that can be used in Github Search API: >2020-02-02"""
    if start_date and end_date:
        return f'{start_date}..{end_date}'
    elif start_date:
        return f'>{start_date}'
    elif end_date:
        return f'<{end_date}'
    else:
        return ''
