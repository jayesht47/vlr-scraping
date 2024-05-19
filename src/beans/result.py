from dataclasses import dataclass
from json import JSONEncoder


@dataclass
class Result():
    match_time: str = None
    match_event: str = None
    match_series: str = None
    match_link: str = None
    match_team_1: str = None
    match_team_1_score: str = None
    match_team_2: str = None
    match_team_2_score: str = None


class CustomResultEncoder(JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, Result)):
            return {"match_time": obj.match_time,
                    "match_event": obj.match_event,
                    "match_series": obj.match_series,
                    "match_link": obj.match_link,
                    "match_team_1": obj.match_team_1,
                    "match_team_1_score": obj.match_team_1_score,
                    "match_team_2": obj.match_team_2,
                    "match_team_2_score": obj.match_team_2_score}
