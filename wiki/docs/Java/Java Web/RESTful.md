---
title: RESTful
---

REST -- REpresentational State Transfer 直接翻译：表现层状态转移。

![](figures/15605158680574.png)


REST最大的几个特点为：资源、统一接口、URI和无状态。

RESTful架构风格规定，数据的元操作，即CRUD(create, read, update和delete,即数据的增删查改)操作，分别对应于HTTP方法：GET用来获取资源，POST用来新建资源（也可以用于更新资源），PUT用来更新资源，DELETE用来删除资源，这样就统一了数据操作的接口，仅通过HTTP方法，就可以完成对数据的所有增删查改工作。