import unittest

from ..custom_errors import WrongAttrError, WrongValueError
from ..requests_builder import IssueSearchRequest, SearchRequest


class SearchRequestTestCase(unittest.TestCase):  # TODO: patch aiohttp and gino
    def _get_class(self, data_type=None, q_params=None, page=1):
        class_dict = {}

        def init(self):
            if q_params is not None:
                self.query_params = q_params
            super(self.__class__, self).__init__(page)

        class_dict["__init__"] = init

        if data_type is not None:
            class_dict["data_type"] = data_type

        return type("ExampleClass", (SearchRequest,), class_dict)

    def test_url(self):
        child = self._get_class(data_type="right", q_params={"one": "a", "two": "b"})()
        self.assertEqual(
            child.url, "https://api.github.com/search/right" + "?q=one:a+two:b&page=1"
        )

    def test_url_with_not_bool_page(self):
        child = self._get_class(
            data_type="right", q_params={"one": "a", "two": "b"}, page=0
        )()
        self.assertEqual(
            child.url, "https://api.github.com/search/right" + "?q=one:a+two:b&page=1"
        )

    def test_url_with_no_data_type_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(q_params={"one": "a", "two": "b"})()

    def test_url_with_not_bool_data_type_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(data_type="", q_params={"one": "a", "two": "b"})()

    def test_url_with_wrong_type_of_data_type_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(data_type=1, q_params={"one": "a", "two": "b"})()

    def test_url_with_no_query_params_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(data_type="right")()

    def test_url_with_not_bool_query_params_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(data_type="right", q_params={})()

    def test_url_with_wrong_type_of_query_params_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(data_type="right", q_params=[1, 2, 3])()

    def test_url_with_wrong_type_of_page_attr(self):
        with self.assertRaises(WrongAttrError):
            self._get_class(
                data_type="right", q_params={"one": "a", "two": "b"}, page="qwe"
            )()


class IssueSearchRequestTestCase(unittest.TestCase):  # TODO: patch aiohttp and gino
    def test_right_values(self):
        instance = IssueSearchRequest(
            label="good first issue", language="python", page=3,
        )
        self.assertEqual(
            instance.url,
            "https://api.github.com/search/issues"
            + '?q=label:"good first issue"+language:python'
            + "+state:open+archived:false&page=3",
        )

    def test_initialize_with_wrong_type_of_label_value(self):
        with self.assertRaises(WrongValueError):
            IssueSearchRequest(label=1, language="w")

    def test_initialize_with_wrong_type_of_language_value(self):
        with self.assertRaises(WrongValueError):
            IssueSearchRequest(label="q", language=2)

    def test_initialize_with_wrong_value_of_state_value(self):
        with self.assertRaises(WrongValueError):
            IssueSearchRequest(label="q", language="w", state="wrong")

    def test_initialize_with_wrong_value_of_archived_value(self):
        with self.assertRaises(WrongValueError):
            IssueSearchRequest(label="q", language="w", archived=1)

    def test_initialize_with_wrong_type_of_page_value(self):
        with self.assertRaises(WrongValueError):
            IssueSearchRequest(label="q", language="w", page="qwe")
