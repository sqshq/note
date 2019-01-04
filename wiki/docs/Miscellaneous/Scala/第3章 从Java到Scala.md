---
title: 第3章 从Java到Scala
---

### 第3章 从Java到Scala
#### 3.1 Scala：简洁的Java
**减少样板代码**

Scala具有非常高的代码密度——输入少量代码就可以完成许多功能。作为对比，来看一个Java代码的例子

```Java
public class Greetings {
    public static void main(String[] args) {
        for (int i = 1; i < 4; i++) 
            System.out.println(i + ",");
    }
    System.out.println("Scala Rocks!!!");
    }
}
```

使用Scala可以省去这段代码不少东西

* 可以不使用分号
* 不用把代码写在类`Greetings`中
* 不需要指定变量`i`的类型
* 可以使用`println`而不使用`System.out.`前缀

下面是Java代码使用Scala简化后的代码。箭头(`<-`)的左边定义了一个val，右边是一个生成器表达式。每次迭代都会创建一个新的val，并使用所生成的值的元素相继对其进行初始化。
```scala
1,2,3,Scala Rocks!!!
```

**使用val定义的变量是不可变的，即初始化后不能更改。然而，那些使用var定义的变量是可变的**。

**不可变性(immutability)是作用在变量上，而不是作用在变量所引用的实例上的**。

例如，如果编写了`val buffer = new StringBuffer()`, 就不能改变`buffer`的引用。但是，可以使用`StringBuffer.append()`方法来修改所引用的实例。
```scala
sb: StringBuffer = a
res1: StringBuffer = a
```

在Scala中，应尽可能多地使用val，因为它可以提升不可变性，从而减少错误，也可以增益函数式风格。
#### 3.2 原始类型对应的Scala类

和Java不同，Scala将所有的类型都视为对象。这就意味着，和调用对象上的方法一样，也可以在字面量上进行方法调用。

在`1.to(3)`或者`1 to 3`中，需要用类似Java中自动装箱(autoboxing)的机制，以便可以在`Int`上调用`to()`方法。因为`Int`不能直接处理这种请求，所以Scala会自动应用`intWrapper()`方法将`Int`转换为`scala.runtime.RichInt`，然后调用`RichInt`上的`to()`方法。

诸如`RichInt`, `RichDouble`和`RichBoolean`这些类，可称为**富包装类**(rich wrapper class)。它们为Scala中的Java原始类型和`String`提供了便于使用的方法。
#### 3.3 元祖和多重赋值

Scala的**元组**是一个*不可变*的对象序列，创建时使用逗号分隔。例如, ("Venkat", "zhenhua", "hello")就是表示一个3个对象的元组。可以将元组中的多个元素同时赋值给多个val或者var(**多重赋值**)。
```scala
firstName: String = Venkat
lastName: String = Subramaniam
emailAddress: String = venkats@agiledeveloper.com
```

也可以将元组整体赋值给一个变量，然后采用**下划线加数字**`._i`这种语法形式访问其中的元素。数字$i$表示在元组中元素的索引，元组的索引从1开始。
```scala
Venkat
```

#### 3.4 灵活的参数和参数值
#### 3.6 字符串和多行原始字符串
Scala中的字符串就是`java.lang.String`。可以用Java的方式使用`String`。Scala能够自动将String转化为`scala.runtime.RichString`。这种转化给`String`新增了一些有用的方法，如`capitalize()`, `lines()`和`reverse()`方法。
```scala
s: String = Good
```

可以用一对3个双引号(`"""..."""`), 创建一个跨行的字符串。Scala将3个双引号中间的内容保持原样，在Scala中这种字符串被称为**原始字符串**。

```scala
val str = """In his famous inaugural speech, John F. Kennedy said "And so, my fellow Americans: ask not what your country can do speak to the citizens of the World..."""
```
#### 3.7 字符串插值

在双引号前面的**s**的意思是s插值器(s-interpolator), 它会找到字符串中的表达式，并将其替换成对应的值。
```scala
discount: Int = 90
message: String = A discount of 90% has been applied
```

如果表达是是最简单的一个变量，那么在它的前面加上美元符号`$`。而对于更复杂的表达式，可以把它们放在大括号中。
```scala
price: Int = 90
totalPrice: String = The amount of discount is 81 dollars
```

美元符号被用作表达式的分隔符，如果说字符串中正好有一个$符号，那么其还可以被用作转义符。
```scala
totalPrice: String = The amount of discount is $81
```

s插值器只是用值去替换表达式，而不做任何格式处理。下面的表达式正确求值了，但是输出结果中小数点后有3位小数：
```scala
On ticket 10% save $2.512
```

为了对输出做格式化，而不只是插值，可以使用**f插值器**(f-interpolator)。字符串的格式化和Java中的`printf`函数遵循相同的规则，只是还可以和前面的例子一样嵌入表达式。改写前面的`println`语句，在表达式后面带上格式`2.2f`。注意，需要用一个额外的%转义已有的那个百分号。我们没有在product或者discount变量后放置任何格式相关的额符号，尽管我们本可以放相应的%s和%d。如果没有指定格式，那么f插值器将会假定格式是%s，也就是说直接转化为字符串。
```scala
On ticket 10% saves $2.51
```

#### 3.9 操作符重载

技术上说，Scala没有操作符，所以操作符重载的意思是重载诸如+、-等符号。在Scala中，这些都是方法名。操作符利用了Scala宽松的方法调用语法––Scala不强制在对象引用和方法名中间使用点号(`.`)。

这两个特性结合在一起就给人一种操作符重载的幻觉。因此，当调用`ref1+ref2`，实际上是`ref1.+(ref2)`，是在`ref1`上面调用`+()`方法。
下面的`Complex`类表示复数，提供了`+`操作符。`Complex`类定义了一个接收两个参数的构造器。
```scala
(1+2i) + (2-3i) = 3-1i
```

Scala没有操作符，所以没有在操作符上定义优先级，但是它在**方法上定义了优先级**。方法的第一个字符决定了优先级。如果在一个表达式中两个字符的优先级相同，那么在左边的方法优先级更高。下面是第一个字符的优先级从低到高的列表：

所有字符

    |
    ^
    &
    <>
    = !
    :
    + -
    * / %
    其他特殊字符
在下面的代码中，我们在`Complex`中定义了加方法和乘方法。

```scala
Calling *
Calling +
-1-6i
```

#### 3.10 Scala与Java的差异

**赋值的结果**

在Java中，赋值操作(像`a=b`)的返回值就是`a`的值，因此像`x=a=b`这样的连续赋值就可以出现，但是在Scala中不能这样做。在Scala中赋值操作的结果值是一个`Unit`———大概等价于一个`Void`。

```scala
var a = 1
var b = 2
a = b = 3 //编译错误
```
**Scala的==**

Java的`==`对基本类型和引用类型有着不同的含义。对于基本类型，`==`意味着基于值的比较，对于引用类型，它意味着基于引用的比较。

Scala对`==`的处理和Java不同，它对所有类型都是一致的。在Scala中，`==`表示基于值的比较，而不论类型是什么。这是在类`Any`(Scala中所有类型都衍生自`Any`)中实现了`final`的`==()`方法保证的。

如果要比较引用是否指向同一个对象，可以使用Scala中的`eq()`方法。

```scala
true
true
true
false
```

**可有可无的分号**

在涉及语句或者表达式的终止时，Scala很厚道——分号(`;`)是可选的，这就能够减少代码中的噪声。然而，Scala在某些上下文中要求在`{`前面有一个分号。
```scala
Created list1
Created List2
class java.util.ArrayList
class $line40.$read$$iw$$iw$$iw$$iw$$iw$$iw$$iw$$iw$$anon$1
```

在定义`list1`的时候放置了一个分号，因此，紧随其后的`{`开启了一个新的代码块。然后，在定义`list2`的时候没有写分号，所以Scala会假定是在创建一个继承自`ArrayList[Int]`的匿名内部类。
**避免显示return**

在Java中，使用`return`语句从方法返回结果。而`return`语句在Scala中是隐式的，显式地放置一个`return`命令会影响Scala推断返回类型的能力。

在下面的代码中，Scala非常愉快地推断出了`check1()`方法地返回类型。但是由于在方法`check2()`中使用了一个显式的`return`，所以Scala没有推断出类型。在这种情况下，必须提供返回类型`Boolean`。

即使你选择提供返回类型，也最好避免显式的`return`命令。`check3`方法就是一个很好的示范。
#### 3.11 默认访问修饰符

在不使用任何访问修饰符的情况下，Scala默认类、字段和方法都是`public`的。
```scala
Started
```

Java的`protected`对任意包中的派生类和当前包的任意类是可见的。然而Scala的`protected`与C++类似，只有派生类能够访问。更近一步，派生类在访问`protected`成员的时候，成员的类型也需要一致。