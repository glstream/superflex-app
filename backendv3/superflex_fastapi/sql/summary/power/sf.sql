SELECT
                    t3.user_id
                    , t3.display_name
                    , t3.avatar
                    , total_value
                    , ROW_NUMBER() OVER (order by sum(position_value) desc) total_rank 
                    , NTILE(10) OVER (order by total_value desc) total_tile
                    , max(qb_value) as qb_value
                    , max(qb_starter_value) as qb_starter_value
                    , RANK() OVER (order by sum(qb_value) desc) qb_rank
                    , RANK() OVER (order by sum(qb_starter_value) desc) qb_starter_rank
                    , NTILE(10) OVER (order by sum(qb_value) desc) qb_tile
                    , sum(qb_value) as qb_sum
                    , sum(qb_starter_value) as qb_starter_sum
                    , coalesce(round(sum(qb_value) / NULLIF(sum(qb_count), 0),0), 0) as qb_average
                    , sum(qb_count) as qb_count
                    , max(rb_value) as rb_value
                    , max(rb_starter_value) as rb_starter_value
                    , RANK() OVER (order by sum(rb_value) desc) rb_rank
                    , RANK() OVER (order by sum(rb_starter_value) desc) rb_starter_rank
                    , NTILE(10) OVER (order by sum(rb_value) desc) rb_tile
                    , sum(rb_value) as rb_sum
                    , sum(rb_starter_value) as rb_starter_sum
                    , coalesce(round(sum(rb_value) / NULLIF(sum(rb_count), 0),0), 0) as rb_average
                    , sum(rb_count) as rb_count
                    , max(wr_value) as wr_value
                    , max(wr_starter_value) as wr_starter_value
                    , RANK() OVER (order by sum(wr_value) desc) wr_rank
                    , RANK() OVER (order by sum(wr_starter_value) desc) wr_starter_rank
                    , NTILE(10) OVER (order by sum(wr_value) desc) wr_tile
                    , sum(wr_value) as wr_sum
                    , sum(wr_starter_value) as wr_starter_sum
                    , coalesce(round(sum(wr_value) / NULLIF(sum(wr_count), 0),0), 0) as wr_average
                    , sum(wr_count) as wr_count
                    , max(te_value) as te_value
                    , max(te_starter_value) as te_starter_value
                    , RANK() OVER (order by sum(te_value) desc) te_rank
                    , RANK() OVER (order by sum(te_starter_value) desc) te_starter_rank
                    , NTILE(10) OVER (order by sum(te_value) desc) te_tile
                    , sum(te_value) as te_sum
                    , sum(te_starter_value) as te_starter_sum
                    , coalesce(round(sum(te_value) / NULLIF(sum(te_count), 0),0), 0) as te_average
                    , sum(te_count) as wr_count
                    , max(picks_value) as picks_value
                    , RANK() OVER (order by sum(picks_value) desc) picks_rank
                    , NTILE(10) OVER (order by sum(picks_value) desc) picks_tile
                    , sum(picks_value) as picks_sum
                    , max(flex_value) as flex_value
                    , RANK() OVER (order by sum(flex_value) desc) flex_rank
                    , max(super_flex_value) as super_flex_value
                    , RANK() OVER (order by sum(super_flex_value) desc) super_flex_rank
                    , max(starters_value) as starters_value
                    , RANK() OVER (order by sum(starters_value) desc) starters_rank
                    , NTILE(10) OVER (order by sum(starters_value) desc) starters_tile
                    , sum(starters_value) as starters_sum
                    , coalesce(round(sum(starters_value) / NULLIF(sum(starters_count), 0),0), 0) as starters_average
                    , sum(starters_count) as starters_count
                    , max(Bench_value) as Bench_value
                    , RANK() OVER (order by sum(bench_value) desc) bench_rank
                    , NTILE(10) OVER (order by sum(bench_value) desc) bench_tile
                    , sum(bench_value) as bench_sum
                    , coalesce(round(sum(bench_value) / NULLIF(sum(bench_count), 0),0), 0) as bench_average
                    , sum(bench_count) as bench_count


                    from (select
                        user_id
                        , display_name
                        , avatar
                        , sum(player_value) as position_value
                        , total_value
                        , DENSE_RANK() OVER (PARTITION BY fantasy_position  order by sum(player_value) desc) as position_rank
                        , DENSE_RANK() OVER (order by total_value desc) as total_rank                        
                        , fantasy_position
                        , case when player_position = 'QB' THEN sum(player_value) else 0 end as qb_value
                        , case when player_position = 'QB' AND fantasy_designation = 'STARTER' THEN sum(player_value) else 0 end as qb_starter_value
                        , case when player_position = 'QB' THEN count(full_name) else 0 end as qb_count
                        , case when player_position = 'RB' THEN sum(player_value) else 0 end as rb_value
                        , case when player_position = 'RB' AND fantasy_designation = 'STARTER' THEN sum(player_value) else 0 end as rb_starter_value
                        , case when player_position = 'RB' THEN count(full_name) else 0 end as rb_count
                        , case when player_position = 'WR' THEN sum(player_value) else 0 end as wr_value
                        , case when player_position = 'WR' AND fantasy_designation = 'STARTER' THEN sum(player_value) else 0 end as wr_starter_value
                        , case when player_position = 'WR' THEN count(full_name) else 0 end as wr_count
                        , case when player_position = 'TE' THEN sum(player_value) else 0 end as te_value
                        , case when player_position = 'TE' AND fantasy_designation = 'STARTER' THEN sum(player_value) else 0 end as te_starter_value
                        , case when player_position = 'TE' THEN count(full_name) else 0 end as te_count
                        , case when player_position = 'PICKS' THEN sum(player_value) else 0 end as picks_value
                        , case when fantasy_position = 'FLEX' THEN sum(player_value) else 0 end as flex_value
                        , case when fantasy_position = 'SUPER_FLEX' THEN sum(player_value) else 0 end as super_flex_value
                        , case when fantasy_designation = 'STARTER' THEN sum(player_value) else 0 end as starters_value
                        , case when fantasy_designation = 'STARTER' THEN count(full_name) else 0 end as starters_count
                        , case when fantasy_designation = 'BENCH' THEN sum(player_value) else 0 end as bench_value
                        , case when fantasy_designation = 'BENCH' THEN count(full_name) else 0 end as bench_count
                        from (SELECT
                        asset.user_id
                        , asset.display_name
                        , asset.avatar
                        , asset.full_name
                        , asset.player_position
                        , asset.fantasy_position
                        , asset.fantasy_designation
                        , asset.team
                        , asset.player_value  
                        , sum(asset.player_value) OVER (PARTITION BY asset.user_id) as total_value    
                        from      
                        (
                        WITH base_players as (SELECT
                    lp.user_id
                    , lp.league_id
                    , lp.session_id
                    , pl.full_name 
                    , pl.player_id
                    , sf.ktc_player_id
                    , pl.player_position
                    , coalesce(sf.league_type, -1) as player_value
                    , RANK() OVER (PARTITION BY lp.user_id, pl.player_position ORDER BY coalesce(sf.league_type, -1) desc) as player_order
                    , qb_cnt
                    , rb_cnt
                    , wr_cnt
                    , te_cnt
                    , flex_cnt
                    , sf_cnt
                    , rf_cnt

                    from dynastr.league_players lp
                    inner join dynastr.players pl on lp.player_id = pl.player_id
                    LEFT JOIN dynastr.sf_player_ranks sf on sf.player_full_name  = pl.full_name
                    inner join dynastr.current_leagues cl on lp.league_id = cl.league_id and cl.session_id = 'session_id' 
                    where lp.session_id = 'session_id'
                    and lp.league_id = 'league_id'
                    and pl.player_position IN ('QB', 'RB', 'WR', 'TE' )
                    and sf.rank_type = 'rank_type'
                    )

                    , base_picks as (select t1.user_id
                                , t1.season
                                , t1.year
                                , t1.player_full_name
                                , sf.ktc_player_id
                                FROM (
                                    SELECT  
                                    al.user_id
                                    , al.season
                                    , al.year 
                                    , CASE WHEN (dname.position::integer) < 13 and al.draft_set_flg = 'Y' and al.year = dname.season
                                                THEN al.year || ' Round ' || al.round || ' Pick ' || dname.position
                                            WHEN (dname.position::integer) > 12 and al.draft_set_flg = 'Y' and al.year = dname.season
                                                THEN al.year || ' ' || dname.position_name || ' ' || al.round_name 
                                            ELSE al.year|| ' Mid ' || al.round_name 
                                            END AS player_full_name 
                                    FROM (                           
                                        SELECT dp.roster_id
                                        , dp.year
                                        , dp.round_name
                                        , dp.round
                                        , dp.league_id
                                        , dpos.user_id
                                        , dpos.season
                                        , dpos.draft_set_flg
                                        FROM dynastr.draft_picks dp
                                        inner join dynastr.draft_positions dpos on dp.owner_id = dpos.roster_id and dp.league_id = dpos.league_id

                                        where dpos.league_id = 'league_id'
                                        and dp.session_id = 'session_id'
                                        ) al 
                                    inner join dynastr.draft_positions dname on  dname.roster_id = al.roster_id and al.league_id = dname.league_id
                                ) t1
                                LEFT join dynastr.sf_player_ranks sf on t1.player_full_name = sf.player_full_name
                                where 1=1
                                and sf.rank_type = 'rank_type'
                                    )              
                    , starters as (SELECT  
                    qb.user_id
                    , qb.player_id
                    , qb.ktc_player_id
                    , qb.player_position
                    , qb.player_position as fantasy_position
                    , qb.player_order
                    from base_players qb
                    where 1=1
                    and qb.player_position = 'QB'
                    and qb.player_order <= qb.qb_cnt
                    UNION ALL
                    select 
                    rb.user_id
                    , rb.player_id
                    , rb.ktc_player_id
                    , rb.player_position
                    , rb.player_position as fantasy_position
                    , rb.player_order
                    from base_players rb
                    where 1=1
                    and rb.player_position = 'RB'
                    and rb.player_order <= rb.rb_cnt
                    UNION ALL
                    select 
                    wr.user_id
                    , wr.player_id
                    , wr.ktc_player_id
                    , wr.player_position
                    , wr.player_position as fantasy_position
                    , wr.player_order
                    from base_players wr
                    where wr.player_position = 'WR'
                    and wr.player_order <= wr.wr_cnt

                    UNION ALL
                    select 
                    te.user_id
                    , te.player_id
                    , te.ktc_player_id
                    , te.player_position
                    , te.player_position as fantasy_position
                    , te.player_order
                    from  
                    base_players te
                    where te.player_position = 'TE'
                    and te.player_order <= te.te_cnt
                    )

                    , flex as (
                    SELECT
                    ns.user_id
                    , ns.player_id
                    , ns.ktc_player_id
                    , ns.player_position
                    , 'FLEX' as fantasy_position
                    , ns.player_order
                    from (
                    SELECT
                    fp.user_id
                    , fp.ktc_player_id
                    , fp.player_id
                    , fp.player_position
                    , RANK() OVER (PARTITION BY fp.user_id ORDER BY fp.player_value desc) as player_order
                    , fp.flex_cnt
                    from base_players fp
                    left join starters s on s.ktc_player_id = fp.ktc_player_id
                    where 1=1
                    and s.ktc_player_id IS NULL
                    and fp.player_position IN ('RB','WR','TE')  
                    order by player_order) ns
                    where player_order <= ns.flex_cnt)

                    ,super_flex as (
                    SELECT
                    ns_sf.user_id
                    , ns_sf.player_id
                    , ns_sf.ktc_player_id
                    , ns_sf.player_position
                    , 'SUPER_FLEX' as fantasy_position
                    , ns_sf.player_order
                    from (
                    SELECT
                    fp.user_id
                    , fp.ktc_player_id
                    , fp.player_id
                    , fp.player_position
                    , RANK() OVER (PARTITION BY fp.user_id ORDER BY fp.player_value desc) as player_order
                    , fp.sf_cnt
                    from base_players fp
                    left join (select * from starters UNION ALL select * from flex) s on s.ktc_player_id = fp.ktc_player_id
                    where s.ktc_player_id IS NULL
                    and fp.player_position IN ('QB','RB','WR','TE')  
                    order by player_order) ns_sf
                    where player_order <= ns_sf.sf_cnt)

                    ,rec_flex as (
                    SELECT
                    ns_rf.user_id
                    , ns_rf.player_id
                    , ns_rf.ktc_player_id
                    , ns_rf.player_position
                    , 'REC_FLEX' as fantasy_position
                    , ns_rf.player_order
                    from (
                    SELECT
                    fp.user_id
                    , fp.ktc_player_id
                    , fp.player_id
                    , fp.player_position
                    , ROW_NUMBER() OVER (PARTITION BY fp.user_id ORDER BY fp.player_value desc) as player_order
                    , rf_cnt
                    from base_players fp
                    left join (select * from starters UNION ALL select * from flex) s on s.ktc_player_id = fp.ktc_player_id
                    where s.ktc_player_id IS NULL
                    and fp.player_position IN ('WR','TE')  
                    order by player_order) ns_rf
                    where player_order <= ns_rf.rf_cnt)

                    , all_starters as (select 
                    user_id
                    ,ap.player_id
                    ,ap.ktc_player_id
                    ,ap.player_position 
                    ,ap.fantasy_position
                    ,'STARTER' as fantasy_designation
                    ,ap.player_order
                    from (select * from starters UNION ALL select * from flex UNION ALL select * from super_flex UNION ALL select * from rec_flex) ap
                    order by user_id, player_position desc)
                                            
                    select tp.user_id
                    ,m.display_name
                    ,m.avatar
                    ,sf.player_full_name as full_name
                    ,p.team
                    ,tp.player_id as player_id
                    ,tp.player_position
                    ,tp.fantasy_position
                    ,tp.fantasy_designation
                    ,coalesce(sf.league_type, -1) as player_value
                    from (select 
                            user_id
                            ,ap.player_id
                            ,ap.ktc_player_id
                            ,ap.player_position 
                            ,ap.fantasy_position
                            ,'STARTER' as fantasy_designation
                            ,ap.player_order 
                            , null as league_id
                            from all_starters ap
                            UNION
                            select 
                            bp.user_id
                            ,bp.player_id
                            ,bp.ktc_player_id
                            ,bp.player_position 
                            ,bp.player_position as fantasy_position
                            ,'BENCH' as fantasy_designation
                            ,bp.player_order
                            , bp.league_id
                            from base_players bp where bp.player_id not in (select player_id from all_starters)
                            UNION ALL
                            select 
                            user_id
                            ,null as player_id
                            ,picks.ktc_player_id
                            ,'PICKS' as player_position 
                            ,'PICKS' as fantasy_position
                            ,'PICKS' as fantasy_designation
                            , null as player_order
                            , null as league_id
                            from base_picks picks
                            ) tp
                    left join dynastr.players p on tp.player_id = p.player_id
                    inner JOIN dynastr.sf_player_ranks sf on tp.ktc_player_id = sf.ktc_player_id
                    inner join dynastr.managers m on tp.user_id = m.user_id 
                    where 1=1
                    and sf.rank_type = 'rank_type'
                    order by m.display_name, m.avatar, player_value desc
                    ) asset  
                            ) t2
                            GROUP BY
                             t2.user_id
                            , t2.display_name
                            , t2.avatar
                            , t2.total_value
                            , t2.fantasy_position
                            , t2.player_position
                            , t2.fantasy_designation) t3  
                                GROUP BY
                                    t3.user_id
                                    , t3.display_name
                                    , t3.avatar
                                    , t3.total_value
                                    , total_rank
                                ORDER BY                                                        
                                total_value desc