-- Duplicate Emails
-- https://leetcode.com/problems/duplicate-emails
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:36:04 EDT
-- runtime: 383

# Write your MySQL query statement below
Select p.email as Email
from Person p
inner join (
    select email, id
    from Person
    group by email
    having count(*)>1
) a on p.id=a.id
