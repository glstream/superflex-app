with sf_players as (select player_full_name
, p.team
, case when round(CAST(p.age AS float)) < 1 then Null else round(CAST(p.age AS float)) end as age
, superflex_sf_value as value
, superflex_sf_rank as rank
, CASE WHEN substring(lower(player_full_name) from 6 for 5) = 'round' THEN 'Pick' 
	   	WHEN _position = 'RDP' THEN 'Pick'
		ELSE _position END as _position
, 'superflex_sf_value' as roster_type 
, rank_type
,insert_date
from dynastr.sf_player_ranks sf
left join dynastr.players p on sf.player_full_name = p.full_name
UNION ALL
select player_full_name
,  p.team
, case when round(CAST(p.age AS float)) < 1 then Null else round(CAST(p.age AS float)) end as age
, superflex_one_qb_value as value
, superflex_one_qb_rank as rank
, CASE WHEN substring(lower(player_full_name) from 6 for 5) = 'round' THEN 'Pick' 
	   	WHEN _position = 'RDP' THEN 'Pick'
		ELSE _position END as _position
, 'superflex_one_qb_value' as roster_type
, rank_type
,insert_date
from dynastr.sf_player_ranks sf
left join dynastr.players p on sf.player_full_name = p.full_name)
															   
select player_full_name
,CONCAT(_position, ' ', rank() OVER (partition by roster_type, _position ORDER BY value DESC)) as pos_rank
, team
, age
, value as player_value
, rank as player_rank
, row_number() OVER (order by value desc) as _rownum
, _position
, case when roster_type = 'superflex_sf_value' then 'sf_value' 
	when roster_type = 'superflex_one_qb_value' then 'one_qb_value' end as roster_type
,	rank_type
, TO_DATE(insert_date, 'YYYY-mm-DDTH:M:SS.z')-1 as _insert_date
from sf_players
where 1=1
and player_full_name not like '%2023%'
and value > 0
order by value desc
									 
