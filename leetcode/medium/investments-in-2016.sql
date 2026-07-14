-- Investments in 2016
-- https://leetcode.com/problems/investments-in-2016
-- difficulty: medium
-- first_seen: 2026-07-10 00:31:24 EDT
-- runtime: 563ms
-- Notes:
-- Hint: use CTE, concat subquery for location, use exclusive logic using count and group


with valid as (
    select distinct(i.pid), i.tiv_2016
    from Insurance i
    
    inner join Insurance j
    on i.tiv_2015=j.tiv_2015 and i.pid <> j.pid
    
    where concat(i.lat, ',', i.lon) in (
        select concat(lat, ',', lon)
        from Insurance k
        group by k.lat, k.lon
        having count(*)=1
    )
)

select round(sum(v.tiv_2016),2) as 'tiv_2016'
from valid v