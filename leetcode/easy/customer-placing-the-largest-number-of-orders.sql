-- Customer Placing the Largest Number of Orders
-- https://leetcode.com/problems/customer-placing-the-largest-number-of-orders
-- difficulty: easy
-- runtime: 462ms

# Write your MySQL query statement below
Select o.customer_number
from Orders o
group by o.customer_number
order by count(*) desc
limit 1