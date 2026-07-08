-- Two Sum
-- https://leetcode.com/problems/two-sum
-- difficulty: easy
-- first_seen: 2026-07-08 03:23:37 EDT
-- runtime: 3

-- NOTES START
-- write your notes here
-- NOTES END

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numMap = {}
        n = len(nums)
        for i in range(n):
            next = target - nums[i]
            if next in numMap:
                return [numMap[next], i]
            numMap[nums[i]] = i
        return []