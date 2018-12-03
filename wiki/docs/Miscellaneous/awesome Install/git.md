---
title: git
toc: true
date: 2017-12-30
tags: [Git]
---

## 安装
`git`在mac上已经默认安装了，使用之前只需要简单的配置即可。

### 设置Git的user name和email

把下面的`username`和`email`替换成您的`Github`的用户名和地址。

```
$ git config --global user.name "username"
$ git config --global user.email "email"
```

### 生成密钥

```
$ ssh-keygen -t rsa -C "email"
```

默认连续3个回车， 最后得到了两个文件：`～/.ssh/id_rsa`和`~/.ssh/id_rsa.pub`。注意这两个文件的保存地址(会输出在终端上，等下要用)。

其中公钥保存在`id_rsa.pub`内。

### 添加密钥到ssh-agent

`ssh-agent`是一种控制用来保存公钥身份验证所使用的私钥的程序，其实`ssh-agent`就是一个密钥管理器，运行`ssh-agent`以后，使用`ssh-add`将私钥`id_rsa`交给`ssh-agent`保管，其他程序需要身份验证的时候可以将验证申请交给`ssh-agent`来完成整个认证过程。

```
$ eval "$(ssh-agent -s)"
```

添加生成的 `SSH key` 到 `ssh-agent`。

```
$ ssh-add ~/.ssh/id_rsa
```

### 登陆`Github`, 添加`ssh`

复制`id_rsa.pub`文件里面的内容。

```
more .ssh/id_rsa.pub
```

打开[`GitHub`](https://github.com),依次选择`settings`-`SSH and GPG keys`-`New SSH key`。进入到如下界面，输入任意`Title`，在`Key`输入框内粘贴上`id_rsa.pub`文件里面的内容。

![add_ssh_key](http://or9a8nskt.bkt.clouddn.com/add_ssh_key.png)

测试一下是否可以连接：

```
ssh -T git@github.com
```

测试成功后，在github页面的SSH keys上的钥匙符号会显示为绿色：

![gree](http://or9a8nskt.bkt.clouddn.com/gree.png)





