---
title: Mac环境下搭建Hadoop家族产品
date: 2017-09-30
toc: true
author: larry
tags: [Hadoop]
---


### 1. 安装Hadoop

上面步骤和条件如果都具备的话，就可以安装Hadoop了。Hadoop有三种运行模式：**单机模式**，**伪分布式模式**，**分布式模式**，这里设置的是伪分布式模式。


#### 0 Java SDK

在所有安装前，确认已经安装了JAVA JDK，并设置了JAVA_HOME。这里推荐使用HomeBrew安装JDK，因为HomeBrew可以非常方便的管理多个版本[[Mac OS X and multiple Java versions](https://stackoverflow.com/questions/26252591/mac-os-x-and-multiple-java-versions)]。

* homebrew-cask 安装多个java版本
* jenv 管理多个java版本

```bash
# 1. Install jenv
brew install jenv
# 2. Add jenv to the bash profile
if which jenv > /dev/null; then eval "$(jenv init -)"; fi
# 3. Add jenv to your path
export PATH="$HOME/.jenv/shims:$PATH"
# 4. Tap "caskroom/versions"
brew tap caskroom/versions
# 5. Install the latest version of java
brew cask install java
# 6. Install java 7 or 8 (whatever you need)
brew cask install java6
#brew cask install java7
#brew cask install java8
# 7. Add each path to jenv one-at-a-time.
jenv add /Library/Java/JavaVirtualMachines/jdk-10.0.2.jdk/Contents/Home
# 8. Check if jenv registered OK
jenv versions
# 9. Set java version to use (globaly)
jenv global 10.0
# 10. Check java version
java -version
```


#### 1.1 配置ssh

配置ssh就是为了能够实现Hadoop的免密登录，这样方便远程管理Hadoop并无需登录密码在Hadoop集群上共享文件资源。如果你的机子没有配置ssh的话，在命令终端输入`ssh localhost`是需要输入你的电脑登录密码的。配置好ssh后，就无需输入密码了。

* 第一步就是在终端执行`ssh-keygen -t rsa`，之后一路`enter`键，当然如果你之前已经执行过这样的语句，那过程中会提示是否要覆盖原有的key，输入y即可。

* 第二步执行语句`cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`用于授权你的公钥到本地可以无需密码实现登录。

理论上这时候，你在终端输入`ssh localhost`就能够免密登录了。

#### 1.2 下载安装Hadoop

这时候brew的好处就体现出来了，你无需到Hadoop官网去找下载链接，只要在命令终端输入`brew install hadoop`等命令执行完，你就可以看到在`/usr/lcoal/Cellar`目录下就有了hadoop目录，表示安装成功。

#### 1.3 配置Hadoop

###### 1.3.1 配置HDFS地址和端口号

进入目录`/usr/local/Cellar/hadoop/3.1.0/libexec/etc/hadoop`，打开`core-site.xml`将`<configuration></configuration>`替换为

```
<configuration>
  <property>
     <name>hadoop.tmp.dir</name>  
     <value>/usr/local/Cellar/hadoop/hdfs/tmp</value>
    <description>A base for other temporary directories.</description>
  </property>
  <property>
     <name>fs.default.name</name>                                     
     <value>hdfs://localhost:9000</value>                             
  </property>                                                       
</configuration>
```

###### 1.3.2 配置mapreduce中`jobtracker`的地址和端口

在相同的目录下，你可以看到一个`mapred-site.xml`文件。同样将文件中的`<configuration></configuration>`替换为

```
<configuration>
      <property>
        <name>mapred.job.tracker</name>
        <value>localhost:9010</value>
      </property>
</configuration>
```

###### 1.3.3 修改hdfs备份数

在相同目录下，打开`hdfs-site.xml`，同样的替换为

```
<configuration>
   <property>
     <name>dfs.replication</name>
     <value>1</value>
    </property>
</configuration>
```

变量`dfs.replication`指定了每个HDFS默认备份方式通常为3, 由于我们只有一台主机和一个伪分布式模式的DataNode，将此值修改为1。


###### 1.3.4 格式化HDFS

这个操作相当于一个文件系统的初始化，执行命令`hdfs namenode -format`。 出现提示输入Y/N时要输入大写Y。

#### 1.4 配置Hadoop环境变量

因为我用的是iTerm2和zsh，所以打开`~/.zshrc`添加

```
export HADOOP_HOME=/usr/local/Cellar/hadoop/3.1.0/
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
```

再执行`source ~/.zshrc`以确保配置生效。配置的目的是方便在任意目录下全局开启关闭hadoop相关服务，而不需要到`/usr/local/Cellar/hadoop/3.0.0/sbin下执行`。

#### 1.5 启动/关闭Hadoop服务

启动/关闭HDFS服务的命令为

```
./start-dfs.sh          
./stop-dfs.sh
```


启动/关闭YARN服务

```
./start-yarn.sh        
./stop-yarn.sh
```

启动/关闭Hadoop服务(等效上面两个)

```
./start-all.sh   
./stop-all.sh
```

通过访问以下网址查看hadoop是否启动成功


* Node Information: [http://localhost:9870](http://localhost:9870)
* Resource Manager: [http://localhost:8088](http://localhost:8088)
* NodeManager : [http://localhost:8042](http://localhost:8042)

这里要注意的是在3.1.0版本中[http://localhost:50070](http://localhost:50070)转移到了[http://localhost:9870](http://localhost:9870).


#### 1.6 配置yarn


etc/hadoop/mapred-site.xml:

```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>

<configuration>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```


etc/hadoop/yarn-site.xml:

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```

启动

```
$ sbin/start-yarn.sh
```

### 2 安装Spark


有了前面这么多的准备工作，终于可以安装Spark了。到[Spark官网](http://spark.apache.org/downloads.html)下载你需要的Spark版本，注意这里我们看到需要有依赖的Hadoop，而且还让你选择Hadoop的版本，这里默认即可。下载完直接双击压缩包就会解压，将其重命名为`spark`放到`/opt`下面。

毫无疑问，我们还需要一个环境参数配置，打开`~/.zshrc`添加

```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
```

走到这一步，我们终于可以启动spark了，打开终端，输入`spark-shell --master local`, OK

### 3 安装 Hive

下载[hive](http://hive.apache.org/downloads.html)后解压到指定目录，并添加路径

```bash
export HIVE_HOME=/opt/apache-hive-x.y.z-bin
export PATH=$PATH:$HIVE_HOME/bin
```

这样，初步安装就完成了，键入hive启动 hive shell

```bash
$ hive hive>
```

### 4 安装Zookeaper

到[官网](https://zookeeper.apache.org/releases.html#download)下载zookeaper。

使用Zookeeper之前，需要有一个配置文件`conf/zoo.cfg`.

```text 
tickTime=2000
dataDir=/tmp/zookeeper
clientPort=2181
```

启动Zookeeper

```bash
bin/zkServer.sh start
```



### 5 安装Kafka


Kafka使用了scala和java语言，所以应该首先安装scala。到[scala官网](https://www.scala-lang.org/download/)下载scala，选择`Other ways to install Scala`，点击下载binary。

到[kafka官网](http://kafka.apache.org/downloads)下载kafaka，注意选择对应的scala版本。

### 6 安装HBase

到[官网](http://hbase.apache.org/downloads.html)下载Hbase，解压并设置好路径。


首先配置`conf/hbase-env.sh`文件，设置JAVA_HOME为正确的JAVA版本，设置export HBASE_MANAGES_ZK=false，使用我们自己的zookeeper。

配置`conf/hbase.site`文件，如下

```xml
<configuration>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://localhost:9000/hbase</value>
  </property>
  <property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/tmp/zookeeper</value>
  </property>
</configuration>
```

`hbase.rootdir`为hbase的根目录，参见Hadoop中coresite.xml文件，即配置的端口号。

> 站点： http://localhost:16010/

### 7 Vagrant方案


其实最简单的安装莫过于Vagrant方案了，搭建Vagrant虚拟机的过程见我的博文[vagrant搭建ubuntu](vagrant搭建ubuntu.md)，在选择配置文件的时候，选择这里的[配置文件](https://github.com/datacell/bigdatabase/tree/bartemius_v1.0.0/scripts/boxes/bartemius/1.0.0/Vagrantfile)。下载好配置文件后，在终端切换到配置文件所在文件夹，输入命令行

```bash
vagrant up
vagrant ssh
```
即可使用。当然使用其他的源或配置也可以，读者可以寻找适合自己的。





### 一键式：Cloudera

[Cloudera](https://www.cloudera.com)推出的QuickStart VM集成了几乎所有常用的大数据组件，开箱即用。在官网下载好对应的虚拟机版本后，导入虚拟机即可。


#### 网络连接

通过终端连接虚拟机会比较方便。打开虚拟机，选择设置(settings)，选择网络选项卡。网络连接可以参考[此篇博文](https://blog.csdn.net/weixin_37871174/article/details/71249359)