from austin.utils import get_end_date_for_stale, get_github_date_filter


class IssueAnalyserMixin:
    def _search_issues(self, **parameters):
        key_value_pairs = [
            f'{key}:{value}'
            for key, value in parameters.items()
            if value
        ]
        query = ' '.join(key_value_pairs)
        json, headers = self.api.search_issues(q=query)        
        return json

    def _get_issues_count(self, start_date, end_date, search_parameters):
        date = get_github_date_filter(start_date, end_date)
        if date:
            search_parameters['created'] = date

        json = self._search_issues(**search_parameters)
        return json['total_count']

    def _get_open_issues_count(self):
        return self._get_issues_count(
            self.start_date,
            self.end_date,
            {**self.base_search_parameters, 'state': 'open'}
        )

    def _get_closed_issues_count(self):
        return self._get_issues_count(
            self.start_date,
            self.end_date,
            {**self.base_search_parameters, 'state': 'closed'}
        )

    def _get_stale_issues_count(self):
        end_date_for_stale = get_end_date_for_stale(
            self.end_date,
            self.DAYS_TO_BECOME_STALE,
        )
        return self._get_issues_count(
            self.start_date,
            end_date_for_stale,
            {**self.base_search_parameters, 'state': 'open'},
        )

    def _analyze(self):
        info = {}

        info['open_count'] = self._get_open_issues_count()
        info['closed_count'] = self._get_closed_issues_count()
        info['stale_count'] = self._get_stale_issues_count()

        return info
