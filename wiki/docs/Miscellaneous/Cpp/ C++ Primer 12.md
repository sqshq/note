---
title: C++ Primer (12) - 动态内存
toc: true
date: 2017-07-30
tags: [C++, Memory]
top: 12
---

C++ 支持动态分配对象。动态对象的正确释放是编程中及其容易出错的地方。

程序使用动态内存处于以下三种原因之一：

* 程序不知道自己需要使用多少对象
* 程序不知道所需对象的准确类型
* 程序需要在多个对象间共享数据

## 12.1 动态内存智能指针

动态内存的管理是通过new和delete来完成的：

* new：分配空间，并返回一个指向该对象的指针
* delete：销毁对象，释放关联的内存

动态内存的使用非常容易出现问题，C++标准库提供了**智能指针**(smart pointer)来管理动态对象(定义在memory头文件中)：

* `shared_ptr`: 允许多个指针指向同一个对象
* `unique_ptr`: 独占所指向的对象
* `weak_ptr`: 指向`shared_ptr`所管理的对象的弱引用

### 12.1.1 shard_ptr类

默认初始化的智能指针中保存着一个空指针。shared_ptr支持的操作：

* `shared_ptr<T> sp` 空智能指针，可以指向类型为T的对象
* `p`  将p用作一个条件判断，若p指向一个对象，则为true
* `*p` 解引用p，获得它指向的对象
* `p->mem` 等价于 (*p).mem
* `p.get()` 返回p中保存的指针。
* `swap(p, q), p.swap(q)` 交换p和q中的指针
* `make_shared<T>(args)` 返回一个shared_ptr, 指向一个动态分配的类型为T的对象。使用args初始化此对象
* `shared_ptr<T>p(q)` p是q的拷贝
* `p=q` p和q都是shared_ptr，所保存的指针必须能相互转换。此造作会递减p的引用计数，递增q的引用计数；若p的引用计数变为0，则将其管理的原内存释放

每个shard_ptr都有一个引用计数，以下情况计数器会递增：

* 拷贝一个shared_ptr
* 用一个shared_ptr初始化另一个shared_ptr(注：传值时拷贝)
* 把shared_ptr作为参数传递给一个函数
* shared_ptr作为函数的返回值

以下情况，引用计数递减

* 给shared_ptr赋予一个新值
* shared_ptr被销毁

一旦一个shared_ptr引用计数为0，它就会自动释放自己所管理的对象。

### 12.1.2  直接管理内存

C++通过new和delete来直接管理内存。

传递给delete的指针必须指向动态分配的内存或者一个空指针。也就是说一般的指针是不可以的。

使用new和delete管理动态内存存在三个常见问题：

* 内存泄漏(memory leak)：忘记delete内存
* 使用已经释放的对象
* 同一块内存释放两次


**空悬指针**(dangling pointer)：在delete之后，指针值变为无效，但指针仍然保存着已经释放了的动态内存的地址。可以在离开其作用于之前释放掉它所关联的内存，或者赋予nullptr值。

## 12.1.3 shared_ptr和new结合使用

接受指针参数的智能指针构造函数是explicit的，因此我们不能将一个内置指针隐式转换为一个智能指针，智能使用直接初始化形式来初始化一个智能指针：

```cpp
shared_ptr<int> p1 = new int(1024); // error
shared_ptr<int> p2(new int(1024); //correct
```

注：两种初始化

* 拷贝初始化(copy initialization)： 使用=初始化一个变量
* 直接初始化(direct initialization)： 不使用=

### 12.1.5 unique_ptr

一个unique_ptr"拥有"它所指向的对象。与shared_ptr不同，某个时刻只能有一个unique_ptr指向一个给定对象。当unique_ptr被销毁时，它所指向的对象也被销毁。

类似shared_ptr，初始化unique_ptr必须采用直接初始化形式：

```cpp
unique_ptr<double> p1; // 可以指向一个double的unique_ptr
unique_ptr<int> p2(new int(42)); //指向一个值为42的int
```

由于一个unique_ptr拥有它指向的对象，因此unique_ptr不支持普通的拷贝或赋值操作。


unique_ptr操作：

* `unique_ptr<T> u1`: 空unique_ptr, 可以指向类型为T的对象。u1会使用delete来释放它的指针。
* `unique_ptr<T, D> u2`: u2会使用一个类型为D的可调用对象来释放它的指针。
* `unique_ptr<T, D> u(d)`: 空unique_ptr，指向类型为T的对象，用类型为D的对象d代替delete
* `u=nullptr`：释放u指向的对象，将u置为空
* `u.release()`: u放弃对指针的控制权，返回指针，并将u置为空
* `u.reset()`:释放u指向的对象
* `u.reset(q)，u.reset(nullptr)`: 如果提供了内置指针q，令u指向这个对象；否则将u置为空。

release只是放弃了对指针的控制权，也就是切断unique_ptr和它原来管理的对象间的联系，并没有释放指向的内存。

### 12.1.6 weak_ptr

weak_ptr指向由一个shared_ptr管理的对象。将一个weak_ptr绑定到一个shared_ptr不会改变shared_ptr的引用计数。

weak_ptr操作：

* `weak_ptr<T> w`： 空weak_ptr可以指向类型为T的对象
* `weak_ptr<T> w(sp)`：与shared_ptr sp指向相同对象的weak_ptr。T必须能转换为sp指向的类型
* `w=p`: p可以是一个shared_ptr或一个weak_ptr。赋值后w与p共享对象
* `w.reset()`：将w置为空
* `w.use_count()`:与w共享对象的shared_ptr的数量
* `w.expired()`:若w.use_count()为0，返回true，否则返回false
* `w.lock()`：如果expired为true，返回一个空的shared_ptr；否则返回一个指向w的对象的shared_ptr.

weak_ptr主要用于解决上面提到的**空悬指针**(dangling pointer)问题。一般几乎不可能知道指针所指向的内存是否已经释放。通过shared_ptr的expired和lock操作，用户能够检查内存释放[1]。

```cpp
#include <iostream>
#include <memory>

int main()
{
    // OLD, problem with dangling pointer
    // PROBLEM: ref will point to undefined data!

    int* ptr = new int(10);
    int* ref = ptr;
    delete ptr;

    // NEW
    // SOLUTION: check expired() or lock() to determine if pointer is valid

    // empty definition
    std::shared_ptr<int> sptr;

    // takes ownership of pointer
    sptr.reset(new int);
    *sptr = 10;

    // get pointer to data without taking ownership
    std::weak_ptr<int> weak1 = sptr;

    // deletes managed object, acquires new pointer
    sptr.reset(new int);
    *sptr = 5;

    // get pointer to new data without taking ownership
    std::weak_ptr<int> weak2 = sptr;

    // weak1 is expired!
    if(auto tmp = weak1.lock())
        std::cout << *tmp << '\n';
    else
        std::cout << "weak1 is expired\n";

    // weak2 points to new data (5)
    if(auto tmp = weak2.lock())
        std::cout << *tmp << '\n';
    else
        std::cout << "weak2 is expired\n";
}
```

## 12.2 动态数组

### 12.2.2 allocator类

allocator是C++标准类库，用来分配未构造的内存。

allocator分配的内存是未构造的(unconstructed)。为了使用allocate返回的内存，必须用construct构造对象。使用未构造的内存，其行为是未定义的。

标准库allocator类及其算法：

* `allocator<T> a`： 定义了一个名为a的allocator对象，它可以为类型为T的对象分配内存
* `a.allocate(n)`：分配一段原始的、未构造的内存，保存n个类型为T的对象
* `a.deallocate(p, n)`：释放从T*指针p中地址开始的内存，这块内存保存了n个类型为T的对象；p必须是一个先前由allocate返回的指针，且n必须是p创建时所要求的大小。在调用deallocate之前，用户必须对每个在这块内存中创建的对象调用destory。
* `a.construct(p, args)`: p必须是一个类型为T*的指针，指向一块原始内存；arg被传递给类型为T的构造函数，用来在p指向的内存中构造一个对象。
* `a.destroy(p)`: p为T*类型的指针，此算法对p指向的对象执行析构函数。


除了construct，还可以用`uninitialized_copy`和`uninitialized__fill`在未初始化内存中创建对象。

copy与uninitialized_copy的不同见[2]。






## reference

1. [When is std:weak_ptr useful?](https://stackoverflow.com/questions/12030650/when-is-stdweak-ptr-useful)
2. [Difference between std::uninitialized_copy & std::copy?](https://stackoverflow.com/questions/30158192/difference-between-stduninitialized-copy-stdcopy)