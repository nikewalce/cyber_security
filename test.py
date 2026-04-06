def removeDuplicates(nums) -> int:
    return len(nums[:2] + [nums[i] for i in range(2, len(nums)) if nums[i] != nums[i-2]]) if len(nums) > 2 else len(nums)

print(removeDuplicates([0,0,1,1,1,1,2,3,3])) #7