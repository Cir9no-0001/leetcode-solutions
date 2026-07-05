-- Employees Earning More Than Their Managers
-- https://leetcode.com/problems/employees-earning-more-than-their-managers
-- difficulty: easy
-- runtime: 416

SELECT 
    e.name AS Employee
FROM Employee e
inner JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;