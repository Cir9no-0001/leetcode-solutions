-- Customers Who Never Order
-- https://leetcode.com/problems/customers-who-never-order
-- difficulty: easy
-- runtime: 576

# Write your MySQL query statement below
Select c.name as Customers
From Customers c
left join orders o
on c.id = o.customerId
where o.id IS NULL;