---
title: 3 文件IO
toc: false
date: 2017-10-30
---

。。。。草稿。。。

内核使用3中数据结构表示文件，它们之间的关系决定了在文件共享方面一个进程对另一个进程可能产生的影响：

* 每个进程在进程表中都有一个记录项，记录项中包含一张打开文件描述符表，可将其视为一个向量，每个描述符占用一项。
an entry in the process table: 每一个打开的文件描述符对应一个entry，entry中的内容包括文件描述符标志位（file descriptor flags）和一个指向file table entry的指针；
file table：内核为所有打开的文件维护一个file table。每一个file table entry包括有：文件状态标志位（file status flag, such as read, write, append, sync和nonblocking）。
v-node和i-node: 每一个开打的文件都有一个v-node结构体，包括文件类型，指向操作函数的指针。对于大部分的文件，v-node还包含一个i-node结构。i-node的内容为打开文件时从硬盘上读取的信息，包括文件所有者，文件大小，文件内容存储在磁盘上的具体位置等。
下图表明了这三种内核数据结构的关系：

![](figures/process_table_entry.png)



如果两个独立进程个字打开了同一文件：

![](figures/two_independent_processes_with_the_same_file_open.png)




上图中，第一个进程打开文件，文件描述符为3， 第二进程打开同一个文件，文件描述符为4。

两个进程都有自己的file table entry，因为每个进程都需要维护自己的当前文件偏移量（current file offset）。

但是，也有可能多个独立进程的文件描述符指向同一个file table entry。这种情况发生在调用dup方法和fork系统调用时，父进程和子进程共享同一个file table entry。