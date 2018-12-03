---
title: STL源码剖析
toc: false
date: 2017-10-30
tags: [Cpp, STL]
top: 4
---


《STL源码剖析》这本书可以作为深入学习C++ STL的伴侣，毕竟并不是所有人都可以流畅地阅读STL源码的。这本书非常详细的剖析了STL源码：它对源码中重要的代码都做了详细的注释，而对于复杂的、难以理解的内容，作者也做了不少图解。


### 源码

学习之前，当然是先看看源码了。在mac上，LLVM附带的C++的STL(Standard Template Library)位于：

`/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1/`

另外，STL源码剖析推荐的SGI STL可以在[GITHUB](https://github.com/karottc/sgi-stl)下载，其[官方网站](https://community.hpe.com/t5/Servers-The-Right-Compute/SGI-com-Tech-Archive-Resources-now-retired/ba-p/6992583#.W0KS_baPCAx)不再提供下载。


