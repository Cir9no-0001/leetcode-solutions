-- Rising Temperature
-- https://leetcode.com/problems/rising-temperature
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:36:03 EDT
-- runtime: 515

Select w.id as Id
from Weather w
inner join Weather q
on DATEDIFF(w.recordDate, q.recordDate) = 1
where w.temperature>q.temperature;