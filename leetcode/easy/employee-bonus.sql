-- Employee Bonus
-- https://leetcode.com/problems/employee-bonus
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:03 EDT
-- runtime: 919

-- NOTES START
-- write your notes here
-- NOTES END

# Write your MySQL query statement below
Select e.name, b.bonus
from Employee e
left join Bonus b
on e.empId=b.empId
where b.bonus<1000 or b.bonus is NULL;