-- Sales Person
-- https://leetcode.com/problems/sales-person
-- difficulty: easy
-- first_seen: 2026-07-07 18:22:02 EDT
-- runtime: 1346

-- NOTES START
-- write your notes here
-- NOTES END

select s.name
from SalesPerson s
left join Orders o on s.sales_id = o.sales_id
left join Company c on o.com_id = c.com_id and c.name = 'RED'
group by s.sales_id, s.name
having count(c.com_id) = 0;