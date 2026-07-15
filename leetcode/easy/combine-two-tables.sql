-- Combine Two Tables
-- https://leetcode.com/problems/combine-two-tables
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:08 EDT
-- runtime: 414ms

Select p.firstName, p.lastname, a.city, a.state
From Person p
left join Address a
on p.personId=a.personId;
