---
title: 137 Single Number II
toc: false
date: 2017-08-17
tags: [Leetcode, Bit Manipulation]
top: 136
---

Given a **non-empty** array of integers, every element appears *three* times except for one, which appears exactly once. Find that single one.


**Note**:
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

Example 1:

```
Input: [2,2,3,2]
Output: 3
```

Example 2:

```
Input: [0,1,0,1,0,1,99]
Output: 99
```

#### 分析

这道题目是LeetCode 136 Single Number的扩展。其实LeetCode 136可以看成是这道题目的特例。为什么这么说呢？因为有一种通用的方法可以去除出现$n$次的整数。该方法使用位操作，具体来说就是如果整数出现$n$次，那么二进制表示的第$i$位数也出现$n$次，将第$i$位数加起来取$n$的余数肯定是0。用伪代码表示：

```Java
for (num : nums)
    res += (num >> i) & 1;
assert res % n == 0;
```

那么如果把出现一次的那个数字也算上，第$i$位数加起来取$n$的余数肯定等于出现一次的数字第$i$位数。将每一位上的数合起来(|，按位或)，即得到那个数。


```Java
public int singleNumberII(int[] nums) {
    int single = 0;
    for (int i = 0; i < 32; i++) {
        int iBit = 0;
        for (int num : nums)
            iBit += (num >> i) & 1;
        single |= (iBit % 3) << i;
    }
    return single;
}
```

还有1中解法，比较好的解释在[这里](https://leetcode.com/problems/single-number-ii/discuss/43302/Accepted-code-with-proper-Explaination.-Does-anyone-have-a-better-idea)

