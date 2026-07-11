-- User Activity for the Past 30 Days I
-- https://leetcode.com/problems/user-activity-for-the-past-30-days-i
-- difficulty: easy
-- first_seen: 2026-07-11 07:51:00 EDT
-- runtime: 444ms
--
-- Notes stored in leetcode_notes.json

select a.activity_date as day, count(distinct(user_id)) as active_users
from Activity a
where a.activity_date between '2019-06-28' and '2019-07-27'
group by a.activity_date