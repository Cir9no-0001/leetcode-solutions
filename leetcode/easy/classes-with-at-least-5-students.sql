-- Classes With at Least 5 Students
-- https://leetcode.com/problems/classes-with-at-least-5-students
-- difficulty: easy
-- first_seen (local): 2026-07-05 20:19:06 EDT
-- runtime: 311

Select c.class
from Courses c
Group by c.class
having count(class)>=5;