from dataclasses import dataclass
from json import JSONEncoder


@dataclass
class News():
    title: str
    link: str


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, News)):
            return {"title": obj.title, "link": obj.link}
