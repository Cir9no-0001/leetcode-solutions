-- Count Salary Categories
-- https://leetcode.com/problems/count-salary-categories
-- difficulty: medium
-- first_seen: 2026-07-18 15:01:07 EDT
-- runtime: 1465ms
-- Notes:
--


select 'High Salary' as 'category', sum(if(a.income>50000, 1, 0)) as 'accounts_count'
from Accounts a

union

select 'Average Salary' as 'category', sum(if(a.income<=50000 and a.income>=20000, 1, 0)) as 'accounts_count'
from Accounts a

union

select 'Low Salary' as 'category', sum(if(a.income<20000, 1, 0)) as 'accounts_count'
from Accounts a