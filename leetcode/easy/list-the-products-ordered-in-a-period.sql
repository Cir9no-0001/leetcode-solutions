-- List the Products Ordered in a Period
-- https://leetcode.com/problems/list-the-products-ordered-in-a-period
-- difficulty: easy
-- first_seen: 2026-07-20 00:03:50 EDT
-- runtime: 692ms
-- Notes:
-- Hint: use date_format to get rid of the day from the date, and CTE to get the monthly total units per product_id


with temp as(
    select o.product_id, date_format(o.order_date, '%Y-%m') as 'date', sum(o.unit) as 'unit'
    from Orders o
    group by o.product_id, date_format(o.order_date, '%Y-%m')
)
select p.product_name, t.unit
from temp t
inner join Products p
on p.product_id=t.product_id
where t.unit>=100 and t.date='2020-02'