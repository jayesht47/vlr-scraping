import logging
import sys
from typing import List
import flask
from flask import Flask

from services.vlr_service import (get_latest_news, get_recent_results)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = Flask(__name__)


@app.route("/latest-news")
def latest_news():
    response = flask.Response()
    response.set_data(get_latest_news())
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/recent-results")
def recent_results():
    response = flask.Response()
    response.set_data(get_recent_results())
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response
