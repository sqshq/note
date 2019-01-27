### **Appendix: The Top Ten Topics**

### 10 Bit Manipulation

Bitwise NOT Operator: `~`, "flips all the bits of primitive"

```Java
int x = 10; // bits are 00001010
x = ~x; // bits are now 11110101
```

Bitwise AND Operator: &, returns a value whose bits are turned on only if *both* original bits are turned on:

```Java
int a = x&y; //bits are 0000010
```

Bitwise OR Operator: |, returns a value whose bits are turned on only if *either* of the original bits are turned on;

```Java
int a = x|y; //bits are 00001110
```

Right Shift Operator: >> , the sign bit does *not* change;

```Java
int y = x >> 2; //bits are 11111101
```

Unsigned Right Shift Operator: >>>, the sign bit *might* change:

```Java
int y = x >>> 2; //bits are 00111101
```

Left Shift Operator: <<, the sign bit might change.

```Java
int y = x << 2; //bits are 11010100
```



### 9 Immutability

> An object is considered immutable if its state cannot change after it is constructed. <small>[[Immutable Object](https://docs.oracle.com/javase/tutorial/essential/concurrency/immutable.html)]</small>


For security purposes, and for the sake of conserving memory, <C>String</C>s in Java are immutable. Whenever you make a new <C>String</C>, the JVM puts it into a special part of memory called the "String pool".

Wrappers are  Immutable. There is no setter method for a wrapper object.

### 8 Assertions

Add assertion statements to your code whenever you believe that something *must be true*. For instance:

```Java
assert (height > 0);
// if true, program continues normally
// if false, throw an AssertionEror
```

You can add a little more information to the stack trace by saying:

```Java
assert (height > 0) : “height = “ + height + “ weight = “ + weight;
```

To compile and run with assertions:

```Java
javac TestDriveGame, java // no command lines options were necesseary
java -ea TestDriveGame
```

### 7 Block Scope

略

### 6 Linked Invocations

略(obvious)

### 5 Anonymous and Static Nested Classes

Any Java class that's defined within the scope of another class is a ***nested*** class(嵌套类). And *non-static* class are often referred to as ***inner** classes(内部类).

There are other kinds of inner classes including *static* and *anonymous*.

#### static nested classes


A **static nested class**(静态嵌套类) is  a class enclosed with another, and marked with the static modifier. Because static nested classes are still considered a *member* of the enclosing/outer class, they still get access to any private members of the outer class.. but *only the ones that are also static*.

```Java
public class FooOuter {
    static class BarInner { 
        void sayIt() {
        System.out.println(“method of a static inner class”); }
    }
}
class Test { 
    public static void main (String[] args) {
        FooOuter.BarInner
        foo.sayIt();
        foo = new FooOuter.BarInner();
    }
}
```

#### Anonymous inner classes

Anonymous (inner) classes(匿名内部类) enable you to make your code more concise. They enable you to declare and instantiate a class at the same time. They are like local classes except that they do not have a name. Use them if you need to use a local class only once.

```Java
button.addActionListener(new ActionListener() { 
    public void actionPerformed(ActionEvent ev) { 
    System.exit(0); 
    }
});
```

### 4 Access Levels and Access Modifiers

略

### 3 String and StringBuffer/StringBuilder Methods

> <C>StringBuffer</C> is a thread-safe, mutable sequence of characters. A string buffer is like a <C>String</C>, but can be modified. 
> String buffers are safe for use by multiple threads. The methods are synchronized where necessary so that all the operations on any particular instance behave as if they occur in some serial order that is consistent with the order of the method calls made by each of the individual threads involved. [[JavaDOC -StringBuffer](https://docs.oracle.com/javase/7/docs/api/java/lang/StringBuffer.html)]


```Java
public synchronized StringBuffer append(String str) {
        toStringCache = null;
        super.append(str);
        return this;
    }
```

The <C>StringBuilder</C> class is not synchronized, hence with less overhead in a single threaded environment. As of Java 5.0, you should use the <C>StringBuilder</C> class instead of <C>StringBuffer</C>, unless your <C>String</C> manipulations need to be thread-safe, which is uncommon.


The <C>StringBuiler</C> & <C>StringBuffer</C> classes have:

```Java
StringBxxxx delete(int start, int end); // delete a portion
StringBxxxx insert(int offset, any primitive or a char[]); // insert something
StringBxxxx replace(int start, int end, String s); // replace this part with this String
StringBxxx reverse(); // reverse the SB from front to back
void setCharAt(int index, char ch); // replace a given character
```


### 2 Multidimensional Arrays


### 1 Enumerations

An *enumeration* is a set of valid values.

Before Java5.0, you could only do a half-baked job of creating an enumeration in Java:

```Java
public static final int JERRY = 1; 
public static final int BOBBY = 2; 
public static final int PHIL = 3;
```

As of Java 5.0, you can create full-fledged enumerations using <C>enum</C> keyword.

```Java
public enum Members {JERRY, BOBBY, PHIL};
// The "selectedBandMember" variable is of type "Members", 
// and can ONLY have a value of JERRY, BOBBY, PHIL.
public Members selectedBandMember; 

// later in the code
if (selectedBandMember == Members.JERRY) { 
    // do JERRY related stuff 
}
```

when you create an enum, you're creating A NEW CLASS, and **you're implicitly extending** <C>java.lang.Enum</C>.

```Java
public abstract class Enum<E extends Enum<E>> extends Object 
    implements Comparable<E>, Serializable
```

#### Using "if" and "switch" with Enums

Using the enum, we can perform branches  using either the <C>if</C> or <C>switch</C> statement. Also we can compare enum instances using either `==` or the <C>.equals()</C> method. Usually `==` is considered better style.

```Java
Members n = Members.BOBBY; 
if (n.equals(Members.JERRY)) System.out.println(“Jerrrry!”); 
if (n == Members.BOBBY) System.out.println(“Rat Dog”);

Members ifName = Members.PHIL; 
switch (ifName) {
    case JERRY: System.out.print(“make it sing “);
    case PHIL: System.out.print(“go deep “);
    case BOBBY: System.out.println(“Cassidy! ”); 
}
```















