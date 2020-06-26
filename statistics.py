import json
from flask import Flask, request
from flask_restplus import Api, Resource, fields, reqparse
from query_languages import search_engine, RateLimitException, ServerException
import time

flask_app = Flask(__name__, instance_relative_config=True)
app = Api(app = flask_app,
            version = "1.0",
            title = "Programming language statistics",
            description = "Count the frequency of programming languages appeared on github and stackoverflow")

name_space = app.namespace('statistics', description='Statistics of programming languages')

cached = {}
parser = reqparse.RequestParser()
parser.add_argument('n', type=int, help='1<= n <=10, default 10.')

@name_space.route("/topn")
class TopNList(Resource):
    @app.expect(parser)
    @app.doc(responses={ 200: 'OK', 400: 'Bad Request', 429: 'Too many requests and rate limit reached. Please try later', 502: 'Bad gateway. The upstream server does not responde.' })
    def get(self):
        """
        Get top n tags / programming languages.
        """
        n = 10

        args = parser.parse_args()
        if args['n'] and args['n'] > 0 and args['n'] <= 10:
            n = args['n']

        global cached
        try:
            if (not 'created_time' in cached) or time.time() - cached['created_time'] > 600:
                cached = search_engine().search()
        except RateLimitException as e:
            name_space.abort(429, e.__doc__, status = "Ratelimit violation", statusCode = "429")
        except ServerException as e:
            name_space.abort(502, e.__doc__, status = "Could not connect to server", statusCode = "502")

        sorted_list = {tag: count for tag, count in sorted(cached['items'].items(), key = lambda item: item[1]['counts'], reverse = True)}
        return json.dumps({k : sorted_list[k]['counts'] for k in list(sorted_list)[:n]})

@name_space.route("/appear_all")
class AppearAllList(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Bad Request', 429: 'Too many requests and rate limit reached. Please try later', 502: 'Bad gateway. The upstream server does not responde.' })
    def get(self):
        """
        Get tags / programming languages from all websites.
        """
        global cached
        try:
            if (not 'created_time' in cached) or time.time() - cached['created_time'] > 600:
                cached = search_engine().search()
        except RateLimitException as e:
            name_space.abort(429, e.__doc__, status = "Ratelimit violation", statusCode = "429")
        except ServerException as e:
            name_space.abort(502, e.__doc__, status = "Could not connect to server", statusCode = "502")

        return json.dumps([tag for tag, prop in cached['items'].items() if len(prop['contained']) == len(search_engine.sites)])


if __name__ == "__main__":
    flask_app.run()
