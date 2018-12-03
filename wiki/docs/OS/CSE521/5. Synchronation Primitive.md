---
title: Synchronization Primitives
toc: true
date: 2017-07-30
tags: [OS]
top: 5
---

**Synchronization primitives**(同步原语) are simple software mechanisms provided by a platform (e.g. operating system) to its users for the purposes of supporting thread or process synchronization. They're usually built using lower level mechanisms (e.g. atomic operations, memory barriers, spinlocks, context switches etc)[1].

primitive or atomic action 是由若干个机器指令构成的完成某种特定功能的一段程序，具有不可分割性·即原语的执行必须是连续的，在执行过程中不允许被中断[2]。



## Implementing Critical Sections

* Two possible approaches. **Don’t stop**, or **don’t enter**.

* On **uniprocessors** a single thread can prevent other threads from executing in a critical section by simply not being descheduled.
    * In the kernel we can do this by **masking** interrupts. No timer, no scheduler, no stopping.
    * **In the multicore era this is only of historical interest**. (This design pattern is usually broken.)
* More generally we need a way to force other threads—potentially running on other cores—**not to enter** the critical section while one thread is inside. **How do we do this**?

## Atomic Instructions

Software synchronization primitives **utilize special hardware instructions** guaranteed to be atomic across all cores:

* **Test-and-set**: write a memory location and return its old value.

```c
int testAndSet(int * target, int value) {
  oldvalue = *target;
  *target = value;
  return oldvalue;
}
```

* **Compare-and-swap**: compare the contents of a memory location to a given value. If they are the same, set the variable to a new given value.

```c
bool compareAndSwap(int * target, int compare, int newvalue) {
  if (*target == compare) {
    *target = newvalue;
    return 1;
  } else {
    return 0;
  }
}
```

* **Load-link and store-conditional**: Load-link returns the value of a memory address, while the following store-conditional succeeds **only if** the value has not changed since the load-link.

```c
y = 1;
__asm volatile(
    ".set push;"     /* save assembler mode */
    ".set mips32;"   /* allow MIPS32 instructions */
    ".set volatile;" /* avoid unwanted optimization */
    "ll %0, 0(%2);"  /*   x = *sd */
    "sc %1, 0(%2);"  /*   *sd = y; y = success? */
    ".set pop"       /* restore assembler mode */
    : "=r" (x), "+r" (y) : "r" (sd));
if (y == 0) {
  return 1;
}
```

* Many processors provide either **test and set** or **compare and swap**.
* On others equivalents can be implemented in software using other atomic hardware instructions.

## The Bank Example: Test and Set
Let’s modify our earlier example to use a test and set:

```c
void giveGWATheMoolah(account_t account, int largeAmount) {
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

```c
+int payGWA = 0; // Shared variable for our test and set.

void giveGWATheMoolah(account_t account, int largeAmount) {
+ testAndSet(&payGWA, 1); # Set the test and set.
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
+ testAndSet(&payGWA, 0); # Clear the test and set.
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```
**Does this work?** No! How do I tell if another thread has already set payGWA?

Let’s try again:

```c
void giveGWATheMoolah(account_t account, int largeAmount) {
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

```c
+int payGWA = 0; // Shared variable for our test and set.

void giveGWATheMoolah(account_t account, int largeAmount) {
+ if (testAndSet(&payGWA, 1) == 1) {
+   // But then what?
+ }
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
+ testAndSet(&payGWA, 0); # Clear the test and set.
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

* But what should I do if the payGWA is set?

```c
void giveGWATheMoolah(account_t account, int largeAmount) {
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

```c
+int payGWA = 0; // Shared variable for our test and set.

void giveGWATheMoolah(account_t account, int largeAmount) {
+ while (testAndSet(&payGWA, 1) == 1) {
+   ; // Test it again!
+ }
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
+ testAndSet(&payGWA, 0); # Clear the test and set.
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

## Busy Waiting

![busy waiting](http://or9a8nskt.bkt.clouddn.com/15314088473143.jpg)
 
 
![whentwothreadsrace](http://or9a8nskt.bkt.clouddn.com/whentwothreadsrace.png)


 

## The Bank Example: Test and Set
```c
int payGWA = 0; // Shared variable for our test and set.

void giveGWATheMoolah(account_t account, int largeAmount) {
  while (testAndSet(&payGWA, 1) == 1) {
   ; // Test it again!
  }
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
  testAndSet(&payGWA, 0); # Clear the test and set.
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

What are the **problems** with this approach?
* **Busy waiting**: threads wait for the critical section by "pounding on the door", executing the TAS repeatedly.
* Bad on a multicore system. Worse on a single core system! **Busy waiting prevents the thread in the critical section from making progress!**

## Locks
**Locks** are a synchronization primitive used to implement critical sections.

* Threads **acquire** a lock when entering a critical section.
* Threads **release** a lock when leaving a critical section.

## Spinlocks
What we have implemented today is known as a **spinlock**:

* **lock** for the fact that it guards a critical section (we will have more to say about locks next time), and
* **spin** describing the process of acquiring it.

Spinlocks are **rarely used** on their own to solve synchronization problems.

Spinlocks are **commonly used** to build more useful synchronization primitives.

## More Bank Example

```c
void giveGWATheMoolah(account_t account, int largeAmount) {
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

```c
lock gwaWalletLock; // Need to initialize somewhere

void giveGWATheMoolah(account_t account, int largeAmount) {
+ lock_acquire(&gwaWalletLock);
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
+ lock_release(&gwaWalletLock);
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```

What happens if we call `lock_acquire()` while another thread is in the critical section?

* **The thread acquiring the lock must wait until the thread holding the lock calls lock_release()**.

## How To Wait
**How** do we wait?
* **Active** (or busy) waiting: repeat some action until the lock is released.
* **Passive** waiting: tell the kernel what we are waiting for, go to sleep, and rely on `lock_release` to awaken us.

## Spinning v. Sleeping
There are cases where spinning is the right thing to do. **When**?

* Only on multicore systems. Why?
    * On single core systems **nothing can change** unless we allow another thread to run!
* If the critical section is **short**.
    * Balance the length of the **critical section** against the overhead of a **context switch**.

## When to Spin
If the critical section is **short**:
![when to spin](http://or9a8nskt.bkt.clouddn.com/whentospin.png)


## When to Sleep
If the critical section is **long**:

![when_to_sleep](http://or9a8nskt.bkt.clouddn.com/when_to_sleep.png)

## How to Sleep
The kernel provides functionality allowing kernel threads to sleep and wake on a **key**:
* `thread_sleep(key)`: "Hey kernel, I’m going to sleep, but please wake me up when key happens."
* `thread_wake(key)`: "Hey kernel, please wake up all (or one of) the threads who were waiting for key."
* Similar functionality can be implemented in user space.

## Thread Communication

* Locks are designed to protect **critical sections**.
* `lock_release()` can be considered a **signal** from the thread inside the critical section to other threads indicating that they can proceed.
    * In order to receive this signal a thread must be sleeping.
* What about other kinds of signals that I might want to deliver?
    * The buffer has data in it.
    * Your child has exited.

## Condition Variables
A **condition variable**(条件变量) is a signaling mechanism allowing threads to:

* `cv_wait` until a **condition** is true, and
* `cv_notify` other threads when the condition becomes true.

The **condition** is usually represented as some change to shared state.

* The buffer has data in it: **bufsize > 0**.
* `cv_wait`: notify me when the buffer has data in it.
* `cv_signal`: I just put data in the buffer, so notify the threads that are waiting for the buffer to have data.

* **Condition variable** can convey **more information** than locks about some change to the state of the world.

As an example, a buffer can be **full**, **empty**, or **neither**.

* If the buffer is **full**, we can let threads withdraw but not add items.
* If the buffer is **empty**, we can let threads add but not withdraw items.
* If the buffer is neither full nor empty, we can let threads add and withdraw items.

We have **three** different buffer states (full, empty, or neither) and **two** different threads (producer, consumer).

Why are condition variables a synchronization mechanism?
* Want to ensure that the condition **does not change** between checking it and deciding to wait!

![condition_variable](http://or9a8nskt.bkt.clouddn.com/condition_variable.png)


## reference

[1] https://stackoverflow.com/questions/8017507/definition-of-synchronization-primitive
[2] https://baike.baidu.com/item/原语/3794081?fr=aladdin