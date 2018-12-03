---
title: Lab4 Cache Lab
toc: true
date: 2017-12-30
tags: [CSAPP]
top: 4
---


CMU 15-213 Lab4 Cache Lab

* [Lab 下载地址](http://csapp.cs.cmu.edu/3e/labs.html)
* [Recitation讲解](https://scs.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx#folderID=%22b96d90ae-9871-4fae-91e2-b1627b43e25e%22)


Cache Lab可以帮助理解缓存对C程序的影响。Lab包括两部分，第一部分用C语言写一个缓存模拟器，第二部分写一个小型矩阵的转置函数，使缓存不命中降到最低。

## Part A

Part A的任务是写一个C语言缓存模拟器，输入Valgrind的`trace file`，输出缓存命中次数hit_count，缓存不命中次数miss_count,驱逐次数eviction_count.

### Trance File

要写这样一个缓存模拟器，我们肯定首先要了解输入的内容。Valgrind的`--trace-mem=yes`选项可以追踪内存：

```
$ valgrind --log-fd=1 --tool=lackey -v --trace-mem=yes ls -l

 L 04224488,4
I  0400a0ab,8
 S ffefffdf8,8
I  0400a0b3,5
 M ffefffd48,8
```

上面这个命令用valgrind打印出了在执行`ls -l`过程中内存的使用情况。输出的格式是

```
[空格] 操作符(I/L/S/M) 地址, 字节大小
[space] operator(I/L/S/M) address, size
```
操作符有四种I/L/S/M，分别代表指令加载(I)/数据加载(L)/数据存储(S)/M(数据修改)。其中指令加载(I)前面没有空格。

### 命令行参数

接下来还需要了解命令行参数，缓存模拟器可以根据命令行参数设置成不同的规格。例如：

```bash
./csim-ref -s 4 -E 1 -b 4
```

其中`-s, -E, -b`分别表示：

* `-s <s>` 有$S=2^s$个组，
* `-E <E>` E个相联度，即每组E行
* `-b <b>` 每一行是由一个$B=2^b$字节的数据块组成。

所以`-s 4 -E 1 -b 4`表示，高速缓存有16个组，每组1行，每一行是由一个16个字节的数据块组成的。


解析命令行参数可以使用`getopt`函数，在使用时包含`unistd.h`头文件。可使用`man 3 getopt`查询函数用法和示例。

```
getopt -- get option character from command line argument list
getopt(int argc, char * const argv[], const char *optstring);
```

字符串`optstring`可以下列元素，

* 单个字符，表示选项，
* 单个字符后接一个冒号：表示该选项后必须跟一个参数。参数紧跟在选项后或者以空格隔开。该参数的指针赋给optarg。
* 单个字符后跟两个冒号, 这时选项的参数是可选的(可有可无)。有参数时，参数与选项之间不能有空格

所以输入时的处理可以如下：

```
while((opt=getopt(argc, argv, "s:E:b:t:v::")) != -1)
{
	printf("-%c %s ", opt, optarg);
	switch (opt)
	{
		case 's':
			s = atoi(optarg);
			break;
		case 'E':
			E = atoi(optarg);
			break;
		case 'b':
			b = atoi(optarg);
			break;
		case 't':
			filename = optarg;
			break;
		default:
			printf("Wrong argumet \n");
			break;
	}
}
```

### 读取文件

用`getopt()`函数处理完命令行参数，也就知道了需要模拟的高速缓存的具体细节。下一步就是读取Valgrind文本文件，进行处理。 使用`fscanf()`函数可以很方便的从文件中读取内容。同样的用`man 3 fscanf`可以查询`fscanf()`的具体用法：

```C
int fscanf(FILE *stream, const char *format, ...);
```

`fscanf()`依次输入`trace file`中的`[space]operator/address/size`。由于地址的长度大小不一定，所以用`malloc()`动态分配。`fscanf()`中的`%[^,]`表示读入任意多的字符，直到遇到逗号(`,`)为止。

```C
while(fscanf(fp, " %c %[^,],%c", &operator, address, &size)==3)
```

注意在调用`fscanf()`函数时，要确认函数返回值是否等于要赋值的参数数量`fscanf()==3`。

### 模拟缓存

前面的几步都是为了这一步做好准备，现在知道了缓存的细节，读取了`trace file`, 下一步就是要构造一个缓存了。可以用一个多维数组构造缓存，其中一维表示组，一维表示行，另一维表示块。其实它也就是一个二维的缓存行，每一行有$B$字节，有$S$组，每组$E$行，一共有$S\times E$行。那么，我们先构造一个缓存行，然后再构造一个$S\times E$行的数组。

```
struct cacheline {
     int valid_bit; // if 1, valid
     unsigned tag; // tag
     
}
struct cache_line cache[S][E]
```

接下来的一个难点是如何部署LRU(Least Recently Used replacement policy)策略。一个好的方法是使用队列, 在节点中存放地址。

```C
#define QUEUE_TYPE cacheline

/* define node of queue*/
typedef struct queue_node {
	QUEUE_TYPE* value;
	struct queue_node* next;
} node;


/* define a queue */
typedef struct {
	int size;
	int full_size;
	node *head;
	node *tail;
} queue;

/* create a queue */
queue* create_queue(queue* q, int full_size)
{
	q = malloc(sizeof(queue));
	if (q==NULL)
	{
		printf("Memory error");
		exit(1);
	}
	q->size = 0;
	q->full_size = full_size;
	return q;
}

/* pop_queue */
QUEUE_TYPE* pop(queue *q)
{
	node *old_head;
	QUEUE_TYPE* old_value; 
	old_head = q->head;
	q->head = q->head->next;
	q->size -= 1;
	old_value = old_head->value;
	free(old_head);
	return old_value;
}


/* queue is empty */
int is_empty(queue *q)
{
	return (q->size == 0); 
}

/* queue is full */
int is_full(queue *q)
{
	return (q->size == q->full_size);
}
/* destory_queue */
void destroy(queue *q)
{	
	while (!is_empty(q))
		pop(q);
}

/* push_queuq */
QUEUE_TYPE* push(queue *q, QUEUE_TYPE* value)
{
	/* create a new node */
	node *new_node;
	new_node = malloc(sizeof(node));
	new_node->value = value;

	if (is_empty(q))
	{
		q->head = new_node;
		q->tail = new_node;
		q->size = 1;
		return value;
	}
	else
	{
		q->tail->next = new_node;
		q->tail = new_node;
		q->size = q->size + 1;
		if ((q->size) > (q->full_size))
			return pop(q);
	} 
}
```

下面就是细节的处理了，包括内存分配，从地址中提取标记，组索引，块偏移，把输入的16进制字符串转化为数字。这些都非常简单，最终主程序如下：

```
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "queue.h"

/* 将十六进制字符串转换为十进制整数 */
int hexstr2int(char * HexStr)
{
	int iResult = 0, iCycle = 1;

    //判断字符串是否合法
	if( !strlen( HexStr ) )
	{
		return -1;
	}

    //指针变量p指向字符串的末尾
	char * p = HexStr + strlen( HexStr );

	while( (--p+1) != HexStr )
	{
		if ( *p >= '0' && *p <= '9' )
			iResult += ( *p - '0' )*iCycle;
		else if ( *p >= 'A' && *p <= 'F' )
			iResult += ( *p - 'A' + 10 )*iCycle;
		else if ( *p >= 'a' && *p <= 'f' )
			iResult += ( *p - 'a' + 10 )*iCycle;
		iCycle <<= 4;
	}
	return iResult;
}


int main(int argc, char *argv[])
{
	int opt;
	int s, E, b; /* cache parameter */
	int S, B;
	int miss=0, hit=0, eviction=0; /* count on miss/hit/eviction */
	int i, j, flag=0; /* dummy variable */
	char *filename;
	queue *q, *qi; 

	cacheline **cache; // every cache has S set, every set has E lines
	cacheline cacheij, *cacheij_address; //dummy variable

	FILE *fp;
	char operator, *address, size;
	unsigned d_address, tag, set, bit; // 地址，标记(t)，组索引(s)，块偏移(b) 
	
	while((opt=getopt(argc, argv, "s:E:b:t:v::")) != -1)
	{
		printf("-%c %s ", opt, optarg);
		switch (opt)
		{
			case 's':
			s = atoi(optarg);
			break;
			case 'E':
			E = atoi(optarg);
			break;
			case 'b':
			b = atoi(optarg);
			break;
			case 't':
			filename = optarg;
			break;
			default:
			printf("Wrong argumet \n");
			break;
		}
	}
	printf("\n");

	S = 2 << s;
	B = 2 << b;

	/* allocate memory */
	cache = (cacheline **) malloc(sizeof(cacheline*) *S);
	address = (char *) malloc(sizeof(char) * 16);
	q = (queue *) malloc(sizeof(queue) * S);
	for (qi=q, i=0; i<S; qi++, i++)
	{
		cache[i] = (cacheline *) malloc(sizeof(cacheline) *E); /* 每一个缓存组都有E个缓存行 */
		qi->full_size = E;
		for (j=0; j< E; j++)
		{
			/* 设定缓存行 */
			cacheij = cache[i][j];
			cacheij.valid_bit = 0;
			cacheij.tag = i*E+j;
		}
	}

    /* open file */
	fp = fopen(filename, "r");
	if(fp == NULL)
	{
		printf("Open filefailure!");
		exit(1);
	}
	else
	{
		/* read trace data */
		while(fscanf(fp, " %c %[^,],%c", &operator, address, &size)==3)
		{
			printf("%c %s,%c ", operator, address, size);

			/* process address */
			d_address = hexstr2int(address);
			tag = d_address >> (b+s); /* 标记t */
			set = (d_address & ((1<<(b+s))-1)) >> b; /* 组索引s */
			bit = (d_address) & ((1<<b)-1); /* 块偏移b, 其实模拟时没用，但还是写上 */
			printf("     address: %x, tag:%d, set:%d, bit:%d     ", d_address, tag, set, bit);

			/* 找到缓存行，根据操作符（I，L，S，M)，进行操作 */
			if (operator == 'L' || operator == 'S' || operator == 'M')
			{
					/* 首先根据标记，找到行 */
					flag = 0; /* if flag=0, we didn't find it */
				for (i=0; i<E; i++)
				{
					cacheij_address = &cache[set][i];
					if ((cacheij_address->tag == tag) & (cacheij_address->valid_bit))
						/* OK, find it */
					{
						flag = 1;
						hit += 1;
						printf("hit ");
						break;
					}
				}
				if (!flag)
				{
					/* we can't find it! */
					printf("miss ");
					miss += 1;
						/* set is full or not */
					if (is_full(&q[set]))
					{
							/* it's full, pop a cache_line, fill in and push it */
						cacheij_address	= pop(&q[set]);
						cacheij_address->tag = tag;
						push(&q[set], cacheij_address);
						eviction += 1;
						printf("eviction ");
					}
					else
					{
							/* find the uncached cache_line, and fill in */
						for (i=0; i<E; i++)
						{
							cacheij_address = &cache[set][i];
							if (!cacheij_address->valid_bit)
							{
								cacheij_address->tag = tag;
								cacheij_address->valid_bit = 1;
								push(&q[set], cacheij_address);
								break;
							}
						}
					}

				}
					/* if "M" */
				if 	(operator == 'M')
				{
					hit += 1;
					printf("hit ");
				}		
			}
			printf("\n");
		}
	}

	printf("hits:%d misses:%d evictions:%d", hit, miss, eviction);
	//free the memory of cache
	for (i=0; i<S; i++)
		free(cache[i]);
	free(address);
	fclose(fp);
	
	//printSummary(0, 0, 0);
	return 1;
}
```

