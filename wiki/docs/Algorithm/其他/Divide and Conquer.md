---
title: Divide and Conquer
toc: true
date: 2017-10-30
tags: []
top: 3
---

In **divide and conquer**(分治法), we solve a problem recursively, applying three steps at each level of the recursion[1]:

* **Divide** the problem into a number of subproblems that are smaller instances of the same problem.

* **Conquer** the subproblems by solving them recursively. If the subproblem sizes are small enough, however, just solve the subproblems in a straightforward manner.

* **Combine** the solutions to the subproblems into the solution for the original problem.


分治法的设计思想是：

* 分 – 将问题分解为规模更小的子问题；
* 治 – 递归地解决子问题；
* 合 – 将子问题的解合并成原问题的解；

## Recurrences

Recurrences (递归表达式) go hand in hand with the divide-and-conquer paradigm. A **recurrence** is an equation or inequality that describes a function in terms of its value on smaller inputs[1]. 

例如， 归并排序的最差运行时间$T(n)$用递归表达式表达为

$$T(n)=2T(n/2)+o(n)$$

## Problems

利用分治法解决的经典问题：

* 二分搜索
* 大整数的乘法
* Strassen矩阵乘法
* 归并排序
* 快速排序

### 归并排序

MergeSort (归并排序) divides the list $L[0..n-1]$ into two halves $L[0..\llcorner n/2\lrcorner -1]$ and $L[\llcorner n/2\lrcorner ..n-1]$, sorting each of them recursively, and then merging the two smaller sorted arrays into a single sorted one[2].


Pseudocode:

```
MergeSort Input: List L of ``orderable” elements 
Modiﬁes: List L is sorted in-place in ascending order 
Output: None

If n>1
    copy L[0..⎣n/2⎦-1] to A[0..⎣n/2⎦-1];
    copy L[⎣n/2⎦..n-1] to B[0.. ⎡n/2⎤-1];
    MergeSort(A[0..⎣n/2⎦-1]);
    MergeSort(B[0..⎡n/2⎤-1]);
    Merge(A,B,L);
```

Let $C(n)$ be the number of steps MergeSort takes on a list L that has n elements.

Then, we have the recurrence::

$$ C(n) = 2C(n/2)+C_{\text{merge}} (n) \quad \text{for}\quad  n>1, \text{and} \quad  C(1)=1$$




## Reference 

* 算法导论(第三版英文版)
* Algorithm thinking on Coursera


