-- Game Play Analysis I
-- https://leetcode.com/problems/game-play-analysis-i
-- difficulty: easy
-- first_seen (EST): 2026-07-04 23:50:08
-- runtime: 473

SELECT 
    player_id, 
    MIN(event_date) AS first_login
FROM 
    Activity
GROUP BY 
    player_id;