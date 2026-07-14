-- Product Sales Analysis III
-- https://leetcode.com/problems/product-sales-analysis-iii
-- difficulty: medium
-- first_seen: 2026-07-13 17:42:43 EDT
-- runtime: 719ms
-- Notes:
--


select s.product_id, s.year as 'first_year', s.quantity, s.price
from Sales s
where (s.product_id, s.year) in (
    select sa.product_id, min(sa.year)
    from Sales sa
    group by sa.product_id
)