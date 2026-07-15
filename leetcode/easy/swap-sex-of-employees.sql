-- Swap Sex of Employees
-- https://leetcode.com/problems/swap-sex-of-employees
-- difficulty: easy
-- first_seen: 2026-07-08 02:38:06 EDT
-- runtime: 247ms
--
-- Notes stored in leetcode_notes.json
-- Notes:
--






update Salary s
set s.sex = case
    when s.sex ='m' then 'f'
    when s.sex ='f' then 'm'
end;
