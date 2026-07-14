-- Not Boring Movies
-- https://leetcode.com/problems/not-boring-movies
-- difficulty: easy
-- first_seen: 2026-07-08 04:30:18 EDT
-- runtime: 252ms
-- Notes:
--




Select *
from Cinema c
where c.description!='boring' and c.id%2=1
order by c.rating desc;