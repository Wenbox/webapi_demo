# A python web api demo

This is a simple example of web api using python and flask. It searches up to 1000 newly created repositories on Github since today, and up to 1000 newly posted questions on Stackoverflow since today.
There are two endpoints:
* `GET /statistics/appear_all`: display programming languages that appeared in both search results;
* `GET /statistics/top10`: display the top 10 most frequently mentioned topics from the results.

Basically this can be regarded as a gateway to invoke apis of Github and Stackoverflow.
The work process can be illustrated as follows:
![alt text](https://raw.githubusercontent.com/Wenbox/webapi_demo/master/sketch.png, "sketch of this demo")

## Prerequisite
The code is tested with:
* python version >= 3.6
* Flask ([install](https://flask.palletsprojects.com/en/1.0.x/installation/#installation))
* Flask-RESTPlus ([install](https://flask-restplus.readthedocs.io/en/stable/))

## Run
Simply type `python statistics.py` to set up the server on your local host.
Then visit http://127.0.0.1:5000 on your browser, you can see the Swagger interface.
