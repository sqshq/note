---
title: Deadlock and exec
toc: true
date: 2017-07-30
tags: [OS]
top: 6
---


## Locking Multiple Resources

* **Locks** protect access to shared resources.
* Threads may need **multiple** shared resources to perform some operation.

Consider two threads A and B that both need **simultaneous** access to resources 1 and 2:

1. **Thread A** runs, grabs the lock for **Resource 1**.
2. → CONTEXT SWITCH ←
3. **Thread B** runs, grabs the lock for **Resource 2**.
4. → CONTEXT SWITCH ←
5. **Thread A** runs, tries to acquire the lock for **Resource 2**.
6. → THREAD A SLEEPS ←
7. **Thread B** runs, tries to acquire the lock for **Resource 1**.
8. → THREAD B SLEEPS ←

Now what?

## Deadlock
**Deadlock**(死锁) occurs when a thread or set of threads are waiting for each other to finish and thus nobody ever does.

## Self Deadlock
A **single thread** can deadlock. How?
* Thread A acquires Resource 1. Thread A tries to reacquire Resource 1.

This seems inane. Why would this happen?
* `foo()` needs Resource 1. `bar()` needs Resource 1. While locking Resource 1 `foo()` calls `bar()`.

Can we solve this problem?

* Yes! **Recursive** locks. Allow a thread to reacquire a lock that it already holds, as long as calls to acquire are matched by calls to release.
* This kind of problem is not uncommon. You may want to implement recursive locks for OS/161.
* (But don’t make the locks we gave you suddenly recursive…​)

## Conditions for Deadlock
A deadlock **cannot occur** _unless_ all of the following conditions are met:
* **Protected access** to shared resources, which implies waiting.
* **No resource preemption**, meaning that the system cannot forcibly take a resource from a thread holding it.
* **Multiple independent requests**, meaning a thread can hold some resources while requesting others.
* **Circular dependency graph**, meaning that Thread A is waiting for Thread B which is waiting for Thread C which is waiting for Thread D which is waiting for Thread A.

## Dining Philosophers

* "Classic" synchronization problem which I feel obligated to discuss.

* Illustrated below.

![dining philosophers](http://or9a8nskt.bkt.clouddn.com/dining philosophers.png)

[wiki](https://en.wikipedia.org/wiki/Dining_philosophers_problem)


## Feeding Philosophers
Breaking deadlock conditions usually requires eliminating one of the **requirements** for deadlock.
* **Don’t wait**: don’t sleep if you can’t grab the second chopstick and put down the first.
* **Break cycles**: usually by acquiring resources in a **well-defined order**. Number chopsticks 0–4, always grab the higher-numbered chopstick first.
* **Break out**: detect the deadlock cycle and forcibly take away a resource from a thread to break it. (Requires a new mechanism.)
* **Don’t make multiple independent requests**: grab **both** chopsticks at once. (Requires a new mechanism.)

## Deadlock v. Starvation
**Starvation**(饥饿) is an equally-problematic condition in which one or more threads do not make progress.
* Starvation differs from deadlock in that **some** threads make progress and it is, in fact, those threads that are preventing the "starving" threads from proceeding.

## Deadlock v. Race Conditions

What is better: a deadlock (perhaps from overly careful synchronization) or a race condition (perhaps from a lack of correct synchronization)?

I’ll take the deadlock. **It’s much easier to detect!**

## Using the Right Tool

* Most problems can be solved with a **variety** of synchronization primitives.
* However, there is usually **one primitive** that is more appropriate than the others.
* You will have a chance to practice picking synchronization primitives for ASST1, and throughout the class.

## Approaching Synchronization Problems

1. Identify the constraints.
2. Identify shared state.
3. Choose a primitive.
4. Pair waking and sleeping.
5. Look out for multiple resource allocations: can lead to deadlock.
6. Walk through simple examples and corner cases before beginning to code.

## $ wait %1 # Process lifecycle

* Change: `exec()`
* Death: `exit()`
* The Afterlife: `wait()`

## Groundhog Day

Is `fork()` enough?

![fork--](http://or9a8nskt.bkt.clouddn.com/fork().png)


## Change: exec()

* The `exec()` family of system calls replaces the calling process with a new process loaded from a file.
* The executable file must contain a complete **blueprint** indicating how the address space should look when `exec()` completes.
    * What should the contents of memory be?
    * Where should the first thread start executing?
* Linux and other UNIX-like systems use **ELF** (Executable and Linkable Format) as the standard describing the information in the executable file is structured.

## $ readelf # display ELF information

![readlf](http://or9a8nskt.bkt.clouddn.com/readlf.png)

## $ /lib/ld-linux.so.2

![ldlinux](http://or9a8nskt.bkt.clouddn.com/ldlinux.png)
## exec() Argument Passing

* The process calling `exec()` passes arguments to the process that will replace it **through the kernel**.
    * The kernel retrieves the arguments from the process after the call to `exec()` is made.
    * It then pushes them in to the memory of the process where the replacement process can find them when it starts executing.
   * This is where main gets *argc* and *argv*!
* `exec()` also has an interesting return, almost the dual of `fork()`: `exec()` never returns!

## $exec()

![exec1](http://or9a8nskt.bkt.clouddn.com/exec1.png)
![exec2](http://or9a8nskt.bkt.clouddn.com/exec2.png)
![exec3](http://or9a8nskt.bkt.clouddn.com/exec3.png)
![exec4](http://or9a8nskt.bkt.clouddn.com/exec4.png)
![exec5](http://or9a8nskt.bkt.clouddn.com/exec5.png)
![exec6](http://or9a8nskt.bkt.clouddn.com/exec6.png)
![exec7](http://or9a8nskt.bkt.clouddn.com/exec7.png)



## exec() File Handle Semantics
* By convention exec does **not** modify the file table of the calling process! Why not?
* Remember **pipes**?
    * Don’t undo all the hard work that `fork()` put in to duplicating the file table!
![pipes example 3](http://or9a8nskt.bkt.clouddn.com/pipesexample3.png)
