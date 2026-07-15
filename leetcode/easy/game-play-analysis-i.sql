-- Game Play Analysis I
-- https://leetcode.com/problems/game-play-analysis-i
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:03 EDT
-- runtime: 473

SELECT 
    player_id, 
    MIN(event_date) AS first_login
FROM 
    Activity
GROUP BY 
    player_id;
