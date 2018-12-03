---
title: Intel Parallel Studio XE
date: 2017-12-03
tags: [IFORT]
---

Intel Paralle Studio 对于学生是可以免费申请的，点击[这里](https://software.intel.com/en-us/qualify-for-free-software/student)填上你的学校邮箱及相关信息即可。

申请界面如下，点击下面的`mac os`选项即可。
![free](http://or9a8nskt.bkt.clouddn.com/free.png)

## 安装

下载软件后，像安装一般软件一样，点击安装一步步往下走即可，在安装过程中需要输入申请到的激活码。

## 环境配置

以最新的2018 Release为例, 安装好以后在`.bashrc`中加上如下语句：

```
#intel
source /opt/intel/compilers_and_libraries_2018.0.104/mac/bin/compilervars.sh intel64
source /opt/intel/compilers_and_libraries_2018.0.104/mac/mkl/bin/mklvars.sh intel64
```

这样即配置好了相关的`IFORT`编译器以及`MKL`库。运行`ifort`命令和`-mkl`选项测试:

```
$ifort fortran_file.f90 -mkl
```




