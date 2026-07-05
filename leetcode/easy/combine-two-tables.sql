-- Combine Two Tables
-- https://leetcode.com/problems/combine-two-tables
-- synced: 2026-07-05 01:19:16 UTC

# Write your MySQL query statement below
Select p.firstName, p.lastname, a.city, a.state
From Person p
left join Address a
on p.personId=a.personId;
