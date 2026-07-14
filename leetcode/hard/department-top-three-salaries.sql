-- Department Top Three Salaries
-- https://leetcode.com/problems/department-top-three-salaries
-- difficulty: hard
-- first_seen: 2026-07-08 02:38:05 EDT
-- runtime: 929ms
--
-- Notes stored in leetcode_notes.json
-- Notes:
-- Hint: CTE + inner join + dense_rank with partition to rank

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
