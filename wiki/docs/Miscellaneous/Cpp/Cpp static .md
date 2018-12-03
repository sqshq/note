---
title: static用法
toc: true
date: 2017-12-30
tags: [C, static]
top: 1
---


static在C语言中是非常重要的关键字，但是它很容易被理解错误。因为static可以出现在多个地方，有着不同的含义：

* static 全局变量
* static 局部变量
* static 函数

根本原因是[1]:
![static](http://or9a8nskt.bkt.clouddn.com/Screen Shot 2018-07-09 at 1.37.29 PM.png)


当一个全局变量被声明为static(静态全局变量)时，它的存储位置并没有改变，还在虚拟内存的.data段（已初始化数据）。但是它只在定义它的源文件内有效，其他源文件无法访问它。它最重要的改变是**链接属性**的改变：静态变量的初始化在链接时已完成，如果显示指定初始值，则初始化为0。

每次函数调用静态局部变量的时候都修改它然后离开，下次读的时候从全局存储区读出的静态局部变量就是上次修改后的值。






### References

1. Pointers on C, page 61

