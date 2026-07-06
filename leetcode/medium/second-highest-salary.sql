-- Second Highest Salary
-- https://leetcode.com/problems/second-highest-salary
-- difficulty: medium
-- first_seen: 2026-07-05 20:40:00 EDT
-- runtime: 248

-- NOTES START
-- write your notes here
-- NOTES END

Select(
    Select distinct(e.salary) 
    from Employee e
    order by e.salary desc
    limit 1 offset 1
)as SecondHighestSalary