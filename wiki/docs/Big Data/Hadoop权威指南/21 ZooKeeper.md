---
title: 21 ZooKeeper
toc: false
date: 2017-10-30
---

* 中间件，提供协调服务
* 作用于分布式系统，发挥其优势，可以为大数据服务
* 支持Java, 提供java和C语言的客户端API

什么事分布式系统？

* 分布式系统：很多台计算机组成一个整体，一个整体一致对外并且处理同一请求
* 内部的每台计算机都可以互相通信(rpc/rest)
* 客户端到服务端的一次请求到响应结束会历经多台计算机

zookeeper的特性

* 一致性：数据一致性，数据按照顺序分批入库
* 原子性：事务要么成功那么失败，不会局部化
* 单一视图：客户端连接集群中的任意一个zk节点，数据都是一致的
* 可靠性：每次对zk的操作状态都会保存在服务端
* 实时性：客户端可以读取到zk服务端的最新数据

zk的作用

* master节点选举，主节点挂了以后，从节点就会接手工作，并且保证这个节点是唯一的，这也是所谓首脑模式，从而保证集群是高可用的
* 统一配置文件管理，即只需要部署一台服务器，则可以把相同的配置文件同步更新到其他所有服务器，此操作在云计算中用的特别多。
    * 假设修改了redis统一配置，需要在多个服务器上尽快修改
* 发布与订阅，类似于消息队列MQ,dubbo。发布者把数据存在znode上，订阅者会读取这个数据
* 提供分布式锁，分布式环境中不同进程之间争夺资源，类似于多线程中的锁
* 集群管理，集群中保证数据的强一致性


```
connect host:port
get path [watch]
ls path [watch]
set path data [version]
rmr path
delquota [-n|-b] path
quit
printwatches on|off
create [-s] [-e] path data acl
stat path [watch]
close
ls2 path [watch]
history
listquota path
setAcl path acl
getAcl path
sync path
redo cmdno
addauth scheme auth
delete path [version]
setquota -n|-b val path
```
 

### Resources

* [Apache ZooKeeper](https://zookeeper.apache.org/)
* [ZooKeeper Wiki](https://cwiki.apache.org/confluence/display/ZOOKEEPER/Index)
* [ZooKeeper Getting Started Guide](https://zookeeper.apache.org/doc/current/zookeeperStarted.html)