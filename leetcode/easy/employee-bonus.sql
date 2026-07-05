-- Employee Bonus
-- https://leetcode.com/problems/employee-bonus
-- difficulty: easy
-- first_seen (EST): 2026-07-04 23:50:08
-- runtime: 919

# Write your MySQL query statement below
Select e.name, b.bonus
from Employee e
left join Bonus b
on e.empId=b.empId
where b.bonus<1000 or b.bonus is NULL;