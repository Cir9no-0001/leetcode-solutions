-- Triangle Judgement
-- https://leetcode.com/problems/triangle-judgement
-- difficulty: easy
-- first_seen: 2026-07-08 03:16:17 EDT
-- runtime: 289ms
--
-- Notes stored in leetcode_notes.json
-- Notes:
--

select t.x, t.y, t.z, 
case
    when t.x+t.y>t.z and t.x+t.z>t.y and t.z+t.y>t.x 
    then 'Yes'
    else 'No'
    end as triangle
from Triangle t