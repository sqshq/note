---
title: 136 Single Number
toc: false
date: 2017-08-17
tags: [Leetcode, Hash Table, Bit Manipulation]
top: 136
---

## 136. Single Number

Given a **non-empty** array of integers, every element appears *twice* except for one. Find that single one.

**Note**:

Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

Example 1:

```
Input: [2,2,1]
Output: 1
```
Example 2:

```
Input: [4,1,2,1,2]
Output: 4
```


#### Java

这道题目涉及位操作。`^`(`xor`, 异或):  当两个位不同时，输出true/1。异或的真值表：


| A | B | Output  |
| --- | --- | --- |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 0 | 1 | 0 |


所以对于整数来说：

```python
0 ^ 0 = 0 
n ^ 0 = n 
n ^ n = 0
```

如果把题目中的所有整数接连异或，由于出现两次的数字异或结果为0，最后剩下的就是出现一次的数字。

```Java
public int singleNumber(int[] nums) {
    int res = 0;
    for (int num : nums)
        res ^= num;
    return res; 
}
```







#### Python

```python
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        n = 0
        for num in nums:
            n = n^num
        return n     
```


