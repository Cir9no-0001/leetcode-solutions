-- Market Analysis I
-- https://leetcode.com/problems/market-analysis-i
-- difficulty: medium
-- first_seen: 2026-07-14 11:53:25 EDT
-- runtime: 1287ms
--
-- Notes:
--

select 
    u.user_id as 'buyer_id', 
    u.join_date, 
    count(o.order_id) as orders_in_2019
from Users u
left join Orders o
    on u.user_id=o.buyer_id
    and o.order_date between '2019-00-00' and '2020-00-00'
group by u.user_id



