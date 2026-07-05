-- Game Play Analysis I
-- https://leetcode.com/problems/game-play-analysis-i
-- solved: 2026-07-05 01:15:24 UTC

SELECT 
    player_id, 
    MIN(event_date) AS first_login
FROM 
    Activity
GROUP BY 
    player_id;