-- Big Countries
-- https://leetcode.com/problems/big-countries
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:01 EDT
-- runtime: 280
--
-- Notes stored in leetcode_notes.json

# Write your MySQL query statement below
Select w.name, w.population, w.area
from World w
where w.area>=3000000 or w.population>=25000000;