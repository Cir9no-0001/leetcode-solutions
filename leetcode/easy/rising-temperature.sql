-- Rising Temperature
-- https://leetcode.com/problems/rising-temperature
-- difficulty: easy
-- runtime: 515

Select w.id as Id
from Weather w
inner join Weather q
on DATEDIFF(w.recordDate, q.recordDate) = 1
where w.temperature>q.temperature;