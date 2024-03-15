from fastapi import FastAPI, Depends
from psycopg2 import extras
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
from superflex_models import UserDataModel, LeagueDataModel
from pathlib import Path

# UTILS
from utils import (get_user_id, insert_current_leagues, insert_league)

# Load environment variables from .env file
load_dotenv()
# Define a list of allowed origins (use ["*"] for allowing all origins)
origins = [
    "*",
]

app = FastAPI()
# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user_details")
def user_details(user_data: UserDataModel, db=Depends(get_db)):
    return insert_current_leagues(db, user_data)


@app.post("/league_details")
def league_details(league_data: LeagueDataModel, db=Depends(get_db)):
    print('attempt')
    return insert_league(db, league_data)


@app.get("/leagues")
def leagues(league_year: str, user_name: str, db: str = Depends(get_db)):
    cursor_ = db.cursor(cursor_factory=extras.RealDictCursor)
    user_id = get_user_id(user_name)
    session_id = 'cc73437c-40b6-4cd4-9835-6b41033968c4'  # testing session_id

    cursor_.execute(
        f"""select ROW_NUMBER() OVER() as key, session_id, cl.user_id, cl.league_id, league_name, avatar, total_rosters, qb_cnt, CASE WHEN sf_cnt > 0 THEN 'Superflex' else 'SingleQB' end as sf_check, starter_cnt, total_roster_cnt, sport, insert_date, rf_cnt, case when league_cat = 0 THEN 'redraft' else 'dynasty' end as league_type, league_year, rs.ktc_power_rank, rs.sf_power_rank, rs.fc_power_rank, rs.dp_power_rank, rs.espn_contender_rank, rs.nfl_contender_rank, rs.fp_contender_rank, rs.fc_contender_rank, rs.cbs_contender_rank 
    from dynastr.current_leagues cl 
    left join dynastr.ranks_summary rs on cl.league_id = rs.league_id and cl.user_id = rs.user_id  
    where 1=1
    and session_id = 'cc73437c-40b6-4cd4-9835-6b41033968c4' 
    and cl.user_id ='{user_id}' 
    and league_year = '{league_year}'
    limit 10"""
    )
    db_resp_obj = cursor_.fetchall()

    return db_resp_obj


@app.get("/league")
def league(league_id: str, platform: str, rank_type: str, db: str = Depends(get_db)):
    print(league_id, platform, rank_type)

    cursor_ = db.cursor(cursor_factory=extras.RealDictCursor)
    session_id = 'cc73437c-40b6-4cd4-9835-6b41033968c4'  # testing session_id
    league_type = 'sf_value'

    if platform == 'sf':
        league_pos_col = (
            "superflex_sf_pos_rank"
            if league_type == "sf_value"
            else "superflex_one_qb_pos_rank"
        )
        league_type = (
            "superflex_sf_value"
            if league_type == "sf_value"
            else "superflex_one_qb_value"
        )
        with open(
            Path.cwd() / "sql" / "details" /
            f"{rank_type}" / f"{platform}.sql",
            "r",
        ) as power_file:
            power_sql = (
                power_file.read()
                .replace("'session_id'", f"'{session_id}'")
                .replace("league_type", f"{league_type}")
                .replace("'league_id'", f"'{league_id}'")
                .replace("league_pos_col", f"{league_pos_col}")
            )

    else:
        with open(
            Path.cwd() / "sql" / "details" /
            f"{rank_type}" / f"{platform}.sql",
            "r",
        ) as power_file:
            power_sql = (
                power_file.read()
                .replace("'session_id'", f"'{session_id}'")
                .replace("league_type", f"{league_type}")
                .replace("'league_id'", f"'{league_id}'")
            )
    cursor_.execute(power_sql)
    db_resp_obj = cursor_.fetchall()

    return db_resp_obj
