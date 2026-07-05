-- Rising Temperature
-- https://leetcode.com/problems/rising-temperature
-- solved: 2026-07-05 01:15:25 UTC

Select w.id as Id
from Weather w
inner join Weather q
on DATEDIFF(w.recordDate, q.recordDate) = 1
where w.temperature>q.temperature;