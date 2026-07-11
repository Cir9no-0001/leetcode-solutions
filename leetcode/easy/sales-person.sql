-- Sales Person
-- https://leetcode.com/problems/sales-person
-- difficulty: easy
-- first_seen: 2026-07-08 02:38:07 EDT
-- runtime: 1346ms
--
-- Notes stored in leetcode_notes.json

select s.name
from SalesPerson s
left join Orders o on s.sales_id = o.sales_id
left join Company c on o.com_id = c.com_id and c.name = 'RED'
group by s.sales_id, s.name
having count(c.com_id) = 0;