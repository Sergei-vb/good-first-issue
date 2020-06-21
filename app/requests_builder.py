from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import aiohttp

from .config import get_db_url
from .custom_errors import (
    WrongAttrError,
    WrongResponseError,
    WrongValueError,
)
from .models import db, Issue, Repository

DB_URL = get_db_url()
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

    @staticmethod
    def get_right_datetime(d_time: str) -> Optional[datetime]:
        if d_time is None:
            return None
        return datetime.strptime(d_time, '%Y-%m-%dT%H:%M:%SZ')


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

        for issue_item in self.response['items']:
            # TODO: check if repository already exists !!!
            rep_item = await self._get_json(url=issue_item['repository_url'])

            await Repository.create(
                repository_id=rep_item['id'],
                api_url=rep_item['url'],
                html_url=rep_item['html_url'],
                name=rep_item['name'],
                full_name=rep_item['full_name'],
                fork=rep_item['fork'],
                archived=rep_item['archived'],
                forks_count=rep_item['forks_count'],
                stargazers_count=rep_item['stargazers_count'],
            )

            await Issue.create(  # TODO: add checking if already exists
                issue_id=issue_item['id'],
                api_url=issue_item['url'],
                html_url=issue_item['html_url'],
                title=issue_item['title'],
                created_at=self.get_right_datetime(issue_item['created_at']),
                updated_at=self.get_right_datetime(issue_item['updated_at']),
                closed_at=self.get_right_datetime(issue_item['closed_at']),
                comments_count=issue_item['comments'],
                labels=[label['name'] for label in issue_item['labels']],
                repository_api_url=issue_item['repository_url'],
            )


class RepositorySearchRequest(SearchRequest):
    data_type = 'repositories'
