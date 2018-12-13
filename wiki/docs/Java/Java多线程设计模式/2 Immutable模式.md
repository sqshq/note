---
title: 2 Immutable模式
---

String类表示字符串，类中并没有修改字符串内容的方法。由于String内部状态不会发生变化，所以无论String实例被多少个线程访问，也无需线程的互斥处理。

Immutable模式中存在着确保实例状态不发生改变的类。在访问这些实例时并不需要执行耗时的互斥处理。

### 示例程序

| 名字 | 说明 |
| --- | --- |
| Person | 表示人的类 |
| Main |	 测试程序行为的类 |
| PrintPersonThread | 显示Person实例的线程的类 |

```Java tab="Person"
public final class Person {
    private final String name;
    private final String address;
    public Person(String name, String address) {
        this.name = name;
        this.address = address;
    }
    public String getName() {
        return name;
    }
    public String getAddress() {
        return address;
    }
    public String toString() {
        return "[ Person: name = " + name + ",
             address = " + address + " ]";
    }
}
```

```Java tab="Main"
public class Main {
    public static void main(String[] args) {
        // 创建一个Person类的实例，并启动三个线程访问该实例
        Person alice = new Person("Alice", "Alaska");
        new PrintPersonThread(alice).start();
        new PrintPersonThread(alice).start();
        new PrintPersonThread(alice).start();
    }
}
```



```Java tab="PrintPersonThread"
public class PrintPersonThread extends Thread {
    private Person person;
    public PrintPersonThread(Person person) {
        this.person = person;
    }
    public void run() {
        while (true)
            System.out.println(Thread.currentThread().getName()
                     + " prints " + person);
    }
}
```


* Person类的变量仅可通过构造函数来设置，类中没有修改字段值的`set`方法，只有获取字段值的`get`方法。
* Person类声明了final类型，无法创建Person类的子类，防止子类修改字段值。
* Person类的变量的可见性都是`private`，只能内部访问，防止被修改，并且都声明为了`final`，一旦被赋值就不会发生改变。


![Immutable_Pattern_UM](figures/Immutable_Pattern_UML.png)


### 扩展

#### 何时使用

Immutable类中的字段的值不可以修改，也不存在修改字段内容的方法。Immutable类的实例被创建后，状态降不再发生变化。不需要使用`synchronized`进行保护。能够在不失去安全性和生存性的前提下提高性能。在以下情况下使用：

* 实例创建后，状态不再发生变化
* 实例是共享的，且被频繁访问


#### 考虑成对的mutable/immutable类

如果程序可以分为修改类和不修改类的情况，那么可以将这个类拆分称为mutable类和immutable类。并设计成可以根据mutable实例创建immutable实例，也可以根据immutable实例创建mutable实例。

Java的标准库中就有成对的mutable类和immutable类。例如String类和StringBuffer类。StringBuffer类是字符串的mutable类，能够改写，是线程安全的。String类是字符串的immutable类，不可以改写的。StringBuffer类中有一个以String为参数的构造函数，而String类中有一个以StringBuffer为参数的构造函数。

#### 标准类库中用到的Immutable模式

* 表示字符串的String类
* 表示大数字的BigInteger、BigDecimal类
* 基本类型的包装类(Integer, Short, Double)
* 表示颜色的Color类