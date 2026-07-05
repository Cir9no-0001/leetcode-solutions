-- Delete Duplicate Emails
-- https://leetcode.com/problems/delete-duplicate-emails
-- difficulty: easy
-- runtime: 814ms

# Write your MySQL query statement below
Delete d
from Person p
inner join Person d
    on p.email=d.email and p.id<d.id;
