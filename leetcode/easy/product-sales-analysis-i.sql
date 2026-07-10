-- Product Sales Analysis I
-- https://leetcode.com/problems/product-sales-analysis-i
-- difficulty: easy
-- first_seen: 2026-07-10 00:35:07 EDT
-- runtime: 1090

select p.product_name, s.year, s.price 
from Sales s
join Product p 
on s.product_id=p.product_id;