-- Replace Employee ID With The Unique Identifier
-- https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier
-- difficulty: easy
-- first_seen: 2026-07-21 16:38:21 EDT
-- runtime: 1248ms
-- Notes:
--


select 
    eu.unique_id,
    e.name
from Employees e
left join EmployeeUNI eu
on e.id=eu.id