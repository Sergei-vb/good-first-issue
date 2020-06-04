from abc import ABC, abstractmethod
from urllib.parse import urljoin

from .custom_errors import WrongAttributeError, WrongValueError

GITHUB_API_SEARCH_URL = 'https://api.github.com/search/'


class SearchRequest(ABC):
    data_type: str

    def __init__(self):
        self.url = None
        self.page = 1
        self.query_params = {}

    @property
    @abstractmethod
    def data_type(self):
        pass

    def send(self):
        self._build_url()
        # TODO: sending

    def _build_url(self) -> None:
        if not self.query_params:
            raise WrongAttributeError(
                'The query_params attribute can not be empty. Need to add any qualifiers!'
            )

        raw_url = urljoin(
            urljoin(GITHUB_API_SEARCH_URL, self.data_type),
            '?q={}&page={}'
        )

        query = '+'.join(
            ['{}:{}'.format(k, v) for k, v in self.query_params.items()]
        )
        self.url = raw_url.format(query, self.page)


class IssueSearchRequest(SearchRequest):
    data_type = 'issues'

    def add_label(self, value: str) -> None:
        self.query_params['label'] = '"{}"'.format(value)

    def add_language(self, value: str) -> None:  # TODO: add checking for PL
        self.query_params['language'] = value

    def add_state(self, value: str) -> None:
        if value not in ('open', 'closed'):
            raise WrongValueError

        self.query_params['state'] = value

    def add_archived(self, value: str) -> None:
        if value not in ('true', 'false'):
            raise WrongValueError

        self.query_params['archived'] = value

    def add_page(self, value: int) -> None:
        if not str(value).isnumeric():
            raise WrongValueError

        self.page = value


class RepositorySearchRequest(SearchRequest):
    data_type = 'repositories'
