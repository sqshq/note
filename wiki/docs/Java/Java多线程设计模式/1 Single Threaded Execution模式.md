---
title: 1 Single Threaded Execution模式
---

所谓Single Threaded Execution模式，就是指“以一个线程执行”。就像一座独木桥同一时间内只允许一个人通过一样，该模式用于设置限制，以确保同一时间内只能让一个线程执行处理。


### Example: 通过门

首先，我们来看一下应该使用Single Threaded Execution模式却没有使用的程序，体会一下在多线程下无法正确执行的程序会引发什么现象。

该程序模拟的是三个人频繁地通过一个只允许一个人经过的门的情形。当人们通过门的时候，统计人数便会递增。另外，程序还会记录通行者的姓名与出生地。

| 名字 | 说明 |
| --- | --- |
| Main | 创建门，并让三个人不断地通过的类 |
| Gate |	 表示门的类。它会在人通过时记录其姓名和出生地 |
| UserThread | 表示人的类。人们将不断地通过门 |


```Java tab="Main"
// 创建一个门，并让三个人不断地通过.
// 为了便于一一对应，每个人的名字与出生地的首字母都设置成了相同的。
public class Main {
    public static void main(String[] args) {
        Gate gate = new Gate();
        new UserThread(gate, "Steve Nash", "San Francisco").start();
        new UserThread(gate, "Michael Jordan", "Miami").start();
        new UserThread(gate, "Ronaldo", "Rome").start();
    }
}
```

```Java tab="Gate"
public class Gate {
    protected int counter = 0;
    protected String name = "Nobody";
    protected String address = "Nowhere";
 
    // 非安全线程： 通过门
    public void pass(String name, String address) {
        this.counter++; // 到目前为止已经通过这道门的人数
        this.name = name; // 最后一个通行者的姓名
        this.address = address; // 最后一个通行者的出生地
        check();
    }
 
    // toString返回门当前状态的字符串
    public String toString() {
        return "No." + conuter + ": " + name + "," + address;
    }
 
    // 检查name和adress的首字母是否项目，不相同则为异常数据
    private void check(){
        if(name.charAt(0) != address.charAt(0)
            System.out.println("******* BROKEN ********:"+toString());
    }
}
```

```Java tab="UserThread"
public class UserThread extends Thread {
    private final Gate gate;// 要通过的门
    private final String myname; // 姓名
    private final String myaddress;// 出生地
 
    public UserThread(Gate gate, String myname, 
                        String myaddress) {
        super();
        this.gate = gate; 
        this.myname = myname;
        this.myaddress = myaddress;
    }
    // 线程首先显示通行者姓名与BEGIN字样，随后反复调用pass，
    // 表示这个人在门里不断地穿梭通过
    public void run() {
        System.out.println(myname + " BEGIN:");
        while (true) gate.pass(myname, myaddress);
    }
}
```

下面是程序的运行结果：


<small>
```
Steve Nash BEGIN:
Ronaldo BEGIN:
Michael Jordan BEGIN:
******* BROKEN ********:No.193689: Michael Jordan,Miami
******* BROKEN ********:No.194489: Michael Jordan,Miami
******* BROKEN ********:No.194959: Michael Jordan,Miami
...
```
</small>

`Gate`类的实例被多个线程使用时，运行结果会与预期不一致，即`Gate`类是线程不安全的。另外，仔细看一下`counter`的值，最开始显示BROKEN的时候，`counter`的值已经变为了193689，也就是说，在检查出第一个错误的时候，三人已经穿梭100万次以上了。但是如果只测试几次，即使几万次，也找不到错误。

这是多线程程序设计的难点。如果检查出错误，那么说明程序线程不安全。但是，**就算没检查出错误，也不能说程序就一定是线程安全的**。测试次数不够、时间点不对，都有可能检查不出错误。一般来说，操作测试并不足以证明程序的安全性。测试只不过提高了“程序也许安全”的概率而已。


加下来，将`Gate`类修改为线程安全的类。其中有两处修改，即分别在`pass`方法和`toString`方法前面加上了`synchronized`关键字.

```Java hl_lines="7 15"
public class Gate {
    protected int counter = 0;
    protected String name = "Nobody";
    protected String address = "Nowhere";
 
    // 非安全线程： 通过门
    public synchronized void pass(String name, String address) {
        this.counter++; // 到目前为止已经通过这道门的人数
        this.name = name; // 最后一个通行者的姓名
        this.address = address; // 最后一个通行者的出生地
        check();
    }
 
    // toString返回门当前状态的字符串
    public synchronized String toString() {
        return "No." + conuter + ": " + name + "," + address;
    }
 
    // 检查name和adress的首字母是否项目，不相同则为异常数据
    private void check(){
        if(name.charAt(0) != address.charAt(0)
            System.out.println("******* BROKEN ********:"+toString());
    }
}
```
### Summary

加下来归纳一下Single Threaded Execution模式:

`Gate`类扮演SharedResource(共享资源)模式，它是可被多个线程访问的类，包含很多方法，主要分为如下两类：

* safeMethod: 多个线程同时调用也不会发生问题的方法.
* unsafeMethod: 多个线程同时调用时，实例状态有可能发生改变。可以通过将unsafeMethod声明为`synchronized`方法来进行保护。


![single-threaded-execution](figures/single-threaded-execution.png)



临界区的大小和性能：一般情况下，Single Threaded Execution模式会降低程序性能，

* 获取锁花费时间：进入`synchronized`方法时，线程需要获取对象的锁，该处理会花费时间
* 线程冲突引起的等待：当线程在临界区内，其他想要进入临界区的线程会阻塞，这种状况称为线程冲突(conflict)。发生冲突时，程序的整体性能会随着线程等待时间的增加而下降。如果尽可能地缩小临界区的范围，降低线程冲突的概率，那么就能一直性能的下降。


#### 计数信号量

Single Threaded Execution模式用于确保某个区域“只能由一个线程”执行。使用计数信号量可以确保某个区域"最多只能由$N$个线程"执行。



```Java tab="BoundedResource"
// 资源个数有限
class BoundedResource {
    private final Semaphore semaphore;
    private final int permits;
    private final static Random random = new Random(314159);

    // 构造函数(permits为资源个数)
    public BoundedResource(int permits) {
        this.semaphore = new Semaphore(permits);
        this.permits = permits;
    }

    // 使用资源
    public void use() throws InterruptedException {
        semaphore.acquire();
        try {
            doUse();
        } finally {
            semaphore.release();
        }
    }

    // 实际使用资源(此处仅使用Thread.sleep)
    protected void doUse() throws InterruptedException {
        Log.println("BEGIN: used = " 
                    + (permits - semaphore.availablePermits()));
        Thread.sleep(random.nextInt(500));
        Log.println("END:   used = " 
                    + (permits - semaphore.availablePermits()));
    }
}
```

```java tab="UserThread"
// 使用资源的线程
class UserThread extends Thread {
    private final static Random random = new Random(26535);
    private final BoundedResource resource;

    public UserThread(BoundedResource resource) {
        this.resource = resource;
    }

    public void run() {
        try {
            while (true) {
                resource.use();
                Thread.sleep(random.nextInt(3000));
            }
        } catch (InterruptedException e) {
        }
    }
}
```

```Java tab="UsingSemaphore"
public class UsingSemaphore {
    public static void main(String[] args) {
        // 设置3个资源
        BoundedResource resource = new BoundedResource(3);

        // 10个线程使用资源
        for (int i = 0; i < 10; i++) {
            new UserThread(resource).start();
        }
    }
}
```