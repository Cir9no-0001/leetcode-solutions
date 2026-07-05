-- Combine Two Tables
-- https://leetcode.com/problems/combine-two-tables
-- difficulty: easy
-- runtime: 414

# Write your MySQL query statement below
Select p.firstName, p.lastname, a.city, a.state
From Person p
left join Address a
on p.personId=a.personId;
