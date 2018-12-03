---
title: 20. Valid Parentheses
toc: false
date: 2017-10-30
tags: [Leetcode, string, stack]
top: 20
---
## 题目
Given a string containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid.

The brackets must close in the correct order, `()` and `()[]{}` are all valid but `(]` and `([)] are not.

## 中文题目

判断一个只包含各种括号符号的字符串中括号的匹配情况。
注意点：

字符串中只会包含`(`, `)`, `[`, `]`, `{`, `}`这些字符
括号匹配要注意顺序，字符串`([)]`是错误的匹配
例子：

输入: s="(){}" 输出: True
输入: s="(){}[" 输出: False

## 思路

典型的用栈来解决的问题，遇到左括号就压栈，遇到右括号时如果栈为空（类似`]]]`的情况），则失败，否则取栈顶元素，看两个括号是否匹配。如果最后栈不为空（类似`[[[`的情况），则匹配失败。


```python
class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        chardict = {'(':')', '[':']', '{':'}'}
        n = len(s)
        stack = []
        for i in range(n):
            inchar = s[i]
            if (inchar == '(') or (inchar == '{') or (inchar =='['):
                stack.append(inchar)
            else:
                if len(stack) == 0:
                    return False
                outchar = stack.pop()
                if inchar != chardict[outchar]:
                    return False
        
        if len(stack) > 0:
            return False
        return True
```

Your runtime beats 100.00 % of python3 submissions.

