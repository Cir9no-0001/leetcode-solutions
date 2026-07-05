-- Rising Temperature
-- https://leetcode.com/problems/rising-temperature
-- difficulty: easy
-- first_seen (EST): 2026-07-04 23:50:08
-- runtime: 515

Select w.id as Id
from Weather w
inner join Weather q
on DATEDIFF(w.recordDate, q.recordDate) = 1
where w.temperature>q.temperature;