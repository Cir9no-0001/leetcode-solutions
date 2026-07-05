-- Customers Who Never Order
-- https://leetcode.com/problems/customers-who-never-order
-- solved: 2026-07-05 01:15:26 UTC

# Write your MySQL query statement below
Select c.name as Customers
From Customers c
left join orders o
on c.id = o.customerId
where o.id IS NULL;