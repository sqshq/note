---
title: 谈谈Python中的拷贝
toc: false
date: 2017-10-30
tags: [Python, Copy]
---




## 可变和不可变对象


为了解释Python中的拷贝，首先要弄清楚Python中的对象分为可变和不可变对象。在Python中的每一个对象都可以分为不可变`immutable`或者可变`mutable`。对于Python核心数据类型，其分类如下：

* 可变： 列表，字典
* 不可变： 数字，字符串，元组


## 赋值

赋值并不拷贝。

**Assignment statements in Python do not copy objects**, they create bindings between a target and an object. For collections that are mutable or contain mutable items, a copy is sometimes needed so one can change one copy without changing the other.([Python官方文档](https://docs.python.org/3.6/library/copy.html#module-copy))


## 深拷贝和浅拷贝

来自`copy`模块的两个函数

* `copy.copy()` 浅拷贝

* `copy.deepcopy()` 深拷贝


The difference between shallow and deep copying is only relevant for **compound objects** (objects that contain other objects, like lists or class instances):

A **shallow copy** constructs a new compound object and then (to the extent possible) inserts references into it to the objects found in the original.
A **deep copy** constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.


## 常见类型拷贝

* dict.copy()  返回一个字典的浅复制。
* list.copy() 返回一个列表的浅复制。


