-- Delete Duplicate Emails
-- https://leetcode.com/problems/delete-duplicate-emails
-- synced: 2026-07-05 02:38:26 UTC

# Write your MySQL query statement below
Delete d
from Person p
inner join Person d
    on p.email=d.email and p.id<d.id;
