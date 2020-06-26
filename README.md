# A python web api demo

This is a simple example of web API using Python and Flask.
It searches up to 1000 newly created repositories on GitHub since today,
and up to 1000 newly posted questions on StackOverflow since today.
There are two endpoints:

* `GET /statistics/appear_all`: display programming languages that appeared in both search results;
* `GET /statistics/top10`: display the top 10 most frequently mentioned topics from the results.

Basically this can be regarded as a gateway to invoke APIs of GitHub and StackOverflow.
The work process can be illustrated as follows:

![](https://raw.githubusercontent.com/Wenbox/webapi_demo/master/sketch.png)

## Prerequisite

If possible, it is recommended to run it in a virtual environment.

* Create virtual environment (Python 3): `python3 -m venv localvenv`
* Activate virtual environment: `. localvenv/bin/activate`

Dependencies are documented in `requirements.txt`

* Install dependencies using pip: `pip install -r requirements.txt`

**Issue with Werkzeug v1.0.0**: The new version of Werkzeug breaks the dependency of Flask-RESTPlus.
See: [flask-restplus is broken by Werkzeug 1.0.0 #777](https://github.com/noirbizarre/flask-restplus/issues/777)
The current workaround is to downgrade Werkzeug to v0.16.1.

The code is tested with:

* python version = 3.6

## Run

Simply type `python statistics.py` to set up the server on your local host.
Then visit http://127.0.0.1:5000 on your browser, you can see the Swagger interface.

## Test

Run `python -m unittest` for dummy unit test.
More meaningful test cases will follow.
The http GET to fetch contents is mocked in order to become independent from remote servers.
Thus, the GET fetches local json data stored in the folder `test_data`.
