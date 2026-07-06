-- Find Customer Referee
-- https://leetcode.com/problems/find-customer-referee
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:19:08 EDT
-- runtime: 455

# Write your MySQL query statement below
Select c.name
from Customer c
left join Customer b
on b.id=c.id
where c.referee_id!=2 or c.referee_id is null;