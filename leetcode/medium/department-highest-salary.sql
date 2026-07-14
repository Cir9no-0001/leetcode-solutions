-- Department Highest Salary
-- https://leetcode.com/problems/department-highest-salary
-- difficulty: medium
-- first_seen: 2026-07-05 22:27:45 EDT
-- runtime: 600ms
-- Notes:
--


with Ranks as (
    select
        d.name as Department, 
        e.name as Employee, 
        e.salary as Salary,
        dense_rank() over (partition by e.departmentId order by e.salary desc) as salary_rank
    from Employee e 
    inner join Department d on d.id = e.departmentId
)
select Department, Employee, Salary
from Ranks
where salary_rank = 1;
