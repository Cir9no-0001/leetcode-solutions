-- Confirmation Rate
-- https://leetcode.com/problems/confirmation-rate
-- difficulty: medium
-- first_seen: 2026-07-22 21:00:20 EDT
-- runtime: 690ms
-- Notes:
--


select 
    s.user_id,
    round(
        avg(if(c.action='confirmed', 1, 0))
    ,2) as 'confirmation_rate'
from Signups s
left join Confirmations c
on s.user_id=c.user_id
group by s.user_id