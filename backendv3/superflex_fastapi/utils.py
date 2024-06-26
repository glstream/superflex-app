import requests
from requests.exceptions import RequestException
from time import sleep
from psycopg2.extras import execute_batch, execute_values
from superflex_models import UserDataModel, LeagueDataModel, RosterDataModel
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
                print(f"Error while making API call: {e}. Retrying in {sleep_time} seconds...")
                sleep(sleep_time)
            else:
                print(f"Error while making API call: {e}. Reached maximum retries ({max_retries}).")
                raise


def dedupe(lst):
    dup_free_set = set()
    for x in lst:
        t = tuple(x)
        if t not in dup_free_set:
            dup_free_set.add(t)
    return list(dup_free_set)


def round_suffix(rank: int) -> str:
    ith = {1: "st", 2: "nd", 3: "rd"}.get(
        rank % 10 * (rank % 100 not in [11, 12, 13]), "th"
    )
    return f"{str(rank)}{ith}"


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


def clean_league_managers(db, league_id: str):
    delete_query = f"""DELETE FROM dynastr.managers where league_id = '{league_id}' """
    cursor = db.cursor()
    cursor.execute(delete_query)
    db.commit()
    cursor.close()
    return


def clean_league_rosters(db, session_id: str, user_id: str, league_id: str):
    delete_query = f"""DELETE FROM dynastr.league_players where session_id = '{session_id}' and league_id = '{league_id}'"""
    cursor = db.cursor()
    cursor.execute(delete_query)
    db.commit()
    cursor.close()
    return


def clean_league_picks(db, league_id: str, session_id: str) -> None:
    delete_query = f"""DELETE FROM dynastr.draft_picks where league_id = '{league_id}' and session_id = '{session_id}'"""
    cursor = db.cursor()
    cursor.execute(delete_query)
    cursor.close()
    return


def clean_draft_positions(db, league_id: str):
    delete_query = (
        f"""DELETE FROM dynastr.draft_positions where league_id = '{league_id}'"""
    )
    cursor = db.cursor()
    cursor.execute(delete_query)
    cursor.close()
    return


def get_managers(league_id: str) -> list:
    res = make_api_call(f"https://api.sleeper.app/v1/league/{league_id}/users")
    manager_data = [
        ["sleeper", i["user_id"], league_id, i["avatar"], i["display_name"]]
        for i in res
    ]
    return manager_data


def get_league_rosters_size(league_id: str) -> int:
    league_res = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_id}")
    return league_res["total_rosters"]


def get_league_rosters(league_id: str) -> list:
    rosters = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_id}/rosters")
    return rosters


def get_traded_picks(league_id: str) -> list:
    total_res = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_id}/traded_picks"
    )
    return total_res


def get_draft_id(league_id: str) -> str:
    draft_res = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_id}/drafts")
    draft_meta = draft_res[0]
    return draft_meta


def get_draft(draft_id: str):
    draft_res = make_api_call(f"https://api.sleeper.app/v1/draft/{draft_id}")
    return draft_res


def get_roster_ids(league_id: str) -> list:
    roster_meta = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    )
    return [(r["owner_id"], str(r["roster_id"])) for r in roster_meta]


def get_full_league(league_id: str):
    l_res = make_api_call(
        f"https://api.sleeper.app/v1/league/{league_id}/rosters")
    return l_res


def insert_current_leagues(db, user_data: UserDataModel):
    user_name = user_data.user_name
    league_year = user_data.league_year
    leagues = get_user_leagues(user_name, league_year)
    session_id = user_data.guid
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
    print('executing')
    user_id = "342397313982976000"
    entry_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    session_id = 'cc73437c-40b6-4cd4-9835-6b41033968c4'
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


def insert_managers(db, managers: list):
    with db.cursor() as cursor:
        execute_values(
            cursor,
            """
                INSERT INTO dynastr.managers VALUES %s
                ON CONFLICT (user_id)
                DO UPDATE SET source = EXCLUDED.source
	                        , league_id = EXCLUDED.league_id
                            , avatar = EXCLUDED.avatar
                            , display_name = EXCLUDED.display_name;
                """,
            [
                (manager[0], manager[1], manager[2], manager[3], manager[4])
                for manager in iter(managers)
            ],
            page_size=1500,
        )
    return


def insert_league_rosters(db, session_id: str, user_id: str, league_id: str) -> None:
    league_players = []
    entry_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    rosters = get_league_rosters(league_id)

    for roster in rosters:
        league_roster = roster["players"]
        try:
            for player_id in league_roster:
                league_players.append(
                    [
                        session_id,
                        user_id,
                        player_id,
                        roster["league_id"],
                        roster["owner_id"]
                        if roster["owner_id"] is not None
                        else "EMPTY",
                        entry_time,
                    ]
                )
        except:
            league_players = []

    with db.cursor() as cursor:
        execute_values(
            cursor,
            """
                 INSERT INTO dynastr.league_players VALUES %s
                ON CONFLICT (session_id, user_id, player_id, league_id)
                DO UPDATE SET insert_date = EXCLUDED.insert_date;
                """,
            [
                (
                    league_player[0],
                    league_player[1],
                    league_player[2],
                    league_player[3],
                    league_player[4],
                    league_player[5],
                )
                for league_player in iter(league_players)
            ],
            page_size=1500,
        )

    return


def total_owned_picks(
    db,
    league_id: str,
    session_id,
    startup,
    base_picks: dict = {},
    traded_picks_all: dict = {},
) -> None:
    if startup is not None:
        base_picks = {}
        traded_picks_all = {}
        league_size = get_league_rosters_size(league_id)
        total_picks = get_traded_picks(league_id)
        draft_id = get_draft_id(league_id)
        years = (
            [str(int(draft_id["season"]) + i) for i in range(1, 4)]
            if draft_id["status"] == "complete"
            else [str(int(draft_id["season"]) + i) for i in range(0, 3)]
        )
        rd = (
            draft_id["settings"]["rounds"]
            if int(draft_id["settings"]["rounds"]) <= 4
            else 4
        )
        rounds = [r for r in range(1, rd + 1)]

        traded_picks = [
            [pick["season"], pick["round"], pick["roster_id"], pick["owner_id"]]
            for pick in total_picks
            if pick["roster_id"] != pick["owner_id"] and pick["season"] in years
        ]

        for year in years:
            base_picks[year] = {
                round: [[i, i] for i in range(1, league_size + 1)] for round in rounds
            }
            for pick in traded_picks:
                traded_picks_all[year] = {
                    round: [
                        [i[2], i[3]]
                        for i in [
                            i for i in traded_picks if i[0] == year and i[1] == round
                        ]
                    ]
                    for round in rounds
                }
        for year, traded_rounds in traded_picks_all.items():
            for round, picks in traded_rounds.items():
                for pick in picks:
                    if [pick[0], pick[0]] in base_picks[year][round]:
                        base_picks[year][round].remove([pick[0], pick[0]])
                        base_picks[year][round].append(pick)

        for year, round in base_picks.items():
            for round, picks in round.items():
                draft_picks = [
                    [
                        year,
                        round,
                        round_suffix(round),
                        pick[0],
                        pick[1],
                        league_id,
                        draft_id["draft_id"],
                        session_id,
                    ]
                    for pick in picks
                ]

                with db.cursor() as cursor:
                    execute_values(
                        cursor,
                        """
                        INSERT INTO dynastr.draft_picks VALUES %s
                        ON CONFLICT (year, round, roster_id, owner_id, league_id, session_id)
                        DO UPDATE SET round_name = EXCLUDED.round_name
                                    , draft_id = EXCLUDED.draft_id;
                        """,
                        [
                            (
                                draft_pick[0],
                                draft_pick[1],
                                draft_pick[2],
                                draft_pick[3],
                                draft_pick[4],
                                draft_pick[5],
                                draft_pick[6],
                                draft_pick[7],
                            )
                            for draft_pick in iter(draft_picks)
                        ],
                        page_size=1500,
                    )
    return


def draft_positions(db, league_id: str, user_id: str, draft_order: list = []) -> None:
    draft_id = get_draft_id(league_id)
    draft = get_draft(draft_id["draft_id"])

    draft_order = []
    draft_dict = draft["draft_order"]
    draft_slot = {k: v for k,
                  v in draft["slot_to_roster_id"].items() if v is not None}
    season = draft["season"]
    rounds = (
        draft_id["settings"]["rounds"]
        if int(draft_id["settings"]["rounds"]) <= 4
        else "4"
    )
    roster_slot = {int(k): v for k, v in draft_slot.items() if v is not None}
    rs_dict = dict(sorted(roster_slot.items(), key=lambda item: int(item[0])))
    if draft_dict is None:
        # if no draft is present then create all managers at mid level for picks
        participents = get_roster_ids(league_id)

        for pos in range(len(rs_dict.items())):
            position_name = "Mid"
            draft_set = "N"
            draft_order.append(
                [
                    season,
                    rounds,
                    pos,
                    position_name,
                    participents[pos][1],  # roster_id
                    participents[pos][0],  # user_id
                    league_id,
                    draft_id["draft_id"],
                    draft_set,
                ]
            )
    else:
        if len(draft.get("draft_order", 0)) < len(draft["slot_to_roster_id"]):
            league = get_league_rosters(league_id)
            empty_team_cnt = 0
            for k, v in draft_slot.items():
                if int(k) not in list(draft.get("draft_order", {}).values()):
                    if league[v - 1]["owner_id"] is not None:
                        draft_dict[league[v - 1]["owner_id"]] = int(k)
                    else:
                        empty_alias = f"Empty_Team{empty_team_cnt}"
                        draft_dict[empty_alias] = v
                        empty_team_cnt += 1

        draft_order_dict = dict(
            sorted(draft_dict.items(), key=lambda item: item[1]))
        draft_order_ = dict([(value, key)
                            for key, value in draft_order_dict.items()])

        for draft_position, roster_id in rs_dict.items():
            draft_set = "Y"
            if draft_position <= 4:
                position_name = "Early"
            elif draft_position <= 8:
                position_name = "Mid"
            else:
                position_name = "Late"
            if int(draft_position) in [
                int(draft_position)
                for user_id, draft_position in draft_order_dict.items()
            ]:
                draft_order.append(
                    [
                        season,
                        rounds,
                        draft_position,
                        position_name,
                        roster_id,
                        draft_order_[int(draft_position)],
                        # draft_order_.get(int(draft_position), "Empty"),
                        league_id,
                        draft_id["draft_id"],
                        draft_set,
                    ]
                )

    cursor = db.cursor()
    execute_batch(
        cursor,
        """INSERT into dynastr.draft_positions (season, rounds,  position, position_name, roster_id, user_id, league_id, draft_id, draft_set_flg)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (season, rounds, position, user_id, league_id)
    DO UPDATE SET position_name = EXCLUDED.position_name
            , roster_id = EXCLUDED.roster_id
            , draft_id = EXCLUDED.draft_id
            , draft_set_flg = EXCLUDED.draft_set_flg
    ;""",
        tuple(draft_order),
        page_size=1500,
    )
    db.commit()
    cursor.close()
    return


def clean_player_trades(db, league_id: str) -> None:
    delete_query = (
        f"""DELETE FROM dynastr.player_trades where league_id = '{league_id}'"""
    )
    cursor = db.cursor()
    cursor.execute(delete_query)
    db.commit()
    return


def clean_draft_trades(db, league_id: str) -> None:
    delete_query = (
        f"""DELETE FROM dynastr.draft_pick_trades where league_id = '{league_id}'"""
    )
    cursor = db.cursor()
    cursor.execute(delete_query)
    db.commit()
    return


def get_trades(league_id: str, nfl_state: dict, year_entered: str) -> list:
    leg = nfl_state["leg"] if nfl_state["leg"] > 0 else 1
    all_trades = []
    if nfl_state["season_type"] != "off":
        leg = nfl_state["leg"] if nfl_state["leg"] > 0 else 1
        for week in range(1, leg + 1):
            transactions = make_api_call(
                f"https://api.sleeper.app/v1/league/{league_id}/transactions/{week}"
            )
            all_trades.extend(transactions)
            # week += 1
        trades_payload = [p for p in [
            i for i in all_trades] if p["type"] == "trade"]
    elif year_entered != nfl_state["season"]:
        for week in range(1, 18):
            transactions = make_api_call(
                f"https://api.sleeper.app/v1/league/{league_id}/transactions/{week}"
            )
            all_trades.extend(transactions)
            week += 1
            trades_payload = [
                p for p in [i for i in all_trades] if p["type"] == "trade"
            ]
    else:
        transactions = make_api_call(
            f"https://api.sleeper.app/v1/league/{league_id}/transactions/1"
        )
        all_trades.extend(transactions)
        trades_payload = [p for p in [
            i for i in all_trades] if p["type"] == "trade"]

    return trades_payload


def get_sleeper_state() -> str:
    state = make_api_call("https://api.sleeper.app/v1/state/nfl")
    return state


def insert_trades(db, trades: dict, league_id: str) -> None:
    player_adds_db = []
    player_drops_db = []
    draft_adds_db = []
    draft_drops_db = []

    for trade in trades:
        for roster_id in trade["roster_ids"]:
            player_adds = trade["adds"] if trade["adds"] else {}
            player_drops = trade["drops"] if trade["drops"] else {}
            draft_picks = trade["draft_picks"] if trade["draft_picks"] else [
                {}]

            for a_player_id, a_id in [
                [k, v] for k, v in player_adds.items() if v == roster_id
            ]:
                player_adds_db.append(
                    [
                        trade["transaction_id"],
                        trade["status_updated"],
                        a_id,
                        "add",
                        a_player_id,
                        league_id,
                    ]
                )
            for d_player_id, d_id in [
                [k, v] for k, v in player_drops.items() if v == roster_id
            ]:

                player_drops_db.append(
                    [
                        trade["transaction_id"],
                        trade["status_updated"],
                        d_id,
                        "drop",
                        d_player_id,
                        league_id,
                    ]
                )

            for pick in draft_picks:
                draft_picks_ = [v for k, v in pick.items()]

                if draft_picks_:
                    suffix = round_suffix(draft_picks_[1])
                    draft_adds_db.append(
                        [
                            trade["transaction_id"],
                            trade["status_updated"],
                            draft_picks_[4],
                            "add",
                            draft_picks_[0],
                            draft_picks_[1],
                            suffix,
                            draft_picks_[2],
                            league_id,
                        ]
                    )
                    draft_drops_db.append(
                        [
                            trade["transaction_id"],
                            trade["status_updated"],
                            draft_picks_[3],
                            "drop",
                            draft_picks_[0],
                            draft_picks_[1],
                            suffix,
                            draft_picks_[2],
                            league_id,
                        ]
                    )

    draft_adds_db = dedupe(draft_adds_db)
    player_adds_db = dedupe(player_adds_db)
    player_drops_db = dedupe(player_drops_db)
    draft_drops_db = dedupe(draft_drops_db)

    cursor = db.cursor()
    execute_batch(
        cursor,
        """INSERT INTO dynastr.draft_pick_trades (transaction_id, status_updated, roster_id, transaction_type, season, round, round_suffix, org_owner_id, league_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
    """,
        tuple(draft_adds_db),
        page_size=1500,
    )
    execute_batch(
        cursor,
        """INSERT INTO dynastr.draft_pick_trades (transaction_id, status_updated, roster_id, transaction_type, season, round, round_suffix, org_owner_id, league_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)  
    """,
        tuple(draft_drops_db),
        page_size=1500,
    )
    execute_batch(
        cursor,
        """INSERT INTO dynastr.player_trades (transaction_id, status_updated, roster_id, transaction_type, player_id, league_id)
    VALUES (%s, %s, %s, %s, %s, %s) 
    """,
        tuple(player_adds_db),
        page_size=1500,
    )
    execute_batch(
        cursor,
        """INSERT INTO dynastr.player_trades (transaction_id, status_updated, roster_id, transaction_type, player_id, league_id)
    VALUES (%s, %s, %s, %s, %s, %s) 
    """,
        tuple(player_drops_db),
        page_size=1500,
    )
    db.commit()
    cursor.close()
    return


def player_manager_rosters(
    db,
    roster_data: RosterDataModel
):
    session_id = roster_data.guid
    user_id = roster_data.user_id
    league_id = roster_data.league_id
    year_entered = roster_data.league_year
    startup = False
    try:
        clean_league_managers(db, league_id)
        clean_league_rosters(db, session_id, user_id, league_id)
        clean_league_picks(db, league_id, session_id)
        clean_draft_positions(db, league_id)

        managers = get_managers(league_id)
        insert_managers(db, managers)

        insert_league_rosters(db, session_id, user_id, league_id)
        total_owned_picks(db, league_id, session_id, startup)
        draft_positions(db, league_id, user_id)

        # delete traded players and picks
        clean_player_trades(db, league_id)
        clean_draft_trades(db, league_id)
        # get trades
        trades = get_trades(league_id, get_sleeper_state(), year_entered)
        # insert trades draft Positions
        insert_trades(db, trades, league_id)
    except Exception as e:
        print('issue', e)
        return e
