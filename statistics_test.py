import unittest
from unittest import mock
from statistics import flask_app, TopNList, AppearAllList
from query_languages_test import mocked_requests_get

class StatisticsServerTests(unittest.TestCase):
    def setUp(self):
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.config['DEBUG'] = False
        self.app = flask_app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('query_languages.requests.Session.get', side_effect=mocked_requests_get)
    def test_topn_with_decorator(self, mock_get):
        response = self.app.get("/statistics/topn",follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('query_languages.requests.Session.get', side_effect=mocked_requests_get)
    def test_appear_all_with_decorator(self, mock_get):
        response = self.app.get("/statistics/appear_all",follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_non_existing(self):
        response = self.app.get("/funny", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()



