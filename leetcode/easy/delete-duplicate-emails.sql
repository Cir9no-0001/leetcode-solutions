-- Delete Duplicate Emails
-- https://leetcode.com/problems/delete-duplicate-emails
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:36:04 EDT
-- runtime: 814

# Write your MySQL query statement below
Delete d
from Person p
inner join Person d
    on p.email=d.email and p.id<d.id;
