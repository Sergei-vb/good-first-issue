import unittest

from ..custom_errors import WrongAttributeError
from ..requests_builder import IssuesSearchRequest


class IssuesSearchRequestTestCase(unittest.TestCase):

    def test_final_url(self):  # TODO: patch side effects
        instance = IssuesSearchRequest()
        instance.add_label('good first issue')
        instance.add_language('python')
        instance.add_state('open')
        instance.add_archived('false')
        instance.send()
        self.assertEqual(
            instance.url,
            'https://api.github.com/search/issues' +
            '?q=label:"good first issue"+language:python' +
            '+state:open+archived:false&page=1'
        )

    def test_final_url_with_not_default_page(self):  # TODO: patch side effects
        instance = IssuesSearchRequest(page=3)
        instance.add_label('good first issue')
        instance.add_language('python')
        instance.add_state('open')
        instance.add_archived('false')
        instance.send()
        self.assertEqual(
            instance.url,
            'https://api.github.com/search/issues' +
            '?q=label:"good first issue"+language:python' +
            '+state:open+archived:false&page=3'
        )

    def test_raised_error_if_send_called_with_no_any_qualifiers(self):
        instance = IssuesSearchRequest()
        with self.assertRaises(WrongAttributeError):
            instance.send()
