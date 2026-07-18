-- DNA Pattern Recognition 
-- https://leetcode.com/problems/dna-pattern-recognition
-- difficulty: medium
-- first_seen: 2026-07-18 10:56:06 EDT
-- runtime: 288ms
-- Notes:
-- Hint: use if, braindead question

select 
    s.sample_id,
    s.dna_sequence,
    s.species,
    if(s.dna_sequence like 'ATG%', 1, 0) as 'has_start',
    if(s.dna_sequence like '%TAA' or s.dna_sequence like '%TAG' or s.dna_sequence like '%TGA', 1, 0) as 'has_stop',
    if(s.dna_sequence like '%ATAT%', 1, 0) as 'has_atat',
    if(s.dna_sequence like '%GGG%', 1, 0) as 'has_ggg'
from Samples s