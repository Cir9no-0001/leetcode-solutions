-- Rising Temperature
-- https://leetcode.com/problems/rising-temperature
-- synced: 2026-07-05 02:38:26 UTC

Select w.id as Id
from Weather w
inner join Weather q
on DATEDIFF(w.recordDate, q.recordDate) = 1
where w.temperature>q.temperature;