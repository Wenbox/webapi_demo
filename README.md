# A python web api demo

This is a simple example of web api using python and flask. It searches up to 1000 newly created repositories on Github since today, and up to 1000 newly posted questions on Stackoverflow since today.
There are two endpoints:
* `GET /statistics/appear_all`: display programming languages that appeared in both search results;
* `GET /statistics/top10`: display the top 10 most frequently mentioned topics from the results.

Basically this can be regarded as a gateway to invoke apis of Github and Stackoverflow.
The work process can be illustrated as follows:

![](https://raw.githubusercontent.com/Wenbox/webapi_demo/master/sketch.png)

## Prerequisite
(If possible, it is recommende to run it in a virtual environment.)

The code is tested with:
* python version = 3.6
* Flask version = 1.1.2 ([install](https://flask.palletsprojects.com/en/1.0.x/installation/#installation))
* Flask-RESTPlus version = 0.13.0 ([install](https://flask-restplus.readthedocs.io/en/stable/))

**Issue with Werkzeug v1.0.0**: The new version of Werkzeug breaks the dependency of Flask-RESTPlus. See: [flask-restplus is broken by Werkzeug 1.0.0 #777](https://github.com/noirbizarre/flask-restplus/issues/777)
The current workaround is to downgrade Werkzeug to v0.16.1 with `pip install -Iv Werkzeug==0.16.1`.

## Run
Simply type `python statistics.py` to set up the server on your local host.
Then visit http://127.0.0.1:5000 on your browser, you can see the Swagger interface.

## Test
Run `python test_query_languages.py` or `python test_statistics.py` for dummy unit test (meaningful test cases are missing currently).
I mocked the http GET to fetch contents from remote servers to save time and avoid trigering rate limit of remote servers.
Instead, the GET fetches from the local json data stored in test_data folder.
