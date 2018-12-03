---
title: Threads and Thread Implementations
toc: true
date: 2017-07-30
tags: [OS]
top: 9
---



## Threads

So what is a thread?

-   Registers
-   Stack


How are each of the following shared between threads or processes?

-   Registers
-   Stack
-   Memory
-   File descriptor table.

![thread](http://or9a8nskt.bkt.clouddn.com/thread.png)

## Why Use Threads?

1.  Threads can be a good way of thinking about applications that do multiple things "simultaneously."
2.  Threads may naturally encapsulate some data about a certain thing that the application is doing.
3.  Threads may help applications hide or parallelize delays caused by slow devices.

## Threads v. Processes Part II


Good example from Wikipedia: multiple threads within a single process are like multiple cooks trying to prepare the same meal together.

![kitchen](http://or9a8nskt.bkt.clouddn.com/kitchen.png)
-   Each one is doing one thing.
-   They are probably doing different things.
-   They all share the same recipe but may be looking at different parts of it.
-   They have private state but can communicate easily.
-   They must coordinate!

## Meme

The OS corrupted
The cake

## Aside: Threads v. Events
-   While threads are a reasonable way of thinking about concurrent programming, they are not the only way—​or even always the *best* way—​to make use of system resources.
-   Another approach is known as [event-driven programming](https://en.wikipedia.org/wiki/Event-driven_programming).
-   Anyone who has done JavaScript development or used frameworks like [node.js](http://nodejs.org/) has grown familiar with this programming model.

Events v. threads (over)simplified:

-   Threads **can block**, so we make use of the CPU by switching between threads!
-   Event handlers **cannot block**, so we can make use of the CPU by simply running events until completion.

## Naturally Multithreaded Applications
Web server:
-   Use a separate thread to handle each incoming request.

Web browser:
-   Separate threads for each open tab.
-   When loading a page, separate threads to request and receive each
    unique part of the page.

Scientific applications:
-   Divide-and-conquer "embarrassingly parallelizable" data sets.

## Why Not Processes?

-   IPC is more difficult because the kernel tries to protect processes from each other.
    -   Inside a single process, anything goes!
-   State (what?) associated with processes doesn’t scale well.


## Implementing Threads

Threads can be implemented in user space by unprivileged libraries.
-   This is the M:1 threading model, M user threads that look like 1 thread to the operating system kernel.

Threads can be implemented by the kernel directly.
-   This is the 1:1 threading model.

![thread1](http://or9a8nskt.bkt.clouddn.com/thread1.png)
![thread2](http://or9a8nskt.bkt.clouddn.com/thread2.png)
![thread3](http://or9a8nskt.bkt.clouddn.com/thread3.png)



## Implementing Threads in User Space

How is this possible?
-   Doesn’t involve multiplexing between processes so no kernel privilege required!

How do I:
-   **Save and restore context?** This is just saving and restoring registers. The C library has an implementation called `setjmp()`/`longjmp()`
-   **Preempt other threads?** Use periodic signals delivered by the operating system to activate a user space thread scheduler.
    
## Aside: setjmp()/longjmp() Wizardry
What will the following code do?

```c
nt main(int argc, void * argv) {
  int i, restored = 0;
  jump_buf saved;
  for (i = 0; i < 10; i++) {
    printf("Value of i is now %d\n", i);
    if (i == 5) {
      printf("OK, saving state...\n");
      if (setjmp(saved) == 0) {
        printf("Saved CPU state.\n");
        break;
      } else {
        printf("Restored CPU state.\n");
        restored = 1;
      }
    }
  }
  if (!restored) {
    longjmp(saved, 1);
  }
}
```

```
Value of i is now 0
Value of i is now 1
Value of i is now 2
Value of i is now 3
Value of i is now 4
Value of i is now 5
OK, saving state...
Saved CPU state.
Restored CPU state.
Value of i is now 6
Value of i is now 7
Value of i is now 8
Value of i is now 9
```


* Use these tricks to impress your (new) friends!
* (Or get rid of old ones…​)

## Comparing Threading Implementations
**M:1 (user space) threading**

Pros:
* Threading operations are much faster because they do not have to cross the user/kernel boundary.
* Thread state can be smaller.

Cons:
* Can’t use multiple cores!
* Operating system may not schedule the application correctly because it doesn’t know about the fact that it contains more than one thread.
* A single thread may block the entire process in the kernel when there are other threads that could run.

**1:1 (kernel) threading**
Pros:
* Scheduling might improve because kernel can schedule all threads in the process.

Cons:
* Context switch overhead for all threading operations.