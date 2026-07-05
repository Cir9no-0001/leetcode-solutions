-- Employees Earning More Than Their Managers
-- https://leetcode.com/problems/employees-earning-more-than-their-managers
-- solved: 2026-07-05 01:15:26 UTC

SELECT 
    e.name AS Employee
FROM Employee e
inner JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;