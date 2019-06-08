---
title: 5 Singleton Pattern
toc: false
date: 2017-10-30
---

In many ways, the **Singleton Pattern**(单例模式) is a convention for ensuring one and only one object is instantiated for a given class. It is often used to manage pools of resources, like connection or thread pools.

> The Singleton Pattern ensures a class has only one instance, and provides a global point of access to it.

### Lazily Created Instance

懒汉式(lazily created instance)在多线程环境下是不安全的，如果多个线程能够同时进入`:::Java if (uniqueInstance == null)`，并且此时 `uniqueInstance`为 null，那么会有多个线程执行`:::java uniqueInstance = new Singleton();` 语句，这将导致实例化多次`uniqueInstance`。


```Java
public class Singleton {
    // We have a static variable to 
    // hold our one instance of the class Singleton.
    private static Singleton uniqueInstance;
    // Our constructor is declared private; 
    // only Singleton can instantiate this class!
    private Singleton() {}
    
    // The getInstance() method gives us a way to 
    // instantiate the class and also to return an instance of it.
    public static Singleton getInstance() {
        if (uniqueInstance == null)
            uniqueInstance = new Singleton();
        return uniqueInstance;
    }
    
    // other useful methods here
    public String getDescription() {
        return "I'm a classic Singleton!";
    }
}
```

![The Singleton Pattern ClassDiagram](figures/TheSingletonPatternClassDiagram.png)

### Eagerly Created Instance

Move to an **eagerly created instance**(饿汉式) rather than a lazily created one(懒汉式). 线程不安全问题主要是由于`uniqueInstance`被实例化多次，采取直接实例化`uniqueInstance`的方式就不会产生线程不安全问题。



```Java
public class Singleton {
    private static Singleton uniqueInstance = new Singleton();
    private Singleton() {}
    public static Singleton getInstance() {
        return uniqueInstance;
    }
}
```

![](figures/EagerSingleton.jpg)




### Synchronized Method

懒汉式-线程安全: 只需要对`getUniqueInstance()`方法加锁，那么在一个时间点只能有一个线程能够进入该方法，从而避免了实例化多次`uniqueInstance`。

we almost trivially fix it by making `getInstance()` a synchronized method:

```Java
public class Singleton {
	private static Singleton uniqueInstance;
	// other useful instance variables here
	private Singleton() {}
 
	public static synchronized Singleton getInstance() {
		if (uniqueInstance == null)
			uniqueInstance = new Singleton();
		return uniqueInstance;
	}
 
	// other useful methods here
	public String getDescription() {
		return "I'm a thread safe Singleton!";
	}
}
```

Good point, and it’s actually a little worse than you make out: the only time synchronization is relevant is the first time through this method. Once we’ve set the uniqueInstance variable to an instance of Singleton, we have no further need to synchronize this method.


* Do nothing if the performance of `getInstance()` isn’t critical to your application.





### Static Inner Class

```Java
public class Singleton {  
    private static class SingletonHolder {  
        private static final Singleton uniqueInstance 
                                = new Singleton();  
    }  
    private Singleton (){}  
    public static final Singleton getInstance() {  
        return SingletonHolder.uniqueInstance;  
    }  
}
```

静态内部类利用了`classloader`机制保证初始化`uniqueInstance`时只有一个线程。注意只有当调用`getInstance`方法时，才会装载`SingletonHolder`，初始化`uniqueInstance`。

### Double-checked locking

With double-checked locking(双重校验锁), we first check to see if an instance is created, and if not, THEN we synchronize. This way, we only synchronize the first time through, just what we want.

```Java
public class Singleton {
	private volatile static Singleton uniqueInstance;
	private Singleton() {}
	public static Singleton getInstance() {
	   // check for an instance and if there isn't one, 
	   // enter a synchronized block
	   // Note we only synchronize the first time through!
		if (uniqueInstance == null) {
			synchronized (Singleton.class) { // only synchronized here
			   // Once in the block, check again and
			   // if still null, create an instance
				if (uniqueInstance == null)
					uniqueInstance = new Singleton();
			}
		}
		return uniqueInstance;
	}
}
```

!!! note
    
    使用`Singleton.class` 而不是`this`,是因为`getInstance()`是一个静态方法。静态方法没有this关键字(见[Head First Java](../Head First Java/10 Numbers and Statics.md))。

采用`volatile`关键字修饰也是很有必要的，`:::java uniqueInstance = new Singleton()`; 这段代码其实是分为三步执行：

1. 为`uniqueInstance`分配内存空间
2. 初始化`uniqueInstance`
3. 将`uniqueInstance`指向分配的内存地址

但是由于JVM会重排指令，执行顺序有可能变成 1->3->2。指令重排在单线程环境下不会出现问题，但是在多线程环境下会导致一个线程获得还没有初始化的实例。例如，线程T1执行了1和 3，此时线程T2调用`getUniqueInstance()`后发现 `uniqueInstance`不为空，因此返回`uniqueInstance`，但此时`uniqueInstance`还未被初始化。

使用`volatile`可以**禁止指令重排序优化**，保证在多线程环境下也能正常运行(volatile的讨论参见[深入了解Java虚拟机](../深入理解Java虚拟机/12 Java内存模型与线程.md/#volatile))。


#### 问题: 序列化

为了序列化单例，需要实现`Serializable`接口，但是仅仅这么做是不够的。通过对单例的序列化与反序列化得到将是一个全新的对象，违反了单例性。

!!! example "序列化/反序列化后的对象是全新对象"

    ```Java
    public static void main(String[] agrs) throws Exception  {
        // 序列化：把singleton写入到文件中
        FileOutputStream fileOutputStream = 
                new FileOutputStream("singleton.ser");
        ObjectOutputStream objectOutputStream = 
                new ObjectOutputStream(fileOutputStream);
        objectOutputStream.writeObject(Singleton.getInstance());
        objectOutputStream.close();
    
        // 反序列化：从文件中读取singleton
        FileInputStream fileInputStream = 
                new FileInputStream("singleton.ser");
        ObjectInputStream objectInputStream = 
                new ObjectInputStream(fileInputStream);
        Singleton anotherSingleton = 
                (Singleton) objectInputStream.readObject();
        objectInputStream.close();
        
        // 是不是同一个对象？结果: false
        System.out.println(anotherSingleton 
                        == Singleton.getInstance());
    }
    ```

一个解决方法是添加`readResolve()`方法。

> `readResolve()` is used for replacing the object read from the stream. A common usage  is enforcing singletons; when an object is read, replace it with the singleton instance. This ensures that nobody can create another instance by serializing and deserializing the singleton. [ref](https://stackoverflow.com/questions/1168348/java-serialization-readobject-vs-readresolve)

```Java
public class Singleton {
    ....
    private Object readResolve() {
       // instead of the object we're on,
       // return the class variable INSTANCE
      return uniqueInstance;
}
```

其具体原因是：

> The `readResolve` method is called when `ObjectInputStream` has read an object from the stream and is preparing to return it to the caller. `ObjectInputStream`  checks whether the class of the object defines the `readResolve` method. If the method is defined, the `readResolve` method is called to allow the object in the stream to designate the object to be returned. The object returned should be of a type that is compatible with all uses. If it is not compatible, a `ClassCastException` will be thrown when the type mismatch is discovered.



#### 问题: 反射

在运行时用户通过反射可以改变单例的私有构造函数。 下面一个例子修改了使用了双重校验锁的单例的构造函数，使其构造函数从私有变成共有。

```Java
public class Singleton {
    private int val;
    private static Singleton uniqueInstance;
    private Singleton() {};
    public static Singleton getInstance() {
        if (uniqueInstance == null) {
            synchronized (Singleton.class){
                if (uniqueInstance == null)
                    uniqueInstance = new Singleton();
            }
        }
        return uniqueInstance;
    }

    public void setValue(int val) {
        this.val = val;
    }

    public int getValue() {
        return val;
    }


    public static void main(String[] args) throws Exception {
        Singleton singleton = Singleton.getInstance(); // 获得单例
        // 获取单例构造函数
        Constructor constructor = 
                Singleton.class.getDeclaredConstructors()[0];
        // 修改单例构造函数
        constructor.setAccessible(true); // private -> public
        Singleton singleton2 = (Singleton)constructor.newInstance();
        if (singleton == singleton2) System.out.println("Objects are same.");
        else System.out.println("Objects are not same.");
        singleton.setValue(1);
        singleton2.setValue(2);
        System.out.println(singleton.getValue());
        System.out.println(singleton2.getValue());
    }
}
// Two objects are not same.
// 1
// 2
```

### Enum

枚举不仅能避免多线程同步问题，而且还能防止反序列化重新创建新的对象。

关于Enum的用法和原理见[Java编程思想](../Java编程思想/20 枚举类型.md)

> This approach is functionally equivalent to the public field approach, except that it is more concise, provides the serialization machinery for free, and provides an ironclad guarantee against multiple instantiation, even in the face of sophisticated serialization or reflection attacks. While this approach has yet to be widely adopted, *a single-element enum type is the best way to implement a singleton*. <small>[Effective Java](../Effective Java/2 Creating and Destroying Objects.md)</small>


```Java
public enum Singleton {  
    INSTANCE;  
    public void whateverMethod() {  
    }  
}  
```

1. 线程安全：`Enum`中的枚举项实际上static类变量，static类型的属性会在类被加载之后被初始化。当一个Java类第一次被真正使用到的时候静态资源被初始化，Java类的加载和初始化过程都是线程安全的。所以，创建一个enum类型是线程安全的。
2. 反序列化: 普通的Java类的反序列化过程中，会通过反射调用类的默认构造函数来初始化对象。所以，即使单例中构造函数是私有的，也会被反射给破坏掉。由于反序列化后的对象是重新new出来的，所以这就破坏了单例。但是，枚举的反序列化并不是通过反射实现的。所以，也就不会发生由于反序列化导致的单例破坏问题。

> Enum constants are serialized differently than ordinary serializable or externalizable objects. The serialized form of an enum constant consists solely of its name; field values of the constant are not present in the form. To serialize an enum constant, `ObjectOutputStream` writes the value returned by the enum constant's name method. To deserialize an enum constant, `ObjectInputStream` reads the constant name from the stream; the deserialized constant is then obtained by calling the `java.lang.Enum.valueOf` method, passing the constant's enum type along with the received constant name as arguments. Like other serializable or externalizable objects, enum constants can function as the targets of back references appearing subsequently in the serialization stream.

> The process by which enum constants are serialized cannot be customized: any class-specific `writeObject`, `readObject`, `readObjectNoData`, `writeReplace`, and `readResolve` methods defined by enum types are *ignored* during serialization and deserialization. Similarly, any `serialPersistentFields` or `serialVersionUID` field declarations are also ignored--all enum types have a fixed `serialVersionUID`  of 0L. Documenting serializable fields and data for enum types is unnecessary, since there is no variation in the type of data sent. [Java Object Serialization Specification](https://docs.oracle.com/javase/7/docs/platform/serialization/spec/serial-arch.html#6469)


!!! example "Enum例子"

```Java tab="Employee"
public enum Employee {
    INSTANCE;
    private int id;
    private String name;

    Employee() { }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

```java tab="Redis"
// 使用连接池封装Redis连接工具类
public enum RedisUtils {
    INSTANCE;

    private final JedisPool pool;
    RedisUtils() {
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        pool = new JedisPool(poolConfig, "localhost");
    }

    public void hset(String key, String field, String value) {
        try (Jedis jedis = pool.getResource()) {
            jedis.sadd(key, field, value);
        }
    }

    public String hget(String key, String field) {
        try (Jedis jedis = pool.getResource()) {
            return jedis.hget(key, field);
        }
    }

    public boolean hexists(String key, String field) {
        try (Jedis jedis = pool.getResource()) {
            return jedis.hexists(key, field);
        }
    }
}
```