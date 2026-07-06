-- Rank Scores
-- https://leetcode.com/problems/rank-scores
-- difficulty: medium
-- first_seen: 2026-07-05 20:53:53 EDT
-- runtime: 304

-- NOTES START
-- write your notes here
-- NOTES END

select s.score, dense_rank() over (order by s.score desc) as "rank"
from Scores s
order by s.score desc
