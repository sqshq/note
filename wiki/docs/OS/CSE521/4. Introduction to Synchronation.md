---
title: Introduction to Synchronization
toc: true
date: 2017-07-30
tags: [OS]
top: 4
---

## Fast Forward: Synchronization
What you need to know
* The OS creates the *illusion of concurrency* by quickly switching the processor(s) between multiple threads
    * We will back up and discuss how this happens after discussion synchronization

* **Threads** are used to abstract and multiplex the CPU

## Pandora’s Concurrency Box
The illusion of concurrency is both **powerful** and **useful**:

* It helps us think about how to structure our applications.
* It hides latencies caused by slow hardware devices.

Unfortunately, concurrency also creates **problems**:

* **Coordination**: how do we enable efficient communication between the multiple threads involved in performing a single task?
* **Correctness**: how do we ensure that shared state remains consistent when being accessed by multiple threads concurrently? How do we enforce time-based semantics?

We will focus on **correctness** today but return to **coordination** later.

## Patient 0

The **operating system** itself is one of the most difficult concurrent programs to write. Why?

* It is multiplexing access to hardware resources and therefore sharing a great deal of state between multiple processes!
* It frequently uses many threads to hide hardware delays while servicing devices and application requests.
* **Lots of shared state** plus **lots of threads** equals a difficult synchronization problem.
* Also, if the operating system gets synchronization wrong **bad things happen**.

## Concurrency v. Parallelism

The Go developers have a great description of this distinction. According to them:

> …​when people hear the word concurrency they often think of 
> parallelism, a related but quite distinct concept. In programming,
> concurrency is the composition of independently executing processes,
> while parallelism is the simultaneous execution of (possibly related)
> computations. Concurrency is about dealing with lots of things at 
> once. Parallelism is about doing lots of things at once.

[Watch the video](https://vimeo.com/49718712) to find out more.

## Unless Shown Otherwise…​

Concurrency forces us to relax any assumptions that we may want to make about how any particular thread executes.

Unless explicitly synchronized, threads may:

1. Be run in **any order**,
2. Be stopped and restarted at **any time**,
3. Remain stopped for **arbitrary lengths of time**.

* Generally these are **good things** — the operating system is making choices about how to allocate resources.
* When accessing shared data these are **challenges** that force us to program more carefully.

## Race Conditions
A **race condition** is "when the output of a process is unexpectedly dependent on timing or other events."

Note that the definition of a race depends on what we **expected** to happen:

* We expected me to have $4,000 after both deposits. (Otherwise we are not observing the Law of the Conversation of Money, probably important to banks except during bailouts.)

## Concurrency v. Atomicity
**Concurrency**: the illusion that multiple things are happening at once.
* Requires stopping or starting any thread at any time.

**Atomicity**: the illusion that a set of separate actions occurred **all at once**.
* Requires not stopping certain threads at certain times or not starting certain threads at certain times, i.e. providing some limited control to threads over their scheduling.

## Critical Sections

A **critical section**(临界区) contains a series of instructions that only one thread can be executing at any given time.
* This set (or sets) of instructions will look atomic with respect to **other threads executing code within the critical section**.

```c
void giveGWATheMoolah(account_t account, int largeAmount) {
  int gwaHas = get_balance(account);
  gwaHas = gwaHas + largeAmount;
  put_balance(account, gwaHas);
  notifyGWAThatHeIsRich(gwaHas);
  return;
}
```
In order to implement the previous example correctly:
* What is local state private to each thread? **gwaHas**
* What is the shared state that is being accessed by giveGWATheMoolah? **account**
* What lines are in the critical section? **2-4**

![things not go well](http://or9a8nskt.bkt.clouddn.com/thingsnotgowell.png)


## Critical Section Requirements
* **Mutual Exclusion:** this is the most basic property. Only one thread should be executing in the critical section at one time.
* **Progress**: all threads should eventually be able to proceed through the critical section.
* **Performance**: we want to keep critical sections as small as possible without sacrificing correctness.