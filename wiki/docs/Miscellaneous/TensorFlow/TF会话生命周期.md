---
title: TF会话生命周期
toc: true
date: 2017-12-30
tags: [tensorflow]
top: 6
---

[转自](http://www.uml.org.cn/zjjs/201704123.asp)

TensorFlow的系统结构以C API为界，将整个系统分为「前端」和「后端」两个子系统：

前端系统：提供编程模型，负责构造计算图；

后端系统：提供运行时环境，负责执行计算图。

![系统架构](http://or9a8nskt.bkt.clouddn.com/15148941239904.png)

前端系统主要扮演Client的角色，主要负责计算图的构造，并管理Session生命周期过程。

前端系统是一个支持多语言的编程环境，并提供统一的编程模型支撑用户构造计算图。Client通过Session，连接TensorFlow后端的「运行时」，启动计算图的执行过程。

后端系统是TensorFlow的运行时系统，主要负责计算图的执行过程，包括计算图的剪枝，设备分配，子图计算等过程。

本文首先以Session创建为例，揭示前端Python与后端C/C++系统实现的通道，阐述TensorFlow多语言编程的奥秘。随后，以Python前端，C API桥梁，C++后端为生命线，阐述Session的生命周期过程。

# Swig: 幕后英雄

前端多语言编程环境与后端C/C++实现系统的通道归功于Swig的包装器。TensorFlow使用Bazel的构建工具，在编译之前启动Swig的代码生成过程，通过`tf_session.i`自动生成了两个适配(Wrapper)文件：

* pywrap_tensorflow.py: 负责对接上层Python调用；

* pywrap_tensorflow.cpp: 负责对接下层C实现。

此外，`pywrap_tensorflow.py`模块首次被加载时，自动地加载`_pywrap_tensorflow.so`的动态链接库。从而实现了`pywrap_tensorflow.py`到`pywrap_tensorflow.cpp`的函数调用关系。

在`pywrap_tensorflow.cpp`的实现中，静态注册了一个函数符号表。在运行时，按照Python的函数名称，匹配找到对应的C函数实现，最终转调到`c_api.c`的具体实现。

![Swig代码生成器](http://or9a8nskt.bkt.clouddn.com/15148941860360.png)


# 编程接口：Python

当Client要启动计算图的执行过程时，先创建了一个Session实例，进而调用父类BaseSession的构造函数。

```python
# tensorflow/python/client/session.py
class Session(BaseSession):
  def __init__(self, target='', graph=None, config=None):
    super(Session, self).__init__(target, graph, config=config)
    # ignoring others
```

在BaseSession的构造函数中，将调用`pywrap_tensorflow`模块中的函数。其中，`pywrap_tensorflow`模块自动由Swig生成。

```python
 # tensorflow/python/client/session.py
from tensorflow.python import pywrap_tensorflow as tf_session

class BaseSession(SessionInterface):
def __init__(self, target='', graph=None, config=None):
    self._session = None
    opts = tf_session.TF_NewSessionOptions(target=self._target, config=config)
    try:
        with errors.raise_exception_on_not_ok_status() as status:
            self._session = tf_session.TF_NewDeprecatedSession(opts, status)
    finally:
        tf_session.TF_DeleteSessionOptions(opts)
# ignoring others
```



# 生成代码：Swig

```  
pywrap_tensorflow.py

```

在pywrap_tensorflow模块中，通过_pywrap_tensorflow将在_pywrap_tensorflow.so中调用对应的C++函数实现。

```python
# tensorflow/bazel-bin/tensorflow/python/pywrap_tensorflow.py
def TF_NewDeprecatedSession(arg1, status):
    return _pywrap_tensorflow.TF_NewDeprecatedSession(arg1, status)
```

在pywrap_tensorflow.cpp的具体实现中，它静态注册了函数调用的符号表，实现Python的函数名称到C++实现函数的具体映射。

```python
# tensorflow/bazel-bin/tensorflow/python/pywrap_tensorflow.cpp
static PyMethodDef SwigMethods[] = {
    ...
     {"TF_NewDeprecatedSession", _wrap_TF_NewDeprecatedSession, METH_VARARGS, NULL},
}
PyObject *_wrap_TF_NewDeprecatedSession(
PyObject *self, PyObject *args) {
TF_SessionOptions* arg1 = ... 
TF_Status* arg2 = ...

TF_DeprecatedSession* result = TF_NewDeprecatedSession(arg1, arg2);
// ignoring others implements
}
```

最终，自动生成的pywrap_tensorflow.cpp仅仅负责函数调用的转发，最终将调用底层C系统向上提供的API接口。

# C API：桥梁

`c_api.h`是TensorFlow的后端执行系统面向前端开放的公共API接口之一，自此将进入TensorFlow后端系统的浩瀚天空。

```C
// tensorflow/c/c_api.c
TF_DeprecatedSession* TF_NewDeprecatedSession(
  const TF_SessionOptions*, TF_Status* status) {
  Session* session;
  status->status = NewSession(opt->options, &session);
  if (status->status.ok()) {
    return new TF_DeprecatedSession({session});
  } else {
    return NULL;
  }
}
```

# 后端系统：C++

NewSession将根据前端传递的Session.target，使用SessionFactory多态创建不同类型的Session(C++)对象。

```C
Status NewSession(const SessionOptions& options, Session** out_session) {
  SessionFactory* factory;
  Status s = SessionFactory::GetFactory(options, &factory);
  if (!s.ok()) {
    *out_session = nullptr;
    LOG(ERROR) << s;
    return s;
  }
  *out_session = factory->NewSession(options);
  if (!*out_session) {
    return errors::Internal("Failed to create session.");
  }
  return Status::OK();
}
```

# 会话生命周期

下文以前端Python，桥梁C API，后端C++为生命线，理顺三者之间的调用关系，阐述Session的生命周期过程。

在Python前端，Session的生命周期主要体现在：

创建Session(target)

迭代执行Session.run(fetches, feed_dict)

Session._extend_graph(graph)

Session.TF_Run(feeds, fetches, targets)

关闭Session

销毁Session

```python
sess = Session(target)
for _ in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
sess.close()
```

相应地，C++后端，Session的生命周期主要体现在：

根据target多态创建Session

Session.Create(graph)：有且仅有一次

Session.Extend(graph)：零次或多次

迭代执行Session.Run(inputs, outputs, targets)

关闭Session.Close

销毁Session对象

```C
// create/load graph ...
tensorflow::GraphDef graph;
// local runtime, target is ""
tensorflow::SessionOptions options;

// create Session
std::unique_ptr<tensorflow::Session> 
sess(tensorflow::NewSession(options));

// create graph at initialization.
tensorflow::Status s = sess->Create(graph);
if (!s.ok()) { ... }

// run step
std::vector<tensorflow::Tensor> outputs;
s = session->Run(
{}, // inputs is empty 
{"output:0"}, // outputs names
{"update_state"}, // target names
&outputs); // output tensors
if (!s.ok()) { ... }

// close
session->Close();
```

创建会话

上文介绍了Session创建的详细过程，从Python前端为起点，通过Swig自动生成的Python-C++的包装器为媒介，实现了Python到TensorFlow的C API的调用。

其中，C API是前端系统与后端系统的分水岭。后端C++系统根据前端传递的Session.target，使用SessionFactory多态创建Session(C++)对象。

![](http://or9a8nskt.bkt.clouddn.com/15148944313909.png)

创建会话

从严格的角色意义上划分，GrpcSession依然扮演了Client的角色。它使用target，通过RPC协议与Master建立通信连接，因此，GrpcSession同时扮演了RPC Client的角色。

![Session多态创建](http://or9a8nskt.bkt.clouddn.com/15148944356342.png)



# 创建/扩展图

随后，Python前端将调用Session.run接口，将构造好的计算图，以GraphDef的形式发送给C++后端。

其中，前端每次调用Session.run接口时，都会试图将新增节点的计算图发送给后端系统，以便后端系统将新增节点的计算图Extend到原来的计算图中。特殊地，在首次调用Session.run时，将发送整个计算图给后端系统。

后端系统首次调用Session.Extend时，转调(或等价)Session.Create；以后，后端系统每次调用Session.Extend时将真正执行Extend的语义，将新增的计算图的节点追加至原来的计算图中。

随后，后端将启动计算图执行的准备工作。

![创建/扩展图](http://or9a8nskt.bkt.clouddn.com/15148944411026.png)


# 迭代运行

接着，Python前端Session.run实现将Feed, Fetch列表准备好，传递给后端系统。后端系统调用Session.Run接口。

后端系统的一次Session.Run执行常常被称为一次Step，Step的执行过程是TensorFlow运行时的核心。

每次Step，计算图将正向计算网络的输出，反向传递梯度，并完成一次训练参数的更新。首先，后端系统根据Feed, Fetch，对计算图(常称为Full Graph)进行剪枝，得到一个最小依赖的计算子图(常称为Client Graph)。

然后，运行时启动设备分配算法，如果节点之间的边横跨设备，则将该边分裂，插入相应的Send与Recv节点，实现跨设备节点的通信机制。

随后，将分裂出来的子图片段(常称为Partition Graph)注册到相应的设备上，并在本地设备上启动子图片段的执行过程。

![关闭会话](http://or9a8nskt.bkt.clouddn.com/15148944539577.png)



当计算图执行完毕后，需要关闭Session，以便释放后端的系统资源，包括队列，IO等。会话关闭流程较为简单，如下图所示。

![关闭会话](media/2017041237.png)



# 销毁会话

最后，会话关闭之后，Python前端系统启动GC，当Session.del被调用后，启动后台C++的Session对象销毁过程。

![销毁会话](media/2017041238.png)



