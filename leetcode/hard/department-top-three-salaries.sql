-- Department Top Three Salaries
-- https://leetcode.com/problems/department-top-three-salaries
-- difficulty: hard
-- first_seen: 2026-07-07 18:22:02 EDT
-- runtime: 929

-- NOTES START
-- write your notes here
-- NOTES END

with cte_rank as(
    select
    e.name as 'Employee',
    e.departmentId,
    e.salary as 'Salary',
    dense_rank() over (partition by e.departmentId order by e.salary desc) as 'ranking',
    d.name as 'Department'

    from Employee e
    inner join Department d
    on e.departmentId=d.id
)
select r.Department, r.Employee, r.Salary
from cte_rank r
where r.ranking<=3;
