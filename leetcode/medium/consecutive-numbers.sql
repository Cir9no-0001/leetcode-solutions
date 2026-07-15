-- Consecutive Numbers
-- https://leetcode.com/problems/consecutive-numbers
-- difficulty: medium
-- first_seen: 2026-07-08 02:38:05 EDT
-- runtime: 685ms
-- Notes:
-- Hint: CTE full join using union







with bogus as(
    select l.num, k.num as knum, j.num as jnum
    from Logs l
    left join Logs k on l.id=k.id-1
    left join Logs j on l.id=j.id+1

    union

    select l.num, k.num as knum, j.num as jnum
    from Logs l
    right join Logs k on l.id=k.id-1
    right join Logs j on l.id=j.id+1
)

select b.num as ConsecutiveNums
from bogus b
where b.num=b.knum and b.num=b.jnum;
