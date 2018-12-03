---
title: 1 TF系统框架
toc: true
date: 2017-12-30
tags: [tensorflow]
top: 1
---

[转自](https://zhuanlan.zhihu.com/p/25646408)

2015年11月9日，Google发布深度学习框架TensorFlow并宣布开源，并迅速得到广泛关注，在图形分类、音频处理、推荐系统和自然语言处理等场景下都被大面积推广。TensorFlow系统更新快速，官方文档教程齐全，上手快速且简单易用，支持Python和C++接口。本文依据对Tensorflow（简称TF）白皮书[1]、TF Github[2]和TF官方教程[3]的理解，从系统和代码实现角度讲解TF的内部实现原理。以Tensorflow r0.8.0为基础，本文由浅入深的阐述Tensor和Flow的概念。先介绍了TensorFlow的核心概念和基本概述，然后剖析了OpKernels模块、Graph模块、Session模块。

# 1.  TF系统框架

## 1.1 TF依赖视图

TF的依赖视图如图1所示，描述了TF的上下游关系链。

![图 1 TensorFlow依赖视图](http://or9a8nskt.bkt.clouddn.com/15148850325344.jpg)




TF托管在github平台，有google groups和contributors共同维护。

TF提供了丰富的深度学习相关的API，支持Python和C/C++接口。

TF提供了可视化分析工具Tensorboard，方便分析和调整模型。

TF支持Linux平台，Windows平台，Mac平台，甚至手机移动设备等各种平台。

## 1.2 TF系统架构

图1-2是TF的系统架构，从底向上分为设备管理和通信层、数据操作层、图计算层、API接口层、应用层。其中设备管理和通信层、数据操作层、图计算层是TF的核心层。
![图1-2 TF系统架构](http://or9a8nskt.bkt.clouddn.com/15148851086975.jpg)



底层设备通信层负责网络通信和设备管理。设备管理可以实现TF设备异构的特性，支持CPU、GPU、Mobile等不同设备。网络通信依赖gRPC通信协议实现不同设备间的数据传输和更新。

第二层是Tensor的OpKernels实现。这些OpKernels以Tensor为处理对象，依赖网络通信和设备内存分配，实现了各种Tensor操作或计算。Opkernels不仅包含MatMul等计算操作，还包含Queue等非计算操作，这些将在第5章Kernels模块详细介绍。

第三层是图计算层（Graph），包含本地计算流图和分布式计算流图的实现。Graph模块包含Graph的创建、编译、优化和执行等部分，Graph中每个节点都是OpKernels类型表示。关于图计算将在第6章Graph模块详细介绍。

第四层是API接口层。Tensor C API是对TF功能模块的接口封装，便于其他语言平台调用。

第四层以上是应用层。不同编程语言在应用层通过API接口层调用TF核心功能实现相关实验和应用。

## 1.3 TF代码目录组织

图1-3是TF的代码结构视图，下面将简单介绍TF的目录组织结构。

![图1-3 TF代码目录组织结构](http://or9a8nskt.bkt.clouddn.com/15148898749709.png)

`Tensorflow/core`目录包含了TF核心模块代码。

`public`: API接口头文件目录，用于外部接口调用的API定义，主要是`session.h` 和`tensor_c_api.h`。

`client`: API接口实现文件目录。

`platform`: OS系统相关接口文件，如file system, env等。

`protobuf`: 均为.proto文件，用于数据传输时的结构序列化.

`common_runtime`: 公共运行库，包含`session`, `executor`, `threadpool`, `rendezvous`, memory管理, 设备分配算法等。

`distributed_runtime`: 分布式执行模块，如rpc session, rpc master, rpc worker, graph manager。

`framework`: 包含基础功能模块，如log, memory, tensor

`graph`: 计算流图相关操作，如construct, partition, optimize, execute等

`kernels`: 核心Op，如matmul, conv2d, argmax, batch_norm等

`lib`: 公共基础库，如gif、gtl(google模板库)、hash、histogram等。

`ops`: 基本ops运算，ops梯度运算，io相关的ops，控制流和数据流操作

`Tensorflow/stream_executor`目录是并行计算框架，由google stream executor团队开发。

`Tensorflow/contrib`目录是contributor开发目录。

`Tensroflow/python`目录是python API客户端脚本。

`Tensorflow/tensorboard`目录是可视化分析工具，不仅可以模型可视化，还可以监控模型参数变化。

`third_party`目录是TF第三方依赖库。

`eigen3`: eigen矩阵运算库，TF基础ops调用

`gpus`: 封装了cuda/cudnn编程库




## 1.4 TF – Kernels模块

TF中包含大量Op算子，这些算子组成Graph的节点集合。这些算子对Tensor实现相应的运算操作。图1-4列出了TF中的Op算子的分类和举例。

![图 1-4 TensorFlow核心库中的部分运算
](http://or9a8nskt.bkt.clouddn.com/15148898870393.png)



