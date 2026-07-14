-- Product Price at a Given Date
-- https://leetcode.com/problems/product-price-at-a-given-date
-- difficulty: medium
-- first_seen: 2026-07-14 11:53:25 EDT
-- runtime: 473ms
--
-- Notes:
--

select 
    p.product_id,
    p.new_price as 'price'
from Products p
where (p.product_id, p.change_date) in (
    select pr.product_id, max(pr.change_date)
    from Products pr
    where pr.change_date<='2019-08-16'
    group by pr.product_id
)

union

select 
    pro.product_id,
    10 as 'price'
from Products pro
group by pro.product_id
having min(pro.change_date)>'2019-08-16'