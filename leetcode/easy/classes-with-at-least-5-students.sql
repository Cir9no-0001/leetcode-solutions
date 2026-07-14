-- Classes With at Least 5 Students
-- https://leetcode.com/problems/classes-with-at-least-5-students
-- difficulty: easy
-- first_seen: 2026-07-05 20:40:00 EDT
-- runtime: 311
--
-- Notes stored in leetcode_notes.json
-- Notes:
--





Select c.class
from Courses c
Group by c.class
having count(class)>=5;