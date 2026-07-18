-- Monthly Transactions I
-- https://leetcode.com/problems/monthly-transactions-i
-- difficulty: medium
-- first_seen: 2026-07-15 23:44:19 EDT
-- runtime: 567ms
-- Notes:
-- Hint: use date_format to get rid of the day portion of the date; repeat when multigrouping


select 
    date_format(t.trans_date, '%Y-%m') as 'month', 
    t.country, 
    count(t.id) as 'trans_count',
    sum(state = 'approved') as 'approved_count',
    sum(t.amount) as 'trans_total_amount',
    sum(
        case
            when state = 'approved' then t.amount
            else 0
        end
    ) as 'approved_total_amount'
from Transactions t
group by date_format(t.trans_date, '%Y-%m'), t.country

