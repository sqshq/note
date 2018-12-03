---
title: vagrant搭建ubuntu
date: 2017-12-30
author: larry
tags: [vagrant, ubuntu]
---

`Vagrant` 是一款用来管理虚拟机的工具，可以构建虚拟开发环境的。`Vagrant`封装一个`Linux`(Ubuntu/CentOS等)的开发环境，分享给其他开发人员。而其他人可以在自己喜欢的桌面系统（Mac/Windows/Linux）上开发程序，代码却能统一在封装好的环境里运行，可以把开发环境配制成与生产环境一样。



# Mac terminal下的`Vagrant`和 `Ubuntu`环境的安装

`Vagrant`可以从下面网页链接下载, 选择 ：
[https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html)

安装好了Vagrant，后然后安装Virtualbox，请到[下载网页](https://www.virtualbox.org)直接下载需要的版本。

下面安装`Ubuntu`
（1）打开Mac terminal，运行下面命令，安装`Ubuntu`。

```bash
$ vagrant init ubuntu/trusty64
$ vagrant up
```

其他的系统版本选择见[https://app.vagrantup.com/boxes/search](https://app.vagrantup.com/boxes/search), 最常用的是`ubuntu/trusty64`和`ubuntu/xenial64`.

键入`vagrant up`后，`vagrant`会下载您指定的操作系统，然后进行安装。整个下载安装过程一般在5分钟左右。

(2)连接到安装好的`Ubuntu`

```
// 这个命令会通过ssh的方式连接虚拟机。
$ vagrant ssh 
```

## 分享文件

打开位于配置文件`Vagrantfile`，配置其中的`config.vm.synced_folder`参数,第一个参数是需要位于主机需要同步的文件夹，可以是相对地址。第二个参数是虚拟机上的需要同步的文件夹，必须是绝对地址。

```
Vagrant.configure("2") do |config|
  # other config here

  config.vm.synced_folder "src/", "/home/shared"
end
```

NOTE: By default, Vagrant will share your project directory (the directory with the Vagrantfile) to /vagrant.


## 安装和配置`ubuntu`

这其实和正常的`ubuntu`系统一样的。一般通过

```
sudo apt-get install software
```

安装软件。

### 安装常用软件

```bash
sudo apt-get update
sudo apt-get install git
sudo apt-get install gdb
sudo apt-get install zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"  // install on-my-zsh
```

**`vagrant`虚拟机默认密码是`vagrant`**


## 常用命令

```
vagrant box add {作者/系统名} {box文件路径}  #添加虚拟机
vagrant box remove {作者/系统名}  #删除虚拟机
vagrant init {作者/系统名}  #初化化虚拟机此时会生成一个Vagrantfile文件
vagrant box list #查年现有的虚拟机
vagrant status  #查看所有虚拟机状态
vagrant halt {作者/系统名}  #关闭指定虚拟机
vagrant provision  #当修改完配制后只要执行一下此命令就可以对虚拟机进行相关修改
vagrant reload #重启虚拟机
vagrant ssh  #使用ssh的方式连接虚拟机
vagrant up  #启动虚拟机
vagrant version #查看版本信息
vagrant plugin {插件} #安装插件
vagrant package {作者/系统名} #把你的虚拟机打包在box可以分享给你拉小人类伴们一起使用，非常方便
vagrant resume  #恢复虚拟机
vagrant suspend  #暂停虚拟机
vagrant destroy  #销毁当前虚拟机
```

## 加载已经下载/存在的虚拟机

有时候虚拟机已经存在，或者你通过其他途径下载虚拟机更快，或者你从朋友那里拷贝了一个虚拟机，那么可不可以直接加载呢？

当然是可以的，而且一句话搞定，例如添加文件名为`path_to_file.box`的虚拟机以`my_box_name`的名字展现：

```bash
vagrant box add my_box_name file:///path_to_file.box
```


