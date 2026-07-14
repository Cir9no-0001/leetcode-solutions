-- Biggest Single Number
-- https://leetcode.com/problems/biggest-single-number
-- difficulty: easy
-- first_seen: 2026-07-09 04:53:51 EDT
-- runtime: 417ms

select(
    select m.num
    from MyNumbers m
    group by m.num
    having count(*)=1
    order by m.num desc
    limit 1
) as num;
