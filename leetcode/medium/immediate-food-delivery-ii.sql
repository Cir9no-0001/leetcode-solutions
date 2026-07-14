-- Immediate Food Delivery II
-- https://leetcode.com/problems/immediate-food-delivery-ii
-- difficulty: medium
-- first_seen: 2026-07-14 19:39:03 EDT
-- runtime: 629ms
-- Notes:
--


select
    round(
        sum(
            case when d.order_date = d.customer_pref_delivery_date then 1
            else 0
            end
        )*100.00/count(d.delivery_id)
    ,2) as immediate_percentage
from
    Delivery d
where
    (d.customer_id, d.order_date) in (
        select de.customer_id, min(de.order_date) 
        from Delivery de
        group by de.customer_id
    )