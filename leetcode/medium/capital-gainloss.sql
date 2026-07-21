-- Capital Gain/Loss
-- https://leetcode.com/problems/capital-gainloss
-- difficulty: medium
-- first_seen: 2026-07-20 05:50:39 EDT
-- runtime: 482ms
-- Notes:
-- Hint: group the stocks, then use if depending on the operation


select 
    s.stock_name,
    sum(if(s.operation='Buy', -s.price, s.price)) as 'capital_gain_loss'
from Stocks s
group by stock_name