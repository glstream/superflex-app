import requests
from requests.exceptions import RequestException
from time import sleep
from psycopg2.extras import execute_batch
from superflex_models import UserDataModel, LeagueDataModel
from datetime import datetime


def make_api_call(
    url, params=None, headers=None, timeout=10, max_retries=5, backoff_factor=1
):
    for retry in range(max_retries):
        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=timeout
            )
            # Raise an exception if the response contains an HTTP error status code
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if retry < max_retries - 1:
                sleep_time = backoff_factor * (2 ** retry)
                print(
                    f"Error while making API call: {e}. Retrying in {sleep_time} seconds..."
                )
                sleep(sleep_time)
            else:
                print(
                    f"Error while making API call: {e}. Reached maximum retries ({max_retries})."
                )
                raise


def get_user_id(user_name: str) -> str:
    user_url = f"https://api.sleeper.app/v1/user/{user_name}"
    user_id = make_api_call(user_url)["user_id"]

    return user_id


def get_user_name(user_id: str):
    username_url = f"https://api.sleeper.app/v1/user/{user_id}"
    user_meta = make_api_call(username_url)
    return (user_meta["username"], user_meta["display_name"])


def get_user_leagues(user_name: str, league_year: str) -> list:
    owner_id = get_user_id(user_name)
    leagues_json = make_api_call(
        f"https://api.sleeper.app/v1/user/{owner_id}/leagues/nfl/{league_year}"
    )
    leagues = []
    for league in leagues_json:
        qbs = len([i for i in league["roster_positions"] if i == "QB"])
        rbs = len([i for i in league["roster_positions"] if i == "RB"])
        wrs = len([i for i in league["roster_positions"] if i == "WR"])
        tes = len([i for i in league["roster_positions"] if i == "TE"])
        flexes = len([i for i in league["roster_positions"] if i == "FLEX"])
        super_flexes = len(
            [i for i in league["roster_positions"] if i == "SUPER_FLEX"])
        rec_flexes = len(
            [i for i in league["roster_positions"] if i == "REC_FLEX"])
        starters = sum([qbs, rbs, wrs, tes, flexes, super_flexes, rec_flexes])
        leagues.append(
            (
                league["name"],
                league["league_id"],
                league["avatar"],
                league["total_rosters"],
                qbs,
                rbs,
                wrs,
                tes,
                flexes,
                super_flexes,
                starters,
                len(league["roster_positions"]),
                league["sport"],
                rec_flexes,
                league["settings"]["type"],
                league_year,
                league["previous_league_id"],
            )
        )
    return leagues


def insert_current_leagues(db, user_data: UserDataModel):
    user_name = user_data.user_name
    league_year = user_data.league_year
    leagues = get_user_leagues(user_name, league_year)
    session_id = 'TEST_FAST_API'
    user_id = get_user_id(user_name)
    entry_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    delete_user_leagues_query = f"""DELETE FROM dynastr.current_leagues where user_id = '{user_id}' and session_id ='{session_id}'"""
    cursor = db.cursor()
    cursor.execute(delete_user_leagues_query)

    print(f"Leagues for user: {user_id} Cleaned.")

    db.commit()
    # insert leagues
    execute_batch(
        cursor,
        """INSERT INTO dynastr.current_leagues (session_id, user_id, user_name, league_id, league_name, avatar, total_rosters, qb_cnt, rb_cnt, wr_cnt, te_cnt, flex_cnt, sf_cnt, starter_cnt, total_roster_cnt, sport, insert_date, rf_cnt, league_cat, league_year, previous_league_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
   ON CONFLICT (session_id, league_id) DO UPDATE 
  SET user_id = excluded.user_id,
  		user_name = excluded.user_name,
		league_id = excluded.league_id,
		league_name = excluded.league_name,
		avatar = excluded.avatar,
		total_rosters = excluded.total_rosters,
		qb_cnt = excluded.qb_cnt,
		rb_cnt = excluded.rb_cnt,
		wr_cnt = excluded.wr_cnt,
		te_cnt = excluded.te_cnt,
		flex_cnt = excluded.flex_cnt,
		sf_cnt = excluded.sf_cnt,
		starter_cnt = excluded.starter_cnt,
		total_roster_cnt = excluded.total_roster_cnt,
		sport = excluded.sport,
      	insert_date = excluded.insert_date,
        rf_cnt = excluded.rf_cnt,
        league_cat = excluded.league_cat,
        league_year = excluded.league_year,
        previous_league_id = excluded.previous_league_id;
    """,
        tuple(
            [
                (
                    session_id,
                    user_id,
                    user_name,
                    league[1],
                    league[0],
                    league[2],
                    league[3],
                    league[4],
                    league[5],
                    league[6],
                    league[7],
                    league[8],
                    league[9],
                    league[10],
                    league[11],
                    league[12],
                    entry_time,
                    league[13],
                    league[14],
                    league[15],
                    league[16],
                )
                for league in iter(leagues)
            ]
        ),
        page_size=1500,
    )
    db.commit()
    cursor.close()
    return


def insert_league(db, league_data: LeagueDataModel):
    print('exeuting')
    user_id = "342397313982976000"
    entry_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    session_id = 'TEST_FAST_API'
    league_single = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_data.league_id}")
    try:
        qbs = len([i for i in league_single["roster_positions"] if i == "QB"])
        rbs = len([i for i in league_single["roster_positions"] if i == "RB"])
        wrs = len([i for i in league_single["roster_positions"] if i == "WR"])
        tes = len([i for i in league_single["roster_positions"] if i == "TE"])
        flexes = len(
            [i for i in league_single["roster_positions"] if i == "FLEX"])
        super_flexes = len(
            [i for i in league_single["roster_positions"] if i == "SUPER_FLEX"]
        )
        rec_flexes = len(
            [i for i in league_single["roster_positions"] if i == "REC_FLEX"]
        )
    except Exception as e:
        print(
            f"An error occurred: {e} on league_single call, seession_id: {session_id}, user_id: {user_id}, league_id:{league_data.league_id}"
        )

    starters = sum([qbs, rbs, wrs, tes, flexes, super_flexes, rec_flexes])
    user_name = get_user_name(user_id)[1]
    cursor = db.cursor()
    # Execute an INSERT statement
    cursor.execute(
        """
    INSERT INTO dynastr.current_leagues 
    (session_id, user_id, user_name, league_id, league_name, avatar, total_rosters, qb_cnt, rb_cnt, wr_cnt, te_cnt, flex_cnt, sf_cnt, starter_cnt, total_roster_cnt, sport, insert_date, rf_cnt, league_cat, league_year, previous_league_id, league_status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (session_id, league_id) DO UPDATE 
    SET user_id = excluded.user_id,
  		user_name = excluded.user_name,
		league_id = excluded.league_id,
		league_name = excluded.league_name,
		avatar = excluded.avatar,
		total_rosters = excluded.total_rosters,
		qb_cnt = excluded.qb_cnt,
		rb_cnt = excluded.rb_cnt,
		wr_cnt = excluded.wr_cnt,
		te_cnt = excluded.te_cnt,
		flex_cnt = excluded.flex_cnt,
		sf_cnt = excluded.sf_cnt,
		starter_cnt = excluded.starter_cnt,
		total_roster_cnt = excluded.total_roster_cnt,
		sport = excluded.sport,
      	insert_date = excluded.insert_date,
        rf_cnt = excluded.rf_cnt,
        league_cat = excluded.league_cat,
        league_year = excluded.league_year,
        previous_league_id = excluded.previous_league_id,
        league_status = excluded.league_status;""",
        (
            session_id,
            user_id,
            user_name,
            league_data.league_id,
            league_single["name"],
            league_single["avatar"],
            league_single["total_rosters"],
            qbs,
            rbs,
            wrs,
            tes,
            flexes,
            super_flexes,
            starters,
            len(league_single["roster_positions"]),
            league_single["sport"],
            entry_time,
            rec_flexes,
            league_single["settings"]["type"],
            league_single["season"],
            league_single["previous_league_id"],
            league_single["status"],
        ),
    )

    # Commit the transaction
    db.commit()

    # Close the cursor and connection
    cursor.close()

    return
