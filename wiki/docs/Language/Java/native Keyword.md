---
title: 修饰词native
toc: true
date: 2018-07-12
tags: [Java]
---

在`Class Object`中一个`wait()`方法定义为：

```Java
public final native void wait(long timeout) throws InterruptedException;
```

这里的native修饰词说明其修饰的方法的实现，是用其他语言(C/C++)实现的，该方法通过JNI调用本地代码。

### JNI


**JNI**(Java Native Interface, Java本地接口)使Java虚拟机中的Java程序可以调用本地代码。

![](http://or9a8nskt.bkt.clouddn.com/15345839777611.png)
