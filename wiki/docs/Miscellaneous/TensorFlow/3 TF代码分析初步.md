---
title: 3 TF代码分析初步
toc: true
date: 2017-12-30
tags: [tensorflow]
top: 3
---


## 3.1 TF总体概述

为了对TF有整体描述，本章节将选取TF白皮书中的示例展开说明，如图 3-1所示是一个简单线性模型的TF正向计算图和反向计算图。图中x是输入，W是参数权值，b是偏差值，MatMul和Add是计算操作，dMatMul和dAdd是梯度计算操作，C是正向计算的目标函数，1是反向计算的初始值，dC/dW和dC/dx是模型参数的梯度函数。

![](http://or9a8nskt.bkt.clouddn.com/15148928910614.jpg)

以图 3-1为例实现的TF代码见图 3-2。首先声明参数变量W、b和输入变量x，构建线性模型$y=W*x+b$，目标函数loss采用误差平方和最小化方法，优化函数optimizer采用随机梯度下降方法。然后初始化全局参数变量，利用session与master交互实现图计算。

![](http://or9a8nskt.bkt.clouddn.com/15148928967117.jpg)
![](http://or9a8nskt.bkt.clouddn.com/15148929012499.jpg)


图 3-2中summary可以记录graph元信息和tensor数据信息，再利用Tensorboard分析模型结构和训练参数。

图 3-3是上述代码在Tensorboard中记录下的Tensor跟踪图。Tensorboard可以显示scaler和histogram两种形式。跟踪变量走势可更方便的分析模型和调整参数。
![](http://or9a8nskt.bkt.clouddn.com/15148929090396.jpg)

图 3-4是图 3-1示例在Tensorboard中显示的graph图。左侧子图描述的正向计算图和反向计算图，正向计算的输出被用于反向计算的输入，其中MatMul对应MatMul_grad，Add对应Add_grad等。右上侧子图指明了目标函数最小化训练过程中要更新的模型参数W、b，右下侧子图是参数节点W、b展开后的结果。
![](http://or9a8nskt.bkt.clouddn.com/15148929127069.jpg)


图 3-4中，参数W是命名空间（Namespace）类型，展开后的W主要由Assign和Read两个OpNode组成，分别负责W的赋值和读取任务。

命名空间gradients是隐含的反向计算图，定义了反向计算的计算逻辑。从图 3-1可以看出，更新参数W需要先计算dMatMul，即图 3-4中的MatMul_grad操作，而Update_W节点负责更新W操作。为了进一步了解UpdateW的逻辑，图 3-5对MatMul_grad和update_W进行了展开分析。

![](http://or9a8nskt.bkt.clouddn.com/15148929304603.jpg)


图 3-5中，子图(a)描述了MatMul_grad计算逻辑，子图(b)描述了MatMul_grad输入输出，子图(c)描述了update_W的计算逻辑。首先明确MatMul矩阵运算法则，假设 z=MatMul(x, y)，则有dx = MatMul(dz, y)，dy = MatMul(x, dz)，由此可以推出dW=MatMul(dAdd, x)。在子图(a)中左下侧的节点b就是输入节点x，dAdd由Add_grad计算输出。update_W的计算逻辑由最优化函数指定，而其中的minimize/update_W/ApplyGradientDescent变量决定，即子图(b)中的输出变量Outputs。

另外，在MatMul_grad/tuple命名空间中还隐式声明了control dependencies控制依赖操作，这在章节2.4控制流中相关说明。

## 3.2 Eigen介绍

在Tensorflow中核心数据结构和运算主要依赖于Eigen和Stream Executor库，其中Eigen支持CPU和GPU加速计算，Stream Executor主要用于GPU环境加速计算。下面简单讲述Eigen库的相关特性，有助于进一步理解Tensorflow。

### 3.2.1 Eigen简述

Eigen是高效易用的C++开源库，有效支持线性代数，矩阵和矢量运算，数值分析及其相关的算法。不依赖于任何其他依赖包，安装使用都很简便[8]。具有如下特性：

* 支持整数、浮点数、复数，使用模板编程，可以为特殊的数据结构提供矩阵操作。比如在用ceres-solver进行做优化问题（比如bundle adjustment）的时候，有时候需要用模板编程写一个目标函数，ceres可以将模板自动替换为内部的一个可以自动求微分的特殊的double类型。而如果要在这个模板函数中进行矩阵计算，使用Eigen就会非常方便。

*  支持逐元素、分块、和整体的矩阵操作。

*  内含大量矩阵分解算法包括`LU`，`LDLt`，`QR`、`SVD`等等。

*  支持使用`Intel MKL`加速

*  部分功能支持多线程

*  稀疏矩阵支持良好，到今年新出的`Eigen3.2`，已经自带了`SparseLU`、`SparseQR`、共轭梯度`Tensor`（ConjugateGradient solver）、bi conjugate gradient stabilized solver等解稀疏矩阵的功能。同时提供SPQR、UmfPack等外部稀疏矩阵库的接口。

*  支持常用几何运算，包括旋转矩阵、四元数、矩阵变换、AngleAxis（欧拉角与Rodrigues变换）等等。

*  更新活跃，用户众多（Google、WilliowGarage也在用），使用Eigen的比较著名的开源项目有ROS（机器人操作系统）、PCL（点云处理库）、Google Ceres（优化算法）。OpenCV自带到Eigen的接口。

Eigen库包含`Eigen`模块和`unsupported`模块，其中`Eigen`模块为`official module`，`unsupported`模块为开源贡献者开发的。

Eigen`unsupported` 模块中定义了数据类型`Tensor`及相关函数，包括`Tensor`的存储格式，`Tensor`的符号表示，`Tensor`的编译加速，`Tensor`的一元运算、二元运算、高维度泛化矩阵运算，`Tensor`的表达式计算。本章后续所述`Tensor`均为`Eigen::Tensor`

Eigen运算性能评估如图 3-6所示，eigen3的整体性能比eigen2有很大提升，与`GOTO2`、`INTEL_MKL`基本持平。

![](http://or9a8nskt.bkt.clouddn.com/15148929413896.jpg)


### 3.2.2 Eigen 存储顺序

Eigen中的`Tensor`支持两种存储方式:

*  Row-major表示矩阵存储时按照row-by-row的方式。

*  Col-major表示矩阵存储时按照column-by-column的方式。

Eigen默认采用`Col-major`格式存储的（虽然也支持Row-major，但不推荐），具体采用什么存储方式取决于算法本身是行遍历还是列遍历为主。例如：`A=[[a11, a12, a13], [a21, a22, a23]]`的存储序列见图3-7。

![](http://or9a8nskt.bkt.clouddn.com/15148929467282.jpg)


### 3.2.3 Eigen 惰性求值

在编程语言理论中，存在及早求值(`Eager Evaluation`) 和惰性求值（`Lazy Evaluation`）

* 及早求值：大多数编程语言所拥有的普通计算方式

* 惰性求值：也认为是“延迟求值”，可以提高计算性能，最重要的好处是它可以构造一个无限的数据类型。

关于惰性求值，举例如下：

`Vec3 = vec1 + vec2`;

及早求值形式需要临时变量`vec_temp`存储运算结果，再赋值给`vec3`，计算效率和空间效率都不高：

`Vec_temp = vec1 + vec2;
Vec3 = vec_temp`

而惰性求值不需要临时变量保存中间结果，提高了计算性能：

`Vec_symbol_3 = (vec_symbol_1 + vec_symbol_2);
Vec3 = vec_symbol_3.eval(vec1, vec2)`

由于Eigen默认采用惰性计算，如果要求表达式的值可以使用`Tensor::eval()`函数。`Tensor::eval()`函数也是`session.run()`的底层运算。例如：

`Tensor result = ((t1 + t2).eval() * 0.2f).exp()`

### 3.2.4 Eigen 编译加速

编译加速可以充分发挥计算机的并行计算能力，提高程序运行速度。

举例如下：

普通的循环相加运算时间复杂度是$O(n)$：

```cpp
for (int i=0; i< size; i++)
    u[i] = v[i] + w[i];
```

如果指令集支持128bit并行计算，则时间复杂度可缩短为$O(n/4)$：

```cpp
for (int i=0; i< 4*(size/4); i+=4)
    u.packet(i) = v.packet(i) + w.packet(i);
```

Eigen编译时使用了`SSE2`加速。假设处理`float32`类型，指令集支持`128bit`并行计算，则一次可以计算4个`float32`类型，速度提升4倍。

### 3.2.5 Eigen::half

Tensorflow支持的浮点数类型有`float16`, `float32`, `float64`，其中`float16`本质上是`Eigen::half`类型，即半精度浮点数。关于半精度浮点数，英伟达2002年首次提出使用半精度浮点数达到降低数据传输和存储成本的目的。

在分布式计算中，如果对数据精度要求不那么高，可以将传输数据转换为`float16`类型，这样可以大大缩短设备间的数据传输时间。在GPU运算中，`float16`还可以减少一般的内存占用。

在Tensorflow的分布式传输中，默认会将`float32`转换为`float16`类型。Tensorflow的转换方式不同于Nvidia的标准，采用直接截断尾数的方式转化为半精度浮点数，以减少转换时间。

![](http://or9a8nskt.bkt.clouddn.com/15148931707077.jpg)

![](http://or9a8nskt.bkt.clouddn.com/15148931776685.jpg)

![](http://or9a8nskt.bkt.clouddn.com/15148931813272.jpg)

浮点数存储格式分成3部分，符号位，指数和尾数。不同精度是指数位和尾数位的长度不一样。

## 3.3 设备内存管理

TF设备内存管理模块利用`BFC`算法（`best-fit with coalescing`）实现。`BFC`算法是`Doung Lea’s malloc(dlmalloc)`的一个非常简单的版本。它具有内存分配、释放、碎片管理等基本功能。

BFC将内存分成一系列内存块，每个内存块由一个`chunk`数据结构管理。从`chunk`结构中可以获取到内存块的使用状态、大小、数据的基址、前驱和后继`chunk`等信息。整个内存可以通过一个`chunk`的双链表结构来表示。

![](http://or9a8nskt.bkt.clouddn.com/15148887566906.jpg)


用户申请一个内存块（`malloc`）。根据建立的`chunk`双链表找到一个合适的内存块（后面会说明什么是合适的内存块），如果该内存块的大小是用户申请大小的两倍以上，那么将该内存块切分成两块，这就是split操作。返回其中一块给用户，并将该内存块标识为占用。Spilt操作会新增一个`chunk`，所以需要修改`chunk`双链表以维持前驱和后继关系。

用户释放一个内存块（free）。先将该块标记为空闲。然后根据`chunk`数据结构中的信息找到其前驱和后继内存块。如果前驱和后继块中有空闲的块，那么将刚释放的块和空闲的块合并成一个更大的`chunk`（这就是merge操作，合并当前块和其前后的空闲块）。再修改双链表结构以维持前驱后继关系。这就做到了内存碎片的回收。

`BFC`的核心思想是：将内存分块管理，按块进行空间分配和释放；通过`split`操作将大内存块分解成小内存块；通过`merge`操作合并小的内存块，做到内存碎片回收。

但是还留下许多疑问。比如说申请内存空间时，什么样的块算合适的内存块？如何快速管理这种块？

`BFC`算法采取的是被动分块的策略。最开始整个内存是一个`chunk`，随着用户申请空间的次数增加，最开始的大`chunk`会被不断的split开来，从而产生越来越多的小`chunk`。当`chunk`数量很大时，为了寻找一个合适的内存块而遍历双链表无疑是一笔巨大的开销。为了实现对空闲块的高效管理，`BFC`算法设计了bin这个抽象数据结构。

Bin数据结构中，每个bin都有一个size属性，一个bin是一个拥有`chunk` size >= bin size的空闲`chunk`的集合。集合中的`chunk`按照`chunk` size的升序组织成单链表。`BFC`算法维护了一个bin的集合：bins。它由多个bin以及从属于每个bin的`chunk`s组成。内存中所有的空闲`chunk`都由bins管理。

![](http://or9a8nskt.bkt.clouddn.com/15148887792693.jpg)


图 3-12中每一列表示一个bin，列首方格中的数字表示bin的size。bin size的大小都是256的$2^n$的倍。每个bin下面挂载了一系列的空闲`chunk`，每个`chunk`的`chunk` size都大于等于所属的bin的bin size，按照`chunk` size的升序挂载成单链表。`BFC`算法针对bins这个集合设计了三个操作：`search`、`insert`、`delete`。


* `Search` 操作：给定一个`chunk` size，从bins中找到大于等于该`chunk` size的最小的那个空闲`chunk`。Search操作具体流程如下。如果bin以数组的形式组织，那么可以从index = `chunk` size /256 >>2的那个bin开始查找。最好的情况是开始查找的那个bin的`chunk`链表非空，那么直接返回链表头即可。这种情况时间复杂度是常数级的。最坏的情况是遍历bins数组中所有的bin。对于一般大小的内存来说，bins数组元素非常少，比如4G空间只需要23个bin就足够了（256 * 2 ^ 23 > 4G），因此也很快能返回结果。总体来说search操作是非常高效的。对于固定大小内存来说，查找时间是常数量级的。

* `Insert` 操作：将一个空闲的`chunk`插入到一个bin所挂载的`chunk`链表中，同时需要维持`chunk`链表的升序关系。具体流程是直接将`chunk`插入到index = `chunk` size /256 >>2的那个bin中即可。

* `Delete`操作：将一个空闲的`chunk`从bins中移除。

TF中内存分配算法实现文件`core/common_runtime/bfc_allocator.cc`，GPU内存分配算法实现文件`core/common_runtime/gpu/gpu_bfc_allocator.cc`。

## 3.4 TF开发工具介绍

TF系统开发使用了`bazel`工具实现工程代码自动化管理，使用了`protobuf`实现了跨设备数据传输，使用了`swig`库实现python接口封装。本章将从这三方面介绍TF开发工具的使用。

### 3.4.1 Swig封装

Tensorflow核心框架使用C++编写，API接口文件定义在`tensorflow/core/public`目录下，主要文件是`tensor_c_api.h`文件，C++语言直接调用这些头文件即可。

Python通过`Swig`工具封装TF库包间接调用，接口定义文件`tensorflow/python/ tensorflow.i`。其中`swig`全称为S`implified Wrapper and Interface Generator`，是封装C/C++并与其它各种高级编程语言进行嵌入联接的开发工具，对swig感兴趣的请参考相关文档。

在`tensorflow.i`文件中包含了若干个`.i`文件，每个文件是对应模块的封装，其中`tf_session.i`文件中包含了`tensor_c_api.h`，实现`client`向`session`发送请求创建和运行`graph`的功能。

### 3.4.2 Bazel编译和调试

`Bazel`是Google开源的自动化构建工具，类似于Make和CMake工具。`Bazel`的目标是构建“快速并可靠的代码”，并且能“随着公司的成长持续调整其软件开发实践”。

TF中几乎所有代码编译生成都是依赖`Bazel`完成的，了解`Bazel`有助于进一步学习TF代码，尤其是编译测试用例进行gdb调试。

`Bazel`假定每个目录为[package]单元，目录里面包含了源文件和一个描述文件BUILD，描述文件中指定了如何将源文件转换成构建的输出。

以图 3-13为例，左子图为工程中不同模块间的依赖关系，右子图是对应模块依赖关系的BUILD描述文件。

图 3-13中name属性来命名规则，srcs属性为模块相关源文件列表，deps属性来描述规则之间的依赖关系。”//search: google_search_page”中”search”是包名，”google_search_page”为规则名，其中冒号用来分隔包名和规则名；如果某条规则所依赖的规则在其他目录下，就用"//"开头，如果在同一目录下，可以忽略包名而用冒号开头。

图 3-13中`cc_binary`表示编译目标是生成可执行文件，`cc_library`表示编译目标是生成库文件。如果要生成g`oogle_search_page`规则可运行

```
bazel buid -c opt // search: google_search_page
```

如果要生成可调试的二进制文件，可运行

```
bazel buid -c dbg // search: google_search_page
```

![](http://or9a8nskt.bkt.clouddn.com/15148888013357.jpg)

TF中首次运行`bazel`时会自动下载很多依赖包，如果有的包下载失败，打开`tensorflow/workspace.bzl`查看是哪个包下载失败，更改对应依赖包的`new_http_archive`中的url地址，也可以把`new_http_archive`设置为本地目录`new_local_repository`。

TF中测试用例跟相应代码文件放在一起，如`MatMul`操作的`core/kernels/matmul_op.cc`文件对应的测试用例文件为`core/kernels/matmul_op_test.cc`文件。运行这个测试用例需要查找这个测试用例对应的BUILD文件和对应的命令规则，如`matmul_op_test.cc`文件对应的BUILD文件为`core/kernels/BUILD`文件，如下

![](http://or9a8nskt.bkt.clouddn.com/15148933046986.jpg)

其中`tf_cuda_cc_test`函数是TF中自定义的编译函数，函数定义在`/tensorflow/ tensorflow.bzl`文件中，它会把`matmul_op_test.cc`放进编译文件中。要生成`matmul_op_test`可执行文件可运行如下脚本：

![](http://or9a8nskt.bkt.clouddn.com/15148933132091.jpg)



### 3.4.3 Protobuf序列化

`Protocol Buffers` 是一种轻便高效的结构化数据存储格式，可以用于结构化数据串行化，或者说序列化。它很适合做数据存储或 RPC 数据交换格式。可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式。

`Protobuf`对象描述文件为`.proto`类型，编译后生成`.pb.h`和`.pb.cc`文件。

`Protobuf`主要包含读写两个函数：Writer（序列化）函数`SerializeToOstream() `和  Reader（反序列化）函数 `ParseFromIstream()`。

Tensorflow在`core/probobuf`目录中定义了若干与分布式环境相关的.proto文件，同时在core/framework目录下定义了与基本数据类型和结构的.proto文件，在core/util目录中也定义部分.proto文件，感觉太随意了。

在分布式环境中，不仅需要传输数据序列化，还需要数据传输协议。`Protobuf`在序列化处理后，由`gRPC`完成数据传输。`gRPC`数据传输架构图见图3-14。

![](http://or9a8nskt.bkt.clouddn.com/15148888381032.jpg)

`gRPC`服务包含客户端和服务端。`gRPC`客户端调用`stub` 对象将请求用 `protobuf` 方式序列化成字节流，用于线上传输，到 `server`端后调用真正的实现对象处理。gRPC的服务端通过observer观察处理返回和关闭通道。

TF使用gRPC完成不同设备间的数据传输，比如超参数、梯度值、graph结构。


