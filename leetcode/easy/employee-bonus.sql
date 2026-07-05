-- Employee Bonus
-- https://leetcode.com/problems/employee-bonus
-- synced: 2026-07-05 02:38:25 UTC

# Write your MySQL query statement below
Select e.name, b.bonus
from Employee e
left join Bonus b
on e.empId=b.empId
where b.bonus<1000 or b.bonus is NULL;