from urllib.parse import urljoin

import requests

from .custom_errors import WrongAttrError, WrongResponse, WrongValueError
from .models import Issue, Repository

GITHUB_API_SEARCH_URL = 'https://api.github.com/search/'


class SearchRequest:

    def __init__(self, page=1):
        self.page = page or 1
        self.url = None
        self.response = None

    def send(self):  # TODO: add async
        self._build_url()
        #self.response = await requests.get(self.url)  # TODO: change to aiohttp
        #await self.save_into_db()

    def _build_url(self) -> None:
        self._validate_url_attrs()
        raw_url = urljoin(
            urljoin(GITHUB_API_SEARCH_URL, self.data_type),
            '?q={}&page={}'
        )
        query = '+'.join(
            ['{}:{}'.format(k, v) for k, v in self.query_params.items()]
        )
        self.url = raw_url.format(query, self.page)

    def _validate_url_attrs(self):
        if (
            not getattr(self, 'data_type', None)
            or not isinstance(self.data_type, str)
            or not bool(self.data_type)
            or not getattr(self, 'query_params', None)
            or not isinstance(self.query_params, dict)
            or not bool(self.query_params)
            or not isinstance(self.page, int)
        ):
            raise WrongAttrError


class IssueSearchRequest(SearchRequest):
    data_type = 'issues'

    def __init__(
        self,
        label: str,
        language: str,
        state: str = 'open',
        archived: bool = False,
        page: int = 1,
    ):
        self._validate_attrs(label, language, state, archived, page)
        self.query_params = {
            'label': f'"{label}"',
            'language': language,
            'state': state,
            'archived': 'true' if archived else 'false',
        }
        super().__init__(page)

    def _validate_attrs(self, label, language, state, archived, page):
        if (
            not isinstance(label, str)
            or not isinstance(language, str)
            or state not in ('open', 'closed')
            or not (archived is True or archived is False)
            or not isinstance(page, int)
        ):
            raise WrongValueError

    #async def save_into_db(self):  # TODO: tests
    #    repositories = []
    #
    #    if not self.response or not self.response.ok:
    #        raise WrongResponse
    #
    #    for item in self.response.json()['items']:
    #        await Issue.create(
    #            issue_id=item['id'],
    #            api_url=item['url'],
    #            html_url=item['html_url'],
    #            title=item['title'],
    #            created_at=item['created_at'],
    #            updated_at=item['updated_at'],
    #            closed_at=item['closed_at'],
    #            comments_count=item['comments'],
    #            labels=[label['name'] for label in item['labels']],
    #            repository_api_url=item['repository_url'],
    #        )
    #        repositories.append(item['repository_url'])
    #    await self._save_connected_repositories_into_db(repositories)
    #
    #async def _save_connected_repositories_into_db(self, reps):  # TODO: tests
    #    for rep in reps:
    #        response = requests.get(rep)
    #        if not response.ok:
    #            raise WrongResponse
    #
    #        result = response.json()
    #
    #        await Repository.create(
    #            repository_id=result['id'],
    #            api_url=result['url'],
    #            html_url=result['html_url'],
    #            name=result['name'],
    #            full_name=result['full_name'],
    #            fork=result['fork'],
    #            archived=result['archived'],
    #            forks_count=result['forks_count'],
    #            stargazers_count=result['stargazers_count'],
    #        )


class RepositorySearchRequest(SearchRequest):
    data_type = 'repositories'
