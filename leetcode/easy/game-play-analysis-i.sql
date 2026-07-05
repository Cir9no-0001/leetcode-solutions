-- Game Play Analysis I
-- https://leetcode.com/problems/game-play-analysis-i
-- synced: 2026-07-05 02:38:26 UTC

SELECT 
    player_id, 
    MIN(event_date) AS first_login
FROM 
    Activity
GROUP BY 
    player_id;