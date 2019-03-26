---
title: CentOS日志 
date: 2017-12-30
tags: [Linux]
---

Centos是追求稳定的程序员首选的Linux桌面版本。本文给出使用过程中最重要的几个问题的解决方案。

#### 美化[¶](https://techlarry.github.io/Miscellaneous/awesome%20Install/ubuntu%E6%97%A5%E5%BF%97/#_1)

Ubuntu的主题通常需要自定义，达到使用者的最熟悉的布局，能够最方便、最高效的使用。Centos可以直接拿过来使用，因为都是基于Gnome3构建的州面环境。建议使用Mac主题和字体，具体可以参考博文[给Ubuntu安装macOS主题](https://www.cnblogs.com/feipeng8848/p/8970556.html)。

#### 同步[¶](https://techlarry.github.io/Miscellaneous/awesome%20Install/ubuntu%E6%97%A5%E5%BF%97/#_2)

在Linux下文件同步没有免费的优秀方案。使用坚果云可以免费同步，但其一个月2GB的流量限制和不菲的套餐，使得大多数用户望而却步。而国外的优秀的网盘在大陆都被禁用或者连接速度极低。

选择Vultr搭建nextCloud私有云是非常好的方法，最便宜的套餐2.5美元一个月，网速非常快，亲测可以占满100MB带宽。而且搭建的SS服务器，不像阿里云，有着被封的风险。



#### 备份

rsync是非常好的一个备份工具。在创建好需要排除的备份列表后，使用命令

```bash
 sudo rsync -aAXhv --exclude-from=excluded / /store/backup/backup_20170322_3
```

可以非常简单的进行备份。

#### 文档



Typora是非常强大的markdown写作软件。可以在/usr/share/applications中添加文件typora.desktop，其内容为

```
[Desktop Entry]
Name=Typora
Exec=/opt/Typora-linux-x64/Typora %u
Type=Application
Icon=/opt/Typora-linux-x64/resources/app/asserts/icon/icon_128x128.png
Terminal=false
```

即可将其添加到桌面。

#### 视频

VLC和SMPlayer是Linux上最受欢迎的播放器。安装VLC视频播放器：

```
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
yum update
yum  install vlc
```





#### 作为服务器

CentOS广泛被用作搭建服务器的平台，而Apache服务器使用最广。

```
sudo yum install httpd -y #安装Apache服务
systemctl start httpd # 启动
systemctl enable httpd # 设置开机自启Apache服务
```

然后把网站放在`/var/www/html`下，打开浏览器，访问本地地址，就可以看到网站。