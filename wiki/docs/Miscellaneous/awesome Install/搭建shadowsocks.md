---
title: 搭建shadowsocks
toc: true
date: 2018-01-01
tags: [ss]
---

## Shadowsocks简介

`Shadowsocks`(ss) 是由 [Clowwindy](https://github.com/Clowwindy) 开发的一款软件，其作用本来是加密传输资料。当然，也正因为它加密传输资料的特性，使得GFW没法将由它传输的资料和其他普通资料区分开来（上图），也就不能干扰我们访问那些「不存在」的网站了。

#### VPS简介

VPS(Virtual private server) 译作虚拟专用伺服器。你可以把它简单地理解为一台在远端的强劲电脑。当你租用了它以后，可以给它安装操作系统、软件，并通过一些工具连接和远程操控它。

[「搬瓦工」](https://bandwagonhost.com/)是一家 VPS 服务器提供商，有美国、亚洲、欧洲等多地的 VPS。它家的服务器以性价比高、访问速度快闻名。

#### Linux 和 SSH简介

Linux是免费开源的操作系统，大概被世界上过半服务器所采用。有大量优秀的开源软件可以安装，上述 `Shadowsocks` 就是其一。你可以通过命令行来直接给Linux 操作系统「下命令」，比如 `$ cd ~/Desktop` 就是进入你根目录下的 Desktop 文件夹。

而 SSH 是一种网络协议，作为每一台 Linux 电脑的标准配置，用于计算机之间的加密登录。当你为租用的 VPS 安装 Linux 系统后，只要借助一些工具，就可以用 SSH 在你自己的 Mac/PC 电脑上远程登录该 VPS 了。



## 部署 Shadowsocks

`Shadowsocks` 需要同时具备客户端和服务器端，所以它的部署也需要分两步。

### 部署 Shadowsocks 服务器端

这里使用[teddysun](https://teddysun.com/342.html) 的一键安装脚本。

以下是3条命令，每次输入一行、回车，等待屏幕上的操作完成后再输入下一条。

```bash
wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks.sh
chmod +x shadowsocks.sh
./shadowsocks.sh 2>&1 | tee shadowsocks.log
```

最后一步输完，你应该会看到下图中内容──是要你为`Shadowsocks` 服务设置一个密码。

输好回车后会让你选择一个端口，输入1–65535间的数字都行。

遵照上图指示，按任意键开始部署`Shadowsocks`。这时你什么都不用做，只需要静静地等它运行完就好。结束后就会看到你所部署的`Shadowsocks`的配置信息。

记住其中黄框中的内容，也就是服务器 IP、服务器端口、你设的密码和加密方式。

#### 3.2 TCP Fast Open

实际上只要具备上述四个信息，你就可以在自己的任意设备上进行登录使用了。但是为了更好的连接速度，你还需要多做几步。

首先是打开 TCP Fast Open，输入以下命令，意为用 nano 这个编辑器打开一个文件。

```
nano /etc/rc.local
```

用方向键把光标移到最末端，粘贴下面这一行内容，然后按 `Ctrl + X`退出。

```
echo 3 > /proc/sys/net/ipv4/tcp_fastopen
```

输入“Y”并回车确认退出。

然后依法炮制，输入：

```
nano /etc/sysctl.conf
```

在文末加上下面的内容，保存退出。

```
net.ipv4.tcp_fastopen = 3
```

再打开一个`Shadowsocks` 配置文件。

```
nano /etc/shadowsocks.json
```

把其中 “fast_open” 一项的 `false` 替换成 `true`。

```
"fast_open":true
```

如果你希望添加多用户的话，可以将 “password” 字段如下图修改。其中，”22345":”password1"意为该用户使用 22345 端口、以“password1”为密码连接登录`Shadowsocks`。

保存退出。最后，输入以下命令重启 `Shadowsocks`。

```bash
/etc/init.d/shadowsocks restart
```

#### 3.3 安装`Shadowsocks`客户端

相比服务器端的安装，客户端的安装就简单了许多。首先，根据操作系统下载相应的客户端。

* [Mac 版客户端下载](https://sourceforge.net/projects/shadowsocksgui)
* [Win 版客户端下载](https://github.com/shadowsocks/shadowsocks-windows/releases)

打开客户端，在「服务器设定」(Servers-Open Server Preferences)里新增服务器。然后依次填入服务器 IP、服务器端口、你设的密码和加密方式。

然后启用代理，就可以实现科学上网了。


