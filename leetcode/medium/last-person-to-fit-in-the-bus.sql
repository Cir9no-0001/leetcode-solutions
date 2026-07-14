-- Last Person to Fit in the Bus
-- https://leetcode.com/problems/last-person-to-fit-in-the-bus
-- difficulty: medium
-- first_seen: 2026-07-14 14:26:55 EDT
-- runtime: 756ms
--
-- Notes:
--

with temp as(
    select q.person_name, sum(q.weight) over (order by q.turn) as 'total_weight'
    from Queue q
)

select t.person_name
from temp t
where t.total_weight<=1000
order by t.total_weight desc
limit 1
