import json
from flask import Flask, request
from flask_restplus import Api, Resource, fields
from query_languages import search_engine
from datetime import date


flask_app = Flask(__name__)
app = Api(app = flask_app, 
            version = "1.0",
            title = "Programming language statistics",
            description = "Count the frequency of programming languages appeared on github and stackoverflow")

name_space = app.namespace('statistics', description='Statistics of programming languages')

cached = {}

@name_space.route("/top10")
class TopTenList(Resource):	
    @app.doc(responses={ 200: 'OK', 400: 'Rate limit reached. Please try later.', 500: 'Server error' })
    def get(self):
        global cached
        if (not 'created_date' in cached) or cached['created_date'] != date.today():
            cached = search_engine().search()
        sorted_list = {tag: count for tag, count in sorted(cached['items'].items(), key = lambda item: item[1]['counts'], reverse = True)}
        return json.dumps({k : sorted_list[k]['counts'] for k in list(sorted_list)[:10]})
        
@name_space.route("/appear_all")
class ApearAllList(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Rate limit reached. Please try later.', 500: 'Server error' })
    def get(self):
        global cached
        if (not 'created_date' in cached) or cached['created_date'] != date.today():
            cached = search_engine().search()
        return json.dumps([tag for tag, prop in cached['items'].items() if len(prop['contained']) == len(search_engine.sites)])



flask_app.run()
