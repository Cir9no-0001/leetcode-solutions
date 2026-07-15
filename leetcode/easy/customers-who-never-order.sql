-- Customers Who Never Order
-- https://leetcode.com/problems/customers-who-never-order
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:06 EDT
-- runtime: 576ms

Select c.name as Customers
From Customers c
left join orders o
on c.id = o.customerId
where o.id IS NULL;
