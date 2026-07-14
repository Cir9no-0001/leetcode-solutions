-- Tree Node
-- https://leetcode.com/problems/tree-node
-- difficulty: medium
-- first_seen: 2026-07-11 15:33:17 EDT
-- runtime: 524ms
-- Notes:
-- Hint: use case and subquery to see if a node already exists as a p_id


select t.id,
case
    when t.p_id is null then 'Root'
    when t.id in (select p_id from Tree) then 'Inner'
    else 'Leaf'
end as 'type'
from Tree t;