-- Big Countries
-- https://leetcode.com/problems/big-countries
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:19:06 EDT
-- runtime: 280

# Write your MySQL query statement below
Select w.name, w.population, w.area
from World w
where w.area>=3000000 or w.population>=25000000;