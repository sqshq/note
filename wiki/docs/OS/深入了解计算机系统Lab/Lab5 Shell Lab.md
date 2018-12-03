---
title: Lab5 Shell Lab
toc: true
date: 2017-12-30
tags: [CSAPP]
top: 5
---


Shell Lab需要我们完成一个简单的shell程序。shell是一个交互的命令行界面的解析器。著名的shell程序有Bourne shell (`sh`)、Bourne-Again shell(`bash`)、Z shell (`zsh`)等。shell的框架已经写好，主要需要完成以下函数：

* `void eval(char *cmdline)`：解析命令与执行
* `void sigchld_handler(int sig)`：`SIGCHLD` 信号处理程序
* `void sigtstp_handler(int sig)`：`SIGTSTP`(ctrl-z) 信号处理程序
* `void sigint_handler(int sig)`：`SIGINT`(ctrl-c) 信号处理程序

## 简介

shell程序`tsh.c`应该具备以下功能：

* 每一行会输出一个 `tsh>`，然后等待用户输入
* 用户的输入包括`name`加上零个或多个参数，这些参数之间用一个或多个空格分隔。如果`name`是内置命令，那么直接执行，否则需要新建一个子进程，并在子进程中完成具体的工作
* 不需要支持管道，但是需要支持输入输出重定向，如 `tsh> /bin/cat < foo > bar`（必须支持在同一行重定向输入以及输出)， 也需要支持内置命令的重定向，如 `tsh> jobs > foo`
* 输入 `ctrl-c` 或 `ctrl-z` 会给当前的前台进程（包括其子进程）发送 `SIGINT`(`SIGTSTP`) 信号，如果没有前台任务，那么这俩信号没有任何效果
* 如果输入的命令以 & 结尾，那么就要以后台任务的方式执行，否则按照前台执行
* 每个job都有其进程ID(`PID`)和job ID(`JID`)都是由`tsh`指定的正整数，`JID`以`%`开头（如 `%5` 表示 `JID`为5，而5则表示`PID`为5，这部分已提供了辅助函数
* 支持的内置命令有
    * `quit` 退出shell
    * `jobs` 列出所有的后台任务
    * `bg job` 给后台job发送`SIGCONT` 信号来继续执行该任务，具体的job数值可以是PID或JID
    * `fg job` 给前台job发送`SIGCONT` 信号来继续执行该任务，具体的job数值可以是PID或JID
* `tsh`应该回收所有的僵尸进程，如果任何job因为接收了没有捕获的信号而终止，`tsh`应该识别出这个时间并且打印出`JID`和相关信号的信息。

### 提示

* 不要使用 `sleep()` 来同步
* 不要使用忙等待 `while(1)`;
* 使用`sigsuspend`来同步
* 竞争条件
* 僵尸进程回收（注意竞争条件以及正确处理信号）
* 等待前台任务（仔细思考怎么样才是好的方式）
* 不要假定进程的执行顺序
* 子进程挂掉的时候应该在一个限定时间内被回收
* 不要在多个地方调用`waitpid`，很容易造成竞争条件，也会造成程序过分复杂
* 不要使用任何系统调用来管理 `terminal group`
* `waitpid`, `kill`, `fork`, `execve`, `setpgid`, `sigprocmask` 和 `sigsuspend` 都非常有用，`waitpid` 中的 `WUNTRACED` 和 `WNOHANG `选项也是如此。
* 遇到不清晰的用 `man` 来查看细节
* 实现 `signal handler` 的时候注意给全部的前台进程组发送 `SIGINT` 和 `SIGTSTP` 信号
* 在 `kill` 函数中使用 `-pid` 的格式作为参数
* 在shell等待前台工作完成时，需要决定在`eval`及`sigchold handler` 具体的分配，这里有一定技巧
* 在函数 `eval` 中，在 `fork` 出子进程之前，必须使用 `sigprocmask` 来阻塞 `SIGCHLD, `SIGINT` 和 `SIGTSTP` 信号，完成之后再取消阻塞。调用 `addjob` 的时候也需要如此。注意，因为子进程也继承了之前的各种状态，所以在子进程中调用 `exec` 执行新程序的时候注意需要取消阻塞，同样也需要恢复默认的 `handler`（shell 本身已经忽略了这些信号）
* 不要使用 `top`, `less`, `vi`, `emacs` 之类的复杂程序，使用简单的文本程序如：`/bin/cat`, `/bin/ls`, `/bin/ps`, `/bin/echo`
* 因为毕竟不是真正的 shell，所以在`fork`之后，`execve`之前，子进程需要调用 `setpgid(0, 0)`，这样就把子进程放到一个新的进程组里。这样就保证我们的shell前台进程组中唯一的进程，当按下 `ctrl-c`时，应该捕获`SIGINT`信号并发送给对应的前台进程组中。

## gdb 操作

可能用到的gdb相关操作：

（1）改变gdb信号处理的设置 ：设置gdb接收到SIGINT时不要停止、打印、传递给调试目标程序 。
         (gdb) handle SIGINT nostop print pass 
（2）使用gdb命令直接向调试的应用程序发送信号 ：首先在你希望发送信号的语句处设置断点，然后运行程序，当停止到断点所在位置后，用gdb的signal命令发送信号给调试目标程序 。
          (gdb) signal SIGINT 

（3）调试多进程程序：mode到可选值为parent和child表示fork之后调试父进程还是子进程。

          (gdb) set follow-fork-mode mode
          
          
## dup/dup2 I/O重定向


```C
dup, dup2 -- duplicate an existing file descriptor
#include <unistd.h>
int dup(int newfd);
int dup2(int newfd, int oldfd);
```

`dup2`函数复制描述符表项`oldfd`到描述符表项`newfd`，覆盖描述符表项`newfd`以前的内容。如果`newfd`已经打开了，`dup2`会在复制`oldfd`之前关闭`newfd`。


