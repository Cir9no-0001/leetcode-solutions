-- Sales Analysis III
-- https://leetcode.com/problems/sales-analysis-iii
-- difficulty: easy
-- first_seen: 2026-07-10 06:49:35 EDT
-- runtime: 1208ms
--
-- Notes stored in leetcode_notes.json

select p.product_id, p.product_name
from Product p
inner join Sales s
on p.product_id=s.product_id
group by p.product_id, p.product_name
having min(s.sale_date)>='2019-01-01' and max(s.sale_date)<='2019-03-31';