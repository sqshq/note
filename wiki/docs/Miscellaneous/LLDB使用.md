---
title: LLDB使用
toc: true
date: 2017-10-30
tags: [LLDB]
top: 6
---


[`lldb`](http://lldb.llvm.org)是一个开源的下一代高性能调试器。LLDB是MAC上的默认调试器，支持调试C、Objective-C和C++语言。


可以比较LLDB与GDB命令的[对照表](http://lldb.llvm.org/lldb-gdb.html)。

### 命令

```
调试器命令:
 
  apropos           -- 列出与单词或主题相关的调试器命令
  breakpoint        -- 在断点上操作的命令 (详情使用'help b'查看)
  bugreport         -- 用于创建指定域的错误报告
  command           -- 用于管理自定义LLDB命令的命令
  disassemble       -- 拆分当前目标中的特定说明。 默认为当前线程和堆栈帧的当前函数
  expression        -- 求当前线程上的表达式的值。 以LLDB默认格式显示返回的值
  frame             -- 用于选择和检查当前线程的堆栈帧的命令
  gdb-remote        -- 通过远程GDB服务器连接到进程。 如果未指定主机，则假定为localhost
  gui               -- 切换到基于curses的GUI模式
  help              -- 显示所有调试器命令的列表，或提供指定命令的详细信息
  kdp-remote        -- 通过远程KDP服务器连接到进程。 如果没有指定UDP端口，则假定端口41139
  language          -- 指定源语言
  log               -- 控制LLDB内部日志记录的命令
  memory            -- 用于在当前目标进程的内存上操作的命令
  platform          -- 用于管理和创建平台的命令
  plugin            -- 用于管理LLDB插件的命令
  process           -- 用于与当前平台上的进程交互的命令
  quit              -- 退出LLDB调试器
  register          -- 命令访问当前线程和堆栈帧的寄存器
  script            -- 使用提供的代码调用脚本解释器并显示任何结果。 如果没有提供代码，启动交互式解释器。
  settings          -- 用于管理LLDB设置的命令
  source            -- 检查当前目标进程的调试信息所描述的源代码的命令
  target            -- 用于在调试器目标上操作的命令
  thread            -- 用于在当前进程中的一个或多个线程上操作的命令
  type              -- 在类型系统上操作的命令
  version           -- 显示LLDB调试器版本
  watchpoint        -- 在观察点上操作的命令
 
 
缩写命令 (使用 'help command alias'查看更多信息):
 
  add-dsym  -- ('target symbols add')  通过指定调试符号文件的路径，或使用选项指定下载符号的模块，将调试符号文件添加到目标的当前模块中的一个
  attach    -- ('_regexp-attach')  通过ID或名称附加到进程
  b         -- ('_regexp-break')  使用几种简写格式之一设置断点
  bt        -- ('_regexp-bt')  显示当前线程的调用堆栈。通过数字参数设置最多显示帧数。参数“all”显示所有线程
  c         -- ('process continue')  继续执行当前进程中的所有线程
  call      -- ('expression --')  计算当前线程上的表达式,使用LLDB的默认格式显示返回的值
  continue  -- ('process continue')  继续执行当前进程中的所有线程
  detach    -- ('process detach')  脱离当前目标进程
  di        -- ('disassemble')  拆分当前目标中的特定说明。 默认为当前线程和堆栈帧的当前函数
  dis       -- ('disassemble')  同上
  display   -- ('_regexp-display')  在每次停止时计算表达式（请参阅'help target stop-hook'）
  down      -- ('_regexp-down')  选择一个新的堆栈帧。默认为移动一个帧，数字参数可以指定值
  env       -- ('_regexp-env')  查看和设置环境变量的简写
  exit      -- ('quit')  退出LLDB调试器
  f         -- ('frame select')  从当前线程中通过索引选择当前堆栈帧（参见'thread backtrace'）
  file      -- ('target create')  使用参数作为主要可执行文件创建目标
  finish    -- ('thread step-out')  完成当前堆栈帧的执行并返回后停止。 默认为当前线程
  image     -- ('target modules')  用于访问一个或多个目标模块的信息的命令
  j         -- ('_regexp-jump')  将程序计数器设置为新地址
  jump      -- ('_regexp-jump')  同上
  kill      -- ('process kill')  终止当前目标进程
  l         -- ('_regexp-list')  使用几种简写格式之一列出相关的源代码
  list      -- ('_regexp-list')  同上
  n         -- ('thread step-over')  源级单步执行、步进调用，默认当前线程
  next      -- ('thread step-over')  同上
  nexti     -- ('thread step-inst-over')  指令级单步执行、步进调用，默认当前线程
  ni        -- ('thread step-inst-over')  同上
  p         -- ('expression --')  计算当前线程上表达式的值，以LLDB默认格式显示返回值
  parray    -- ('expression -Z %1   --')  同上
  po        -- 计算当前线程上的表达式。显示由类型作者控制的格式的返回值。
  poarray   -- ('expression -O -Z %1    --')  计算当前线程上表达式的值，以LLDB默认格式显示返回值
  print     -- ('expression --')  同上
  q         -- ('quit')  退出LLDB调试器
  r         -- ('process launch -X true --')  在调试器中启动可执行文件
  rbreak    -- ('breakpoint set -r %1')  在可执行文件中设置断点或断点集
  repl      -- ('expression -r  -- ')  E计算当前线程上表达式的值，以LLDB默认格式显示返回值
  run       -- ('process launch -X true --')  在调试器中启动可执行文件
  s         -- ('thread step-in')  源级单步执行、步进调用，默认当前线程
  si        -- ('thread step-inst')  指令级单步执行、步进调用，默认当前线程
  sif       -- 遍历当前块，如果直接步入名称与TargetFunctionName匹配的函数，则停止
  step      -- ('thread step-in')  源级单步执行、步进调用，默认当前线程
  stepi     -- ('thread step-inst')  指令级单步执行、步进调用，默认当前线程
  t         -- ('thread select')  更改当前选择的线程
  tbreak    -- ('_regexp-tbreak')  使用几种简写格式之一设置单次断点
  undisplay -- ('_regexp-undisplay')  每次停止时停止显示表达式（由stop-hook索引指定）
  up        -- ('_regexp-up')  选择较早的堆栈帧。 默认为移动一个帧，数值参数可以指定任意数字
  x         -- ('memory read')  从当前目标进程的内存中读取

```


### LLDB语法

LLDB的基本语法如下：

```
<command> [<subcommand> [<subcommand>...]] <action> [-options [option-value]] [argument [argument...]]
```

例如：

```
breakpoint set -f test.m -l 18


command: breakpoint 添加断点命令
action: set 表示设置断点
option: -f 表示在某文件添加断点
arguement: test.m表示要添加断点的文件名为test.m
option: -l 表示某一行
arguement: 18 表示第18行
```


#### expression

expression命令的作用是执行一个表达式，并将表达式返回的结果输出:

```
expression <cmd-options> -- <expr>
```


