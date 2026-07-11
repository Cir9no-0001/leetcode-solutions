-- Article Views I
-- https://leetcode.com/problems/article-views-i
-- difficulty: easy
-- first_seen: 2026-07-11 09:02:16 EDT
-- runtime: 417ms
--
-- Notes stored in leetcode_notes.json

select distinct(v.author_id) as 'id'
from Views v
where v.author_id=viewer_id
order by v.author_id asc