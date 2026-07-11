-- Game Play Analysis IV
-- https://leetcode.com/problems/game-play-analysis-iv
-- difficulty: medium
-- first_seen: 2026-07-09 21:20:34 EDT
-- runtime: 526ms
--
-- Notes stored in leetcode_notes.json

with initial as(
    select a.player_id, min(a.event_date) as first_log
    from Activity a
    group by a.player_id
)
select (
    round(
        sum(
            case 
            when datediff(a.event_date, i.first_log) = 1 then 1 
            else 0 
            end
        )
        /count(distinct a.player_id)
    , 2)) as fraction
from Activity a
inner join initial i
on a.player_id=i.player_id;
