-- Students and Examinations
-- https://leetcode.com/problems/students-and-examinations
-- difficulty: easy
-- first_seen: 2026-07-12 23:07:02 EDT
-- runtime: 858ms
-- Notes:
--



select 
    s.student_id, 
    s.student_name, 
    sub.subject_name, 
    count(e.subject_name) as attended_exams
from Students s
cross join Subjects sub
left join Examinations e
    on e.student_id=s.student_id
    and e.subject_name=sub.subject_name
group by s.student_id, sub.subject_name
order by s.student_id asc