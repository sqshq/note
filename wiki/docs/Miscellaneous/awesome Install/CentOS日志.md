---
title: CentOS日志 
date: 2017-12-30
tags: [Linux]
---

Centos是追求稳定的程序员首选的Linux桌面版本。下面以Centos 6.10, VirtualBox为例。


### 1 安装与基础配置

新建虚拟机。网络选择NAT和Host-Only选项。安装大概3分钟。重启后，创建用户名和密码。


#### 配置用户

为用户user添加sudo权限。修改/etc/sudoers文件

```text
root ALL=(ALL) ALL
user ALL=(ALL) ALL #user改成您的用户名
```

#### 修改主机名

默认安装的主机名往往非常怪异，需要修改。修改`/etc/sysconfig/network`文件中的HOSTNAME属性，重新启动后生效。



#### SSH
CentOS默认是不启动SSH服务的。所以需要安装，启动、配置。

```bash
# 安装SSH
yum install openssh-server
# 开启
service sshd start
# 开启服务的自动启动
chkconfig sshd on
``` 

配置SSH免密登陆, 首先利用ifconfig查看虚拟机Ip地址，例如192.168.56.103,然后将Ip地址增加到本机host文件中.

```text
192.168.56.103 centos
```

然后利用ssh-copy-id命令将密钥拷贝到虚拟机，过程中选择yes，并输入密码。

```bash
ssh-copy-id centos
```

然后在主机上登陆虚拟机

```bash
ssh centos
```



#### 源

配置国内的阿里、网易的安装源能够大大加快包的下载速度。

```bash
# 备份，为了更新失败时切换回去
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
# 进入yum源配置文件夹
cd /etc/yum.repos.d/
# 根据centos版本下载对应的新源
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
#生成缓存，会把新下载CentOS-Base.repo源生效。
yum makecache
```
#### oh-my-zsh

使用流行的oh-my-zsh使目录跳转、文字输入更加快捷。

```
# zsh
yum -y install zsh
yum -y install  git
# 安装oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

由于往往有多台虚拟机，所以希望显示[登陆用户，主机名，路径]这样的信息，否则很容易搞混虚拟机，产生误操作。在`～/.zshrc`文件中添加

```bash
PROMPT='%{$fg_bold[yellow]%}%n@%m ${ret_status} %{$fg[cyan]%}%d%{$reset_color%} $(git_prompt_info)'
```

使用`source ~/.zshrc`生效。

#### mysql

启动mysql服务

```bash
sudo service mysqld start
```

设置管理员密码

```bash
mysqladmin -u root  password 'new-password';
```

如果想重新设置密码，用原先密码登陆数据库

```sql
#使用mysql数据库        
 use mysql；
#修改          
update user set password=password("new-password") where user="root";
#刷新权限        
flush privileges;
```

设置mysql开机启动

```bash
chkconfig mysqld on
```

#### 后台运行

Centos虚拟机的操作一般是通过主机的终端来操作的，所以就希望虚拟机在后台运行。

```
# 开启虚拟机在后台运行
VBoxManage startvm <vm_name> -type headless
```