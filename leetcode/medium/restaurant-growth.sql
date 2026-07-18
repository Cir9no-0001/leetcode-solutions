-- Restaurant Growth
-- https://leetcode.com/problems/restaurant-growth
-- difficulty: medium
-- first_seen: 2026-07-18 10:33:02 EDT
-- runtime: 334ms
-- Notes:
-- Hint: use a CTE to count the number of customers in the given time frame and find the daily sum of all customers for every day, main query to find moving sum and moving average, use offset to remove days with invalid windows


with sorted as(
    select c.visited_on,
    sum(c.amount) as 'daily_sum',
    count(*) over (order by c.visited_on rows between 6 preceding and current row) as 'customer_count'
    from Customer c
    group by c.visited_on
)

select 
    s.visited_on,
    sum(s.daily_sum) over (order by s.visited_on rows between 6 preceding and current row) as 'amount',
    round(sum(s.daily_sum) over (order by s.visited_on rows between 6 preceding and current row)/s.customer_count, 2) as 'average_amount'
from sorted s
group by s.visited_on
order by s.visited_on asc
limit 999999 offset 6
