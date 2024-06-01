import logging
import sys
from flask import Flask, request, Response

from services.vlr_service import (get_latest_news, get_recent_results, get_todays_news)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/latest-news")
def latest_news():
    cache = request.args.get('use_cache')
    use_cache = True
    if (cache != None and cache.strip().lower() == "false"):
        use_cache = False
    response = Response()
    response.set_data(get_latest_news(use_cache))
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/recent-results")
def recent_results():
    response = Response()
    response.set_data(get_recent_results())
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/todays-news")
def todays_news():
    cache = request.args.get('use_cache')
    use_cache = True
    if (cache != None and cache.strip().lower() == "false"):
        use_cache = False
    response = Response()
    import json
    response.set_data(json.dumps(get_todays_news(use_cache)))
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response
