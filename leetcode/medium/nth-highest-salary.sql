-- Nth Highest Salary
-- https://leetcode.com/problems/nth-highest-salary
-- difficulty: medium
-- first_seen: 2026-07-05 20:39:59 EDT
-- runtime: 437

CREATE FUNCTION getNthHighestSalary(N INT) 
RETURNS INT
deterministic
BEGIN
    declare M INT;
    set M=N-1;

    RETURN (
        select distinct(salary)
        from Employee 
        order by salary desc
        limit 1 offset M
    );
END