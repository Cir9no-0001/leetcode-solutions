-- Big Countries
-- https://leetcode.com/problems/big-countries
-- difficulty: easy
-- first_seen (EST): 2026-07-04 23:50:07
-- runtime: 280

# Write your MySQL query statement below
Select w.name, w.population, w.area
from World w
where w.area>=3000000 or w.population>=25000000;