-- Trips and Users
-- https://leetcode.com/problems/trips-and-users
-- difficulty: hard
-- first_seen: 2026-07-15 22:32:48 EDT
-- runtime: 493ms
-- Notes:
-- Hint: CTE and double inner join to filter banned users, case to sum cancels, and group by date


with active as(
    select t.id, t.client_id, t.driver_id, t.city_id, t.status, t.request_at
    from Trips t
    inner join Users u
    on u.users_id=t.client_id
    inner join Users s
    on s.users_id=t.driver_id
    where u.banned='No' and s.banned='No'
)

select 
    a.request_at as 'Day',
    round(
        sum(
            case
                when a.status = 'cancelled_by_driver' or  a.status = 'cancelled_by_client' then 1
                else 0
            end
        )/count(a.request_at)
    ,2) as 'Cancellation Rate'
from active a
group by a.request_at
having a.request_at between '2013-10-01' and '2013-10-03'