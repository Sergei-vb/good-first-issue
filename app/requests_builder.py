import os
from typing import Optional
from urllib.parse import urljoin

import aiohttp

from .custom_errors import (
    EnvironmentVariablesError,
    WrongAttrError,
    WrongResponseError,
    WrongValueError,
)
from .models import db, Issue, Repository

connection_data = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('DATABASE_HOST'),
    'port': os.getenv('DATABASE_PORT'),
    'database': os.getenv('POSTGRES_DB')
}

if None in connection_data.values():
    raise EnvironmentVariablesError

DB_URL = 'postgres://{user}:{password}@{host}:{port}/{database}'.format(
    user=connection_data['user'],
    password=connection_data['password'],
    host=connection_data['host'],
    port=connection_data['port'],
    database=connection_data['database']
)
GITHUB_API_SEARCH_URL = 'https://api.github.com/search/'


class SearchRequest:

    def __init__(self, page=1):
        self.page = page or 1
        self.url = self._build_url()
        self.response = None

    def _build_url(self):
        self._validate_url_attrs()
        raw_url = urljoin(
            urljoin(GITHUB_API_SEARCH_URL, self.data_type),
            '?q={}&page={}'
        )
        query = '+'.join(
            ['{}:{}'.format(k, v) for k, v in self.query_params.items()]
        )
        return raw_url.format(query, self.page)

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

    async def send(self) -> None:
        self.response = await self._get_json()

        async with db.with_bind(DB_URL):
            await self._save_into_db()

    async def _get_json(self, url: Optional[str] = None):  # TODO: add an annotation for return; add tests!
        async with aiohttp.ClientSession() as session:
            async with session.get(url or self.url) as response:
                if response.status != 200:
                    raise WrongResponseError
                return await response.json()


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

    async def _save_into_db(self):  # TODO: tests
        repositories = []

        for item in self.response['items']:
            await Issue.create(
                issue_id=item['id'],
                api_url=item['url'],
                html_url=item['html_url'],
                title=item['title'],
                created_at=item['created_at'],
                updated_at=item['updated_at'],
                closed_at=item['closed_at'],
                comments_count=item['comments'],
                labels=[label['name'] for label in item['labels']],
                repository_api_url=item['repository_url'],
            )
            repositories.append(item['repository_url'])
        await self._save_connected_repositories_into_db(repositories)

    async def _save_connected_repositories_into_db(self, reps):  # TODO: tests
        for rep in reps:
            result = await self._get_json(url=rep)

            await Repository.create(
                repository_id=result['id'],
                api_url=result['url'],
                html_url=result['html_url'],
                name=result['name'],
                full_name=result['full_name'],
                fork=result['fork'],
                archived=result['archived'],
                forks_count=result['forks_count'],
                stargazers_count=result['stargazers_count'],
            )


class RepositorySearchRequest(SearchRequest):
    data_type = 'repositories'
