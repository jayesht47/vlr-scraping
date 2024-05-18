import logging
import sys
from typing import List

from llama_index.core import Document
from llama_index.readers.web import UnstructuredURLLoader
from services.vlr_service import get_latest_news

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

get_latest_news()
