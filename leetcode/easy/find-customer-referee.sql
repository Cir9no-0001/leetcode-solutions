-- Find Customer Referee
-- https://leetcode.com/problems/find-customer-referee
-- difficulty: easy
-- first_seen (EST): 2026-07-04 23:50:07
-- runtime: 455

# Write your MySQL query statement below
Select c.name
from Customer c
left join Customer b
on b.id=c.id
where c.referee_id!=2 or c.referee_id is null;