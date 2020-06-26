import unittest
import json
from unittest import mock
from query_languages import stackoverflow_engine, github_engine, search_engine

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].startswith(stackoverflow_engine.stackoverflow_base):
        f = open('test_data/response_stackoverflow_p1.json')
        content = json.load(f)
        f.close()
        content['has_more'] = False
        return MockResponse(content, 200)
    elif args[0].startswith(github_engine.github_base):
        f = open('test_data/github_response_p1.json')
        content = json.load(f)
        f.close()
        return MockResponse(content, 200)
    else:
        return MockResponse(None, 400)



class stackoverflow_engine_tests(unittest.TestCase):
    @mock.patch('query_languages.requests.Session.get', side_effect=mocked_requests_get)
    def test_search_with_decorator(self, mock_get):
        lans = stackoverflow_engine().search()
        self.assertTrue(lans)

class github_engine_tests(unittest.TestCase):
    @mock.patch('query_languages.requests.Session.get', side_effect=mocked_requests_get)
    def test_search_with_decorator(self, mock_get):
        lans = github_engine().search()
        self.assertTrue(lans)

class search_engine_tests(unittest.TestCase):
    @mock.patch('query_languages.requests.Session.get', side_effect=mocked_requests_get)
    def test_search_with_decorator(self, mock_get):
        lans = search_engine().search()
        self.assertTrue(lans)

if __name__ == "__main__":
    unittest.main()


