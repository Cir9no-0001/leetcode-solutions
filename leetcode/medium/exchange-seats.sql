-- Exchange Seats
-- https://leetcode.com/problems/exchange-seats
-- difficulty: medium
-- first_seen: 2026-07-12 23:32:52 EDT
-- runtime: 347ms
-- Notes:
-- Hint: use case and modulo to change the IDs, then reorder the IDs, don't forget about the last odd seat


select 
    case
        when s.id%2=0 then s.id-1
        when s.id%2=1 and s.id!=(select max(id) from Seat) then s.id+1
        else s.id
    end as id,
    s.student
from Seat s
order by id asc