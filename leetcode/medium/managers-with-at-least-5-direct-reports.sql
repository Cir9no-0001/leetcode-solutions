-- Managers with at Least 5 Direct Reports
-- https://leetcode.com/problems/managers-with-at-least-5-direct-reports
-- difficulty: medium
-- first_seen: 2026-07-09 05:18:24 EDT
-- runtime: 382
--
-- Notes stored in leetcode_notes.json

Select e.name
from Employee e
inner join Employee a
on e.id=a.managerId
group by e.id
having count(*)>=5;