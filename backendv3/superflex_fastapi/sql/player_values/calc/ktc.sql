select player_full_name
,  case when team = 'KCC' then 'KC' else team end as team
, case when round(CAST(age AS float)) < 1 then Null else round(CAST(age AS float)) end as age
, CASE WHEN substring(lower(player_full_name) from 6 for 5) = 'round' THEN 'Pick' 
	   	WHEN position = 'RDP' THEN 'Pick'
		ELSE position END as _position
, sf_value 
, sf_rank 
, one_qb_value
, rank as one_qb_rank
,insert_date
from dynastr.ktc_player_ranks
where 1=1
and player_full_name not like '%2023%'
and (sf_value > 0 OR one_qb_value > 0)					 
order by sf_value desc