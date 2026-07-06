-- Customer Placing the Largest Number of Orders
-- https://leetcode.com/problems/customer-placing-the-largest-number-of-orders
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:36:02 EDT
-- runtime: 462

# Write your MySQL query statement below
Select o.customer_number
from Orders o
group by o.customer_number
order by count(*) desc
limit 1