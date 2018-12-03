---
title: 5 TF - Graph模块 
toc: true
date: 2017-12-30
tags: [tensorflow]
top: 5
---

[转自](https://zhuanlan.zhihu.com/p/25932160)

#5\. TF - Graph模块

TF把神经网络模型表达成一张拓扑结构的Graph，Graph中的一个节点表示一种计算算子。Graph从输入到输出的Tensor数据流动完成了一个运算过程，这是对类似概率图、神经网络等连接式算法很好的表达，同时也是对Tensor + Flow的直观解释。

##5.1 Graph视图

Tensorflow采用符号化编程，形式化为Graph计算图。Graph包含节点（Node）、边（Edge）、NameScope、子图（SubGraph），图 5-1是Graph的拓扑描述。

Ø 节点分为计算节点(Compute Node)、起始点（Source Node）、终止点（Sink Node）。起始点入度为0，终止点出度为0。

Ø NameScope为节点创建层次化的名称，图 3 4中的NameSpace类型节点就是其中一种体现。

Ø 边分为普通边和依赖边（Dependecy Edge）。依赖边表示对指定的计算节点有依赖性，必须等待指定的节点计算完成才能开始依赖边的计算。

![](http://or9a8nskt.bkt.clouddn.com/15148905244886.jpg)

图 5 2是Graph的UML视图模型，左侧GraphDef类为protobuf中定义的graph结构，可将graph结构序列化和反序列化处理，用于模型保存、模型加载、分布式数据传输。右侧Graph类为/core/graph模块中定义的graph结构，完成graph相关操作，如构建(construct)，剪枝(pruning)、划分(partitioning)、优化(optimize)、运行(execute)等。GraphDef类和Graph类可以相关转换，如图中中间部分描述，函数Graph::ToGraphDef()将Graph转换为GraphDef，函数ConvertGraphDefToGraph将GraphDef转换为Graph，借助这种转换就能实现Graph结构的网络传输。

![](http://or9a8nskt.bkt.clouddn.com/15148905444950.jpg)

Graph-UML图中还定义了Node和Edge。Node定义函数操作和属性信息，Edge连接源节点和目标节点。类NodeDef中定义了Op、Input、Device、Attr信息，其中Device可能是CPU、GPU设备，甚至是ARM架构的设备，说明Node是与设备绑定的。类FunctionDefLibrary主要是为了描述各种Op的运算，包括Op的正向计算和梯度计算。FunctionDef的定义描述见图 5 3。

![](http://or9a8nskt.bkt.clouddn.com/15148905577275.jpg)

图 5-4是FunctionDef举例，对MatMulGrad的梯度描述，其中包含函数参数定义、函数返回值定义、模板数据类型定义、节点计算逻辑。

![](http://or9a8nskt.bkt.clouddn.com/15148905637262.jpg)

**5.2** **Graph构建**

有向图（DAG）由节点和有向边组成。本章节主要讲述TF如何利用组合成完整的graph的。假设有如下计算表达式：t1=MatMul(input, W1)。

![](http://or9a8nskt.bkt.clouddn.com/15148905769009.jpg)

图 5-5中图计算表达式包含3个节点，2条边，描述为字符串形式如下。

```
node {name: 'W1' op: 'TestParams'},
node {name: 'input' op: 'TestInput' input:['^W1']},
node {name: 't1' op: 'MatMul' input:['^W1', 'input:1']},
```

TF先调用protobuf的解析方法将graph的字符串描述解析并生成GraphDef实例。

```cpp
protobuf::TextFormat::ParseFromString(gdef_str, &gdef_)
```

然后将GraphDef实例转化为tensorflow::Graph实例，这个过程由tensorflow::GraphConstructor类完成。GraphConstructor先判别node的字符串格式是否正确，然后执行convert函数。

```cpp
GraphConstructor::Convert()
[graph/graph_constructor.cc]
```

首先，按拓扑图的顺序逐步添加node和edge到graph中。

```cpp
Graph:: AddNode(const NodeDef& node_def, Status* status)
Graph:: AddEdge(Node* source, int x, Node* dest, int y)
                             [graph/graph.cc]
```
然后，找出所有起始点（source node）和终止点（sink node）。

```cpp
FixupSourceAndSinkEdges(Graph* g)
            [graph/algorithms.cc]
```

接着，对graph进行优化。图优化部分请参考章节6.5。

```cpp
OptimizeCSE(Graph* g, std::function<bool(const Node*)> consider_fn);
                 [graph/optimizer_cse.cc]
```

TF的graph构建模块测试用例在`core/graph/graph_constructor_test.cc`文件中。

```bash
$ bazel build -c dbg //tensorflow/core/graph_graph_constor_test
$ gdb bazel-bin/tensorflow/core/graph_graph_constructor_test
```

##5.3 Graph局部执行

Graph的局部执行特性允许使用者从任意一个节点输入（feed），并指定目标输出节点（fetch）。图 5 6是TF白皮书中描述Graph局部执行的图。[15]

![](http://or9a8nskt.bkt.clouddn.com/15148918604764.jpg)


图 5-6中左侧为计算图，如果要实现`f=F(c)`运算，代码如下：

```
result=sess.run(f, feed_dict={c:input})
```

TF是如何知道两个点之间的计算路径呢？这里涉及传递闭包的概念。传递闭包就是根据graph中节点集合和有向边的集合，找出从节点A到节点B的最小传递关系。如上图中，点a到点f的传递闭包是a -> c -> f。

Graph局部执行过程就是找到feed和fetch的最小传递闭包，这个传递闭包相当于原graph的subgraph。代码文件在graph/[http://subgraph.cc](http://link.zhihu.com/?target=http%3A//subgraph.cc)中，函数RewriteGraphForExecution()在确定feed节点和fetch节点后，通过剪枝得到最小传递子图。


```
PruneForTargets(g, name_index, fetch_nodes, target_node_names));
                [graph/subgraph.cc]
```
剪枝操作的实现函数如下，Graph通过模拟计算流标记出节点是否被访问，剔除未被访问的节点。


```
PruneForReverseReachability(Graph* g, std::unordered_set<const Node*> visited)
[graph/algorithm.cc]
```
##5.4 Graph设备分配

TF具有高度设备兼容性，支持X86和Arm架构，支持CPU、GPU运算，可运行于Linux、MacOS、Android和IOS系统。而且，TF的设备无关性特征在多设备分布式运行上也非常有用。

Graph中每个节点都分配有设备编号，表示该节点在相应设备上完成计算操作。用户既可以手动指定节点设备，也可以利用TF自动分配算法完成节点设备分配。设备自动算法需要权衡数据传输代价和计算设备的平衡，尽可能充分利用计算设备，减少数据传输代价，从而提高计算性能。

Graph设备分配用于管理多设备分布式运行时，哪些节点运行在哪个设备上。TF设备分配算法有两种实现算法，第一种是简单布放算法（Simple Placer），第二种基于代价模型（Cost Model）评估。简单布放算法按照指定规则布放，比较简单粗放，是早期版本的TF使用的模型，并逐步被代价模型方法代替。

###5.4.1 Simple Placer算法

TF实现的Simple Placer设备分配算法使用union-find方法和启发式方法将部分不相交且待分配设备的Op节点集合合并，并分配到合适的设备上。

Union-find（联合-查找）算法是并查集数据结构一种应用。并查集是一种树型的数据结构，其保持着用于处理一些不相交集合（Disjoint Sets）的合并及查询问题。Union-find定义了两种基本操作：Union和Find。

* Find：确定元素属于哪一个子集。它可以被用来确定两个元素是否属于同一子集。

* Union：将两个子集合并成同一个集合。即将一个集合的根节点的父指针指向另一个集合的根节点。

启发式算法（Heuristic Algorithm）定义了节点分配的基本规则。Simple Placer算法默认将起始点和终止点分配给CPU，其他节点中GPU的分配优先级高于CPU，且默认分配给GPU:0。启发式规则适用于以下两种场景：

* 对于符合GeneratorNode条件（0-indegree, 1-outdegree, not ref-type）的节点，让node与target_node所在device一致，参见图 5 7。

![](http://or9a8nskt.bkt.clouddn.com/15148907334988.jpg)

* 对于符合MetaDataNode条件（即直接在原数据上的操作，如reshape）的节点，让node与source_node所在device一致，参见图 5 8。

![](http://or9a8nskt.bkt.clouddn.com/15148907386738.jpg)

TF中Simple Placer的实现定义在文件`core/common_runtime/simple_placer.cc`。文件中主要定义了两个类：ColocationGraph和SimplePlacer。ColocationGraph类利用Union-find算法将节点子集合合并成一个节点集合，参考成员函数ColocationGraph:: ColocateNodes实现。SimplePlacer类实现节点分配过程，下面将主要介绍SimplePlacer:: Run()函数的实现过程。


```python
SimplePlacer::Run()
```

**首先，**将graph中的node加入到ColocationGraph实例中，不包含起始点和终止点。

```
ColocationGraph colocation_graph(graph_, devices_, options_);
colocation_graph.AddNode(*node);[for node in _graph]
```


**然后，**找出graph中受constraint的edge(即src_node被指定了device的edge)，强制将dst_node指定到src_node所在的device。

```
colocation_graph.ColocateNodes(*edge->src(), *node);
```

**最后，**根据graph中已有的constraint条件为每个no-constraint的node指定device。

```
if IsGeneratorNode(node) AssignAndLog(assigned_device, node);
if IsMetadataNode(node) AssignAndLog(assigned_device, node);
```
Simple Placer的测试用例core/common_runtime/simple_placer_test.cc)文件，要调试这个测试用例，可通过如下方式：

```
$ bazel buid -c dbg //tensorflow/core:common_runtime_simple_placer_test
$ gdb bazel-bin/tensorflow/core/common_runtime_simple_placer_test
```

###5.4.2 代价模型

TF使用代价模型（Cost Model）会在计算流图生成的时候模拟每个device上的负载，并利用启发式策略估计device上的完成时间，最终找出预估时间最低的graph设备分配方案。[1]

Cost model预估时间的方法有两种：

Ø 使用启发式的算法，通过把输入和输出的类型以及tensor的大小输入进去，得到时间的预估

Ø 使用模拟的方法，对图的计算进行一个模拟，得到各个计算在其可用的设备上的时间。

启发式策略会根据如下数据调整device的分配：节点任务执行的总时间；单个节点任务执行的累计时间；单个节点输出数据的尺寸。

![](http://or9a8nskt.bkt.clouddn.com/15148910522852.jpg)

TF中代价模型的实现定义在文件core/graph/[http://costmodel.cc](http://link.zhihu.com/?target=http%3A//costmodel.cc)和core/common_runtime/ [http://costmodel_manager.cc](http://link.zhihu.com/?target=http%3A//costmodel_manager.cc)，其UML视图参见图 5 9。

Cost model manager从graph创建cost model，再评估计算时间，如下。

```c++
Void ConstModel:: InitFromGraph(const Graph& g){
    AddNodesToCostModel(g, this);
    AssignSizes(g, this);
    EstimateComputationCosts(g, this);
    CheckInitialized(g);
}
```

其中评估时间的函数EstimateComputationCosts是对graph中每个node依次评估，节点计算时间评估函数如下。

```c++
TimeEstimateForNode(CostModel* cost_model, Node* n)
```

##5.5 Graph优化

Graph优化算法利用一些优化策略，降低graph的计算复杂度和空间复杂度，提高graph运行速度。

Graph优化算法的实现在文件`core/common_runtime/graph_optimizer.cc`)。

```cpp
GraphOptimizer::Optimize(FunctionLibraryRuntime* runtime,
                Device* device, Graph** graph)
```
Graph优化策略有三种：

### Common Subexpression Elimination (CSE, 公共子表达式消除)

如果一个表达式E已经计算过了，并且从先前的计算到现在的E中的变量都没有发生变化，那么E的此次出现就成为了公共子表达式。例如：x=(a+c)*12+(c+a)*2; 可优化为 x=E*14。

CSE实现函数如下，具体细节参考文献[16]。

```cpp
OptimizeCSE(Graph* g, std:: function<bool(const Node*)>
                            consider_fn);
                    [graph/optimizer_cse.cc]
```

CSE测试用例在文件graph/[http://optimizer_cse_test.cc](http://link.zhihu.com/?target=http%3A//optimizer_cse_test.cc)中，调试方法：

```bash
$ bazel build -c dbg //tensorflow/core:graph_optimizer_cse_test
$ gdb bazel-bin/tensorflow/core/graph_optimizer_cse_test
```

### Constant Folding (常量合并)

在编译优化时，变量如果能够直接计算出结果，那么变量将有常量直接替换。例如：a=3+1-3*1; 可优化为a=1。

常量合并的实现函数如下。

![](media/v2-2c9db44dbcc589a3303d1adb97b49b10_hd.jpg)

常量合并的测试用例在`common_runtime/constant_folding_test.cc`)中，调试方法：

![](media/v2-11d9cd09d86e21949ae7f253a96390b3_hd.jpg)

### Function Inlining (函数内联)

函数内联处理可减少方法调用的成本。在TF中包含以下几种方法：

* RemoveListArrayConverter(g)：” Rewrites _ListToArray and _ArrayToList to a set of Identity nodes”.

* RemoveDeadNodes(g)：删除DeatNode。DeatNode的特征是”not statefull, not _Arg, not reachable from _Retval”.

* RemoveIdentityNodes(g)：删除Identity节点。如n2=Identity(n1) + Identity(n1); 优化后: n2=n1 + n1;

* FixupSourceAndSinkEdges(g)：固定source和sink的边

* ExpandInlineFunctions(runtime, g)：展开内联函数的嵌套调用

其中`_ListToArray`、`_ArrayToList`、`_Arg`、`_Retval`均在`core/ops/function_ops.cc`)中定义。

Graph优化相关测试文件在`common_runtime/function_test.cc`)，调试方法：

```
$ bazel build -c dbg //tensorflow/core:common_runtime_function_test
$ gdb bazel-bin /tensorflow/core/common_runtime_function_test
```


