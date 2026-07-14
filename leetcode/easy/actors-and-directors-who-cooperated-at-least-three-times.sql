-- Actors and Directors Who Cooperated At Least Three Times
-- https://leetcode.com/problems/actors-and-directors-who-cooperated-at-least-three-times
-- difficulty: easy
-- first_seen: 2026-07-09 02:31:14 EDT
-- runtime: 367ms
-- Notes:
--


Select a.actor_id, a.director_id
from ActorDirector a
group by a.actor_id, a.director_id
having count(*)>=3;