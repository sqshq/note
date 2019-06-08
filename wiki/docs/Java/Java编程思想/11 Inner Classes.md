---
title: 11 Inner Classes
toc: false
date: 2017-10-30
---

Inner Class: Place a class definition within another class definition.

When you create an inner class, an object of that inner class has a *link* to *the enclosing object that made it*, and so it can access the members of that enclosing object - without any special qualifications.

#### 使用.this和.new
在普通内部类中，通过`this`引用可以链接到其外部对象。

```java
public class Outer {
    public class Inner {
        public Outer getOuter() {
            // 直接使用this，将会得到Inner's this
            return Outer.this;
        }
    }

    public Inner getInner() {
        return new Inner();
    }

    public void getInfo() {
        System.out.println("I'm Outer");
    }

    public static void main(String[] args) {
        Outer outer = new Outer();
        Outer.Inner inner = outer.getInner();
        inner.getOuter().getInfo();
    }
}
```

创建内部类可以使用`.new`语法。例如上面这个例子可以不使用`getInner()`：

```java
//其他代码与上面的Outer相同
public static void main(String[] args) {
    Outer outer = new Outer();
    Outer.Inner inner = outer.new Inner();
    inner.getOuter().getInfo();
}
```



#### 匿名内部类

Anonymous inner classes(匿名内部类)

```java
public class Parcel7 {
    public Contents contents() {
        return new Contents() { // Insert a class definition
            private int i = 11;
            public int value() { return i; }
        }; // Semicolon required in this case
    }
    public static void main(String[] args) {
        Parcel7 p = new Parcel7();
        Contents c = p.contents();
}

} ///:~
```

The `contents()` method combines the creation of the return value with the definition of the class that represents that return value! In addition, the class is *anonymous*;

#### 静态内部类

静态内部类(Static nested classes), 又叫嵌套类(nested class): 内部类声明为static。

非静态内部类对象隐式地保存了一个引用，指向创建它的外围类对象。当内部类声明为static时：

* 要创建静态内部类的对象时，并不需要外围类的对象
* 不能从静态内部类的对象中访问非静态的外围类对象。

在非static内部类中，通过this引用可以链接到其外围类对象。类似于时staic方法，嵌套类没有this引用。


#### 为什么需要内部类

如果只是需要一个对接口的引用，可以满足需求的话，直接通过外围类实现接口，而不需要使用内部类。

使用内部类最吸引人的原因是：

*每个内部类都能独立地继承一个接口的实现，所以无论外围类是否已经继承了某个接口类的实现，对于内部类都没有影响。*