-- Movie Rating
-- https://leetcode.com/problems/movie-rating
-- difficulty: medium
-- first_seen: 2026-07-21 18:15:05 EDT
-- runtime: 1770ms
-- Notes:
-- Hint: split the query into two and merge using union all, order by has two variables to consider and lexicographically smaller means name/title asc. [TC: O(R1 + R2log M), 2 passes]


(
select u.name as 'results'
from MovieRating mr
inner join Users u
on mr.user_id = u.user_id
group by u.name
order by count(u.name) desc, u.name asc
limit 1
)

union all

(
select m.title as 'results'
from MovieRating mr
inner join Movies m
    on mr.movie_id=m.movie_id
    and mr.created_at between '2020-02-01' and '2020-02-29'
group by m.title
order by avg(mr.rating) desc, m.title asc
limit 1
)