-- Employees Earning More Than Their Managers
-- https://leetcode.com/problems/employees-earning-more-than-their-managers
-- synced: 2026-07-05 02:38:28 UTC

SELECT 
    e.name AS Employee
FROM Employee e
inner JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;