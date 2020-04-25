from urllib.parse import urljoin

from .custom_errors import WrongAttributeError, WrongValueError


class SearchRequest:
    github_api_search_url = 'https://api.github.com/search/'
    data_type = None

    def __init__(self, page=1):
        self.url = None
        self.page = page
        self.query_params = {}

    def send(self):
        self._build_url()
        # TODO: sending

    def _build_url(self):
        if not self.data_type or not isinstance(self.data_type, str):
            raise WrongAttributeError(
                'The data_type attribute is not set or not string type!'
            )

        if not self.query_params:
            raise WrongAttributeError(
                'The query_params attribute can not be empty. ' +
                'Need to add any qualifiers!'
            )

        raw_url = urljoin(
            urljoin(self.github_api_search_url, self.data_type),
            '?q={}&page={}'
        )

        query = '+'.join(
            ['{}:{}'.format(k, v) for k, v in self.query_params.items()]
        )
        self.url = raw_url.format(query, self.page)


class IssuesSearchRequest(SearchRequest):
    data_type = 'issues'

    def add_label(self, value):
        self.query_params['label'] = '"{}"'.format(value)

    def add_language(self, value):  # TODO: add checking for PL
        self.query_params['language'] = value

    def add_state(self, value):
        if value not in ('open', 'closed'):
            raise WrongValueError

        self.query_params['state'] = value

    def add_archived(self, value):
        if value not in ('true', 'false'):
            raise WrongValueError

        self.query_params['archived'] = value


class RepositoriesSearchRequest(SearchRequest):
    data_type = 'repositories'
