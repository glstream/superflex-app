from pydantic import BaseModel


class UserDataModel(BaseModel):
    user_name: str
    league_year: str


class LeagueDataModel(BaseModel):
    league_id: str
