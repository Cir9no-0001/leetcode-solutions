-- Customers Who Bought All Products
-- https://leetcode.com/problems/customers-who-bought-all-products
-- difficulty: medium
-- first_seen: 2026-07-12 23:52:16 EDT
-- runtime: 513ms
-- Notes:
--


select c.customer_id
from Customer c
group by c.customer_id
having count(distinct c.product_key)=(select count(product_key) from Product)