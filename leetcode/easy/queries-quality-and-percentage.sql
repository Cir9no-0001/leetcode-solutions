-- Queries Quality and Percentage
-- https://leetcode.com/problems/queries-quality-and-percentage
-- difficulty: easy
-- first_seen: 2026-07-16 23:54:21 EDT
-- runtime: 380ms
-- Notes:
--


select
    q.query_name,
    round(
        avg(q.rating/q.position)
    ,2) as 'quality',
    round(
        sum(q.rating < 3)*100/count(q.rating)
    ,2) as 'poor_query_percentage'
from queries q
group by q.query_name