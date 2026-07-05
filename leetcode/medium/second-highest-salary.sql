-- Second Highest Salary
-- https://leetcode.com/problems/second-highest-salary
-- difficulty: medium
-- first_seen (EST): 2026-07-05 00:13:11
-- runtime: 248

Select(
    Select distinct(e.salary) 
    from Employee e
    order by e.salary desc
    limit 1 offset 1
)as SecondHighestSalary