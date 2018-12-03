---
title: VSCode
toc: true
date: 2017-10-30
tags: [Editor]
---

Vscode(Visual Studio Code)是一个轻量且强大的代码编辑器。内置JavaScript、TypeScript和Node.js支持，而且拥有丰富的插件生态系统，可通过安装插件来支持C++、C#、Python、PHP等其他语言。

![vscode界面](http://or9a8nskt.bkt.clouddn.com/vscode_demo.png)


## C++的使用

在Vscode中使用C++语言进行编译和调试之前，需要安装一些额外的工具、配置一些文件。

### 插件

　　打开VScode后，按下组合键“⇧⌘X”，打开扩展，输入`C/C++`，安装`C/C++`、`C/C++ Clang Command Adapter`，安装完成后，重启VScode让插件生效。



### 配置文件

两个配置文件在当前工作目录的`.vscode`隐藏文件夹下。


`launch.json`配置文件(下拉菜单 Debug- Open/Add Configuration)，用于调试程序

```C
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(lldb) Launch",  // 配置名称，将会在启动配置的下拉菜单中显示
            "type": "cppdbg",  // 配置类型，这里只能为cppdbg
            "request": "launch", // 请求配置类型，可以为launch（启动）或attach（附加）
            "program": "${workspaceFolder}/tsh", // 将要进行调试的程序的路径
            "args": [], // 程序调试时传递给程序的命令行参数，一般设为空即可
            "stopAtEntry": false, // 设为true时程序将暂停在程序入口处，可以设置为true
            "cwd": "${workspaceFolder}", // 调试程序时的工作目录
            "environment": [],   // （环境变量）
            "externalConsole": true, // 调试时是否显示控制台窗口，一般设置为true显示控制台
            "MIMode": "lldb",  // 指定连接的调试器，可以为gdb或lldb。
            "preLaunchTask": "compile" 
            // 调试会话开始前执行的任务，一般为编译程序。与tasks.json的label相对应
        },

    ],
    "compounds": [],
}
```

`tasks.json` 配置文件(下拉菜单Tasks-configure Tasks)，用于编译程序

```JSON
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "compile", // 任务名称，与launch.json的preLaunchTask相对
            "type": "shell",
            "command": "make", // 编译命令，g++/make 等
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher":"$gcc"
        }
    ]
    
}
```


### 更简单的方法

安装 Code Runner 这个插件，不用进行任何配置就能直接编译并运行(Control+Option+N)，默认情况下使用的是GCC和G++。

![vscode-runcoder](http://or9a8nskt.bkt.clouddn.com/vscode-runcoder.png)

