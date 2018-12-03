### Concurrent Programming in Java 1: Threads and Locks



### Threads

A unique aspect of Java compared to prior mainstream programming languages is that Java included the notions of threads (as instances of the $\mathtt {java.lang.Thread}$ class) in its language definition right from the start.

When an instance of $\mathtt {Thread}$ is created (via a $\mathtt {new}$ operation), it does not start executing right away; instead, it can only start executing when its $\mathtt {start}()$ method is invoked. The statement or computation to be executed by the thread is specified as a parameter to the constructor.

The $\mathtt {Thread}$ class also includes a wait operation in the form of a $\mathtt {join}()$ method. If thread $\mathtt {t0}$ performs a $\mathtt {t1.join}()$ call, thread $\mathtt {t0}$ will be forced to wait until thread $\mathtt {t1}$ completes, after which point it can safely access any values computed by thread $\mathtt {t1}$. Since there is no restriction on which thread can perform a $\mathtt {join}$ on which other thread, it is possible for a programmer to erroneously create a deadlock cycle with $\mathtt {join}$ operations. (A deadlock occurs when two threads wait for each other indefinitely, so that neither can make any progress.)

#### Thread creation

[Java Tutorials - Defining and Starting a Thread](https://docs.oracle.com/javase/tutorial/essential/concurrency/runthread.html)

An application that creates an instance of $\mathtt {Thread}$ must provide the code that will run in that thread. There are two ways to do this:

* *Provide a Runnable object*. The <C>Runnable</C> interface defines a single method, <C>run</C>, meant to contain the code executed in the thread. The Runnable object is passed to the <C>Thread</C> constructor, as in the HelloRunnable example:

```Java
public class HelloRunnable implements Runnable {

    public void run() {
        System.out.println("Hello from a thread!");
    }

    public static void main(String args[]) {
        (new Thread(new HelloRunnable())).start();
    }

}
```

* <i>Subclass <C>Thread</C></i>. The <C>Thread</C> class itself implements <C>Runnable</C>, though its <C>run</C> method does nothing. An application can subclass <C>Thread</C>, providing its own implementation of <C>run</C>, as in the HelloThread example:

```Java
public class HelloThread extends Thread {

    public void run() {
        System.out.println("Hello from a thread!");
    }

    public static void main(String args[]) {
        (new HelloThread()).start();
    }

}
```

Which of these idioms should you use? The first idiom, which employs a <C>Runnable</C> object, is more general, because the <C>Runnable</C> object can subclass a class other than <C>Thread</C>. 

#### Synchronized Methods

[Java tutorials - Synchronized Methods](https://docs.oracle.com/javase/tutorial/essential/concurrency/syncmeth.html)

Making methods synchronized has two effects:

* First, it is NOT possible for two invocations of synchronized methods on the same object to interleave. When one thread is executing a synchronized method for an object, all other threads that invoke synchronized methods for the same object block (suspend execution) until the first thread is done with the object.
* Second, when a synchronized method exits, it automatically establishes a happens-before relationship with any subsequent invocation of a synchronized method for the same object. This guarantees that changes to the state of the object are visible to all threads.

### Structured Locks

Structured locks can be used to enforce mutual exclusion and avoid data races.

A major benefit of structured locks is that their acquire and release operations are **implicit**, since these operations are automatically performed by the Java runtime environment when entering and exiting the scope of a <C>synchronized</C> statement or method, even if an exception is thrown in the middle.

<C>wait()</C> and <C>notify()</C> operations can be used to block and resume threads that need to wait for specific conditions.

#### Guarded Blocks

[Java Tutorials - Guarded Blocks](https://docs.oracle.com/javase/tutorial/essential/concurrency/guardmeth.html)

**Guarded block** is the most common coordination idiom. It begins by polling a condition that before the block can proceed.

Suppose, for example <C>guardedJoy</C> is a method that must not proceed until a shared variable <C>joy</C> has been set by another thread. An efficient guard invokes <C>Object.wait</C> to suspend the current thread. The invocation of <C>wait</C> does not return until another thread has issued a notification that some special event may have occurred.

```Java

public void guardedJoy() {
    // Simple loop guard. Wastes
    // processor time. Don't do this!
    while(!joy) {}
    System.out.println("Joy has been achieved!");
}
```

A more efficient guard invokes <C>Object.wait</C> to suspend the current thread. The invocation of wait does not return until another thread has issued a notification that some special event may have occurred — though not necessarily the event this thread is waiting for:

```Java
public synchronized void guardedJoy() {
    // This guard only loops once for each special event, which may not
    // be the event we're waiting for.
    while(!joy) {
        try {
            wait();
        } catch (InterruptedException e) {}
    }
    System.out.println("Joy and efficiency have been achieved!");
}
```

When <C>wait</C> is invoked, the thread releases the lock and suspends execution. At some future time, another thread will acquire the same lock and invoke <C>Object.notifyAll</C>, informing all threads waiting on that lock that something important has happened:

```Java
public synchronized notifyJoy() {
    joy = true;
    notifyAll();
}
```

!!! Note
    <C>notifyAll()</C> wakes up all threads that are waiting on the object's monitor.
    
    <C>notify</C> wakes up a single thread that is waiting on this object's monitor. 
    
!!! Question
    What's the **useful** difference between <C>notify()</C> and <C>notifyAll()</C>? [[ref](https://stackoverflow.com/questions/37026/java-notify-vs-notifyall-all-over-again)]
    
    Simply put, choosing one of them depends on why your threads are waiting to be notified.
    
    In some cases, all waiting threads can take useful action once the wait finishes. Suppose a set of threads waiting for a certain task to finish; once the task has finished, all waiting threads can continue with their business. In such a case you would use <C>notifyAll()</C> to wake up all waiting threads at the same time.

    Another case, for example mutually exclusive locking, only one of the waiting threads can do something useful after being notified (in this case acquire the lock). In such a case, you would rather use <C>notify()</C>. Properly implemented, you could use <C>notifyAll()</C> in this situation as well, but you would unnecessarily wake threads that can't do anything anyway.



Let's use guarded blocks to create a Producer-Consumer application. This kind of application shares data between two threads: the producer, that creates the data, and the consumer, that does something with it. The two threads communicate using a shared object. Coordination is essential: the consumer thread must not attempt to retrieve the data before the producer thread has delivered it, and the producer thread must not attempt to deliver new data if the consumer hasn't retrieved the old data.

The data is a series of text messages, which are shared through an object of type Drop.


```Java fct_label="Drop"
public class Drop {
    // Message sent from producer
    // to consumer.
    private String message;
    // True if consumer should wait
    // for producer to send message,
    // false if producer should wait for
    // consumer to retrieve message.
    private boolean empty = true;

    public synchronized String take() {
        // Wait until message is
        // available.
        while (empty) {
            try {
                wait();
            } catch (InterruptedException e) {}
        }
        // Toggle status.
        empty = true;
        // Notify producer that
        // status has changed.
        notifyAll();
        return message;
    }

    public synchronized void put(String message) {
        // Wait until message has
        // been retrieved.
        while (!empty) {
            try { 
                wait();
            } catch (InterruptedException e) {}
        }
        // Toggle status.
        empty = false;
        // Store message.
        this.message = message;
        // Notify consumer that status
        // has changed.
        notifyAll();
    }
}
```

```Java fct_label="Producer"
import java.util.Random;

public class Producer implements Runnable {
    private Drop drop;

    public Producer(Drop drop) {
        this.drop = drop;
    }

    public void run() {
        String importantInfo[] = {
            "Mares eat oats",
            "Does eat oats",
            "Little lambs eat ivy",
            "A kid will eat ivy too"
        };
        Random random = new Random();

        for (int i = 0; i < importantInfo.length; i++) {
            drop.put(importantInfo[i]);
            try {
                Thread.sleep(random.nextInt(5000));
            } catch (InterruptedException e) {}
        }
        drop.put("DONE");
    }
}
```

```Java fct_label="Consumer"
import java.util.Random;

public class Consumer implements Runnable {
    private Drop drop;

    public Consumer(Drop drop) {
        this.drop = drop;
    }

    public void run() {
        Random random = new Random();
        for (String message = drop.take(); ! message.equals("DONE"); message = drop.take()) {
            System.out.format("MESSAGE RECEIVED: %s%n", message);
            try {
                Thread.sleep(random.nextInt(5000));
            } catch (InterruptedException e) {}
        }
    }
}
```

```Java fct_label="Example"
public class ProducerConsumerExample {
    public static void main(String[] args) {
        Drop drop = new Drop();
        (new Thread(new Producer(drop))).start();
        (new Thread(new Consumer(drop))).start();
    }
}
```

#### Intrinsic Locks and Synchronization

[Tutorial on Intrinsic Locks and Synchronization in Java](https://docs.oracle.com/javase/tutorial/essential/concurrency/locksync.html)

Every object has an **intrinsic lock**(also, **monitor lock **or **monitor**) associated with it.

By convention, a thread that needs exclusive and consistent access to an object's fields has to acquire the object's intrinsic lock before accessing them, and then release the intrinsic lock when it's done with them.


**Locks In Synchronized Methods** 

When a thread invokes a synchronized method, it automatically acquires the intrinsic lock for that method's object and releases it when the method returns. The lock release occurs even if the return was caused by an uncaught exception.

!!! note
    When a static synchronized method is invoked, since a static method is associated with a class, not an object, the thread acquires the intrinsic lock for the Class object associated with the class. Thus access to class's static fields is controlled by a lock that's distinct from the lock for any instance of the class.

**Synchronized Statements**

Synchronized statements must specify the object that provides the intrinsic lock:

```Java
public void addName(String name) {
    synchronized(this) {
        lastName = name;
        nameCount++;
    }
    nameList.add(name);
}
```

**Reentrant Synchronization**

A thread can acquire a lock that it already owns. Allowing a thread to acquire the same lock more than once enables **reentrant synchronization**(重入同步).

### Unstructured Locks

#### ReentrantLock

A **ReentrantLock**(重入锁) is *unstructured*, unlike synchronized constructs -- i.e. you don't need to use a block structure for locking and can even hold a lock across methods.

A reentrant mutual exclusion <C>Lock</C> with the same basic behavior and semantics as the implicit monitor lock accessed using synchronized methods and statements, but with extended capabilities.[[Java Doc-Class ReentrantLock](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/locks/ReentrantLock.html#tryLock())]

> A ReentrantLock is owned by the thread last successfully locking, but not yet unlocking it. A thread invoking lock will return, successfully acquiring the lock, when the lock is not owned by another thread.


It is recommended practice to *always* immediately follow a call to <C>lock</C> with a <C>try</C> block, most typically in a before/after construction such as:

```Java
class X {
   private final ReentrantLock lock = new ReentrantLock();
   // ...

   public void m() {
     lock.lock();  // block until condition holds
     try {
       // ... method body
     } finally {
       lock.unlock()
     }
   }
 }
```
 
#### Interface Lock

[Java Doc-Interface Lock](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/locks/Lock.html)


```Java
public interface Lock
```

<C>Lock</C> implementations provide more extensive locking operations than can be obtained using <C>synchronized</C> methods and statements. They allow more *flexible* structuring, may have quite different properties, and may support multiple associated <C>Condition</C> objects.


**Comparison with<C>synchronized</C> methods and statements**

The use of synchronized methods or statements provides access to the implicit monitor lock associated with every object, but forces all lock acquisition and release to occur in a **block-structured way**: when multiple locks are acquired they must be released in the opposite order, and all locks must be released in the same lexical scope in which they were acquired.


Implementations of the Lock interface enable the lock to be acquired and released in **different scopes**, and allowing multiple locks to be acquired and released in **any order**.

In most cases, the following idiom should be used:

```Java
Lock l = ...;
     l.lock();
     try {
         // access the resource protected by this lock
     } finally {
         l.unlock();
     }
```

!!! note
    When locking and unlocking occur in different scopes, care must be taken to ensure that all code that is executed while the lock is held is protected by <C>try-finally</C> or <C>try-catch</C> to ensure that the lock is released when necessary.

#### tryLock

[Java Doc - tryLock](https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/locks/Lock.html#tryLock())
 
<C>tryLock</C> acquires the lock ***only if it is free*** at the time of invocation.

A typical usage idiom for this method would be:

```Java
  Lock lock = ...;
  if (lock.tryLock()) {
      try {
          // manipulate protected state
      } finally {
          lock.unlock();
      }
  } else {
      // perform alternative actions
  }
```

### Liveness

> A concurrent application's ability to execute in a timely manner is known as its **liveness**. 


Common forms of Liveness failure:

* The first is **deadlock**, in which all threads are blocked indefinitely, thereby preventing any forward progress. 
* The second is **livelock**, in which all threads repeatedly perform an interaction that prevents forward progress, e.g., an infinite “loop” of repeating lock acquire/release patterns. 
* The third is **starvation**, in which at least one thread is prevented from making any forward progress.

[Liveness failures in detail on OSC](../osc/ch6.md/#8-liveness)






### Dining Philosophers

[Dining Philosophers described in OSC](../osc/ch7.md/#the-dining-philosophers-problem)


The philosophers follow the following protocol:

```Java
while(true) { 
    // Initially, thinking about life, universe, and everything
    think();
 
    // Take a break from thinking, hungry now
    pick_up_left_fork();
    pick_up_right_fork();
    eat();
    put_down_right_fork();
    put_down_left_fork();
 
    // Not hungry anymore. Back to thinking!
}
```

#### Implementation

[The Dining Philosophers Problem in Java](https://www.baeldung.com/java-dining-philoshophers)

We model each of our philosophers as classes that implement the Runnable interface so that we can run them as separate threads. Each Philosopher has access to two forks on his left and right sides. 

Consider a situation in which all philosophers grab the left fork/chopsticks at the same time, leading to the deadlock.

Simply, We introduce the condition that makes the last philosopher reach for his right fork first, instead of the left. This breaks the circular wait condition and we can avert the deadlock.

```Java fct_label="DiningPhilosophersTable"
public class DiningPhilosophersTable {
    private static int numPhilosophers;
    private static int numForks;

    public DiningPhilosophersTable(int num){
        this.numPhilosophers = num;
        this.numForks = num;

        Philosopher[] philosophers = new Philosopher[numPhilosophers];
        Fork[] forks = new Fork[numForks]; // Initialize array of forks

        for (int i = 0; i < numForks; i++) {
            forks[i] = new Fork(i+1);
        }

        for (int i = 0; i < numPhilosophers; i++) {
            // avoid deadlock: the last philosopher picks up the right fork first
            if (i == philosophers.length - 1) {
                philosophers[i] = new Philosopher(Integer.toString(i), 
                    forks[(i + 1) / numForks], forks[i]);
            } else {
                philosophers[i] = new Philosopher(Integer.toString(i), 
                    forks[i], forks[(i + 1) / numForks]);
            }
        }

        for (int i = 0; i < numPhilosophers; i++) {
            Thread thread = new Thread(philosophers[i], "Philosopher"+Integer.toString(i));
            thread.start();
        } // end for
    } // end constructor


    public static void main(String[] args) {
        DiningPhilosophersTable dining = new DiningPhilosophersTable(5);
    } // end main
}
```

```Java fct_label="Philosopher"
public class Philosopher implements Runnable {

    private Fork _left_fork;
    private Fork _right_fork;
    private String _name;

    public Philosopher(String name, Fork left_fork, Fork right_fork) {
        _name = name;
        _left_fork = left_fork;
        _right_fork = right_fork;
    }

    private void doAction(String action) {
        try {
            System.out.println(Thread.currentThread().getName() + " : " + action);
            Thread.sleep(((int) (Math.random() * 500)));
        } catch (InterruptedException ex){
            ex.printStackTrace();
        }
    }

    // Philosopher eats
    private void eat() {
        synchronized (_left_fork) {
            synchronized (_right_fork) {
                doAction("Eating, Using forks " + _left_fork.get_id() + ", "+ _right_fork.get_id());
            }
        }
    }

    // Philosopher thinks
    private void think() {
        doAction("Thinking");

    }

    @Override
    public void run() {
        for (int i=0; i<10; i++){
            eat();
            think();
        }
    }
}
```

```Java fct_label="fork"
public class Fork {
    private static int _id;

    public Fork(int id) {
        this._id = id;
    }

    public int get_id() {
        return _id;
    }
}
```

### Example: List

Using <C>ReentrantLock</C>, <C>ReentrantReadWriteLock</C>, <C>synchronized</C> method to synchronize list methods(add, remove, and contains).

*  Using <C>ReentrantLock</C> for Class  <C>CoarseLists</C>.
*  Using <C>ReentrantReadWriteLock</C> for Class  <C>RWCoarseList</C>.
*  Using <C>synchronized</C> method for Class  <C>SyncList</C>.
*  Class <C>ListSet</C> is an abstract class.

```Java fct_label="CoarseList"
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * Wrapper class for two lock-based concurrent list implementations.
 */
public final class CoarseLists {
    /**
     * An implementation of the ListSet interface that uses Java locks to
     * protect against concurrent accesses.
     *
     */
    public static final class CoarseList extends ListSet {


        private final ReentrantLock lock = new ReentrantLock();
        /**
         * Default constructor.
         */
        public CoarseList() {
            super();
        }

        /**
         * {@inheritDoc}
         *
         */
        @Override
        boolean add(final Integer object) {
            lock.lock();
            try {
                Entry pred = this.head;
                Entry curr = pred.next;

                while (curr.object.compareTo(object) < 0) {
                    pred = curr;
                    curr = curr.next;
                }

                if (object.equals(curr.object)) {
                    return false;
                } else {
                    final Entry entry = new Entry(object);
                    entry.next = curr;
                    pred.next = entry;
                    return true;
                }
            } finally {
                lock.unlock();
            }
        }

        /**
         * {@inheritDoc}
         *
         */
        @Override
        boolean remove(final Integer object) {
            lock.lock();
            try {
                Entry pred = this.head;
                Entry curr = pred.next;

                while (curr.object.compareTo(object) < 0) {
                    pred = curr;
                    curr = curr.next;
                }

                if (object.equals(curr.object)) {
                    pred.next = curr.next;
                    return true;
                } else {
                    return false;
                }
            } finally {
                lock.unlock();
            }
        }

        /**
         * {@inheritDoc}
         *
         */
        @Override
        boolean contains(final Integer object) {
            lock.lock();
            try {
                Entry pred = this.head;
                Entry curr = pred.next;

                while (curr.object.compareTo(object) < 0) {
                    pred = curr;
                    curr = curr.next;
                }
                return object.equals(curr.object);
            } finally {
                lock.unlock();
            }
        }
    }

    /**
     * An implementation of the ListSet interface that uses Java read-write
     * locks to protect against concurrent accesses.
     *
     */
    public static final class RWCoarseList extends ListSet {

        private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

        /**
         * Default constructor.
         */
        public RWCoarseList() {
            super();
        }

        /**
         * {@inheritDoc}
         *
         */
        @Override
        boolean add(final Integer object) {
            try {
                lock.writeLock().lock();

                Entry pred = this.head;
                Entry curr = pred.next;

                while (curr.object.compareTo(object) < 0) {
                    pred = curr;
                    curr = curr.next;
                }

                if (object.equals(curr.object)) {
                    return false;
                } else {
                    final Entry entry = new Entry(object);
                    entry.next = curr;
                    pred.next = entry;
                    return true;
                }
            } finally {
                lock.writeLock().unlock();
            }
        }

        /**
         * {@inheritDoc}
         *
         */
        @Override
        boolean remove(final Integer object) {
            try {
                lock.writeLock().lock();
                Entry pred = this.head;
                Entry curr = pred.next;

                while (curr.object.compareTo(object) < 0) {
                    pred = curr;
                    curr = curr.next;
                }

                if (object.equals(curr.object)) {
                    pred.next = curr.next;
                    return true;
                } else {
                    return false;
                }
            } finally {
                lock.writeLock().unlock();
            }
        }

        /**
         * {@inheritDoc}
         *
         */
        @Override
        boolean contains(final Integer object) {
            try {
                lock.readLock().lock();
                Entry pred = this.head;
                Entry curr = pred.next;

                while (curr.object.compareTo(object) < 0) {
                    pred = curr;
                    curr = curr.next;
                }
                return object.equals(curr.object);
            } finally {
                lock.readLock().unlock();
            }
        }
    }
}
```
```Java fct_label="SyncList"
/**
 *  Class SyncList implements a thread-safe sorted list data structure that
 *  supports contains(), add() and remove() methods.
 *
 *  Thread safety is guaranteed by declaring each of the methods to be
 *  synchronized.
 */
public final class SyncList extends ListSet {
    /**
     * Constructor.
     */
    public SyncList() {
        super();
    }

    /**
     * {@inheritDoc}
     */
    public synchronized boolean contains(final Integer object) {
        Entry pred = this.head;
        Entry curr = pred.next;

        while (curr.object.compareTo(object) < 0) {
            pred = curr;
            curr = curr.next;
        }
        return object.equals(curr.object);
    }

    /**
     * {@inheritDoc}
     */
    public synchronized boolean add(final Integer object) {
        Entry pred = this.head;
        Entry curr = pred.next;

        while (curr.object.compareTo(object) < 0) {
            pred = curr;
            curr = curr.next;
        }

        if (object.equals(curr.object)) {
            return false;
        } else {
            final Entry entry = new Entry(object);
            entry.next = curr;
            pred.next = entry;
            return true;
        }
    }

    /**
     * {@inheritDoc}
     */
    public synchronized boolean remove(final Integer object) {
        Entry pred = this.head;
        Entry curr = pred.next;

        while (curr.object.compareTo(object) < 0) {
            pred = curr;
            curr = curr.next;
        }

        if (object.equals(curr.object)) {
            pred.next = curr.next;
            return true;
        } else {
            return false;
        }
    }
}
```

```Java fct_label="ListSet"
/**
 * Lists that support this interface must be able to add
 * objects, remove objects, and test for existence of an object. These methods
 * are required to maintain a sorted list of items internally with no
 * duplicates.
 */
public abstract class ListSet {
    /**
     * Starting entry of this concurrent list.
     */
    protected final Entry head;

    /**
     * Default constructor.
     */
    public ListSet() {
        this.head = new Entry(Integer.MIN_VALUE);
        this.head.next = new Entry(Integer.MAX_VALUE);
    }

    /**
     * Getter for the head of the list.
     *
     * @return The head of this list.
     */
    public Entry getHead() {
        return head;
    }

    /**
     * Add an integer value to this sorted list, ensuring uniqueness. This
     * method must use ListSet.head as the head of the list.
     *
     * @param o The integer to add.
     * @return false if this value already exists in the list, true otherwise
     */
    abstract boolean add(Integer o);

    /**
     * Remove an integer value from this list if it exists. This method must use
     * ListSet.head as the head of the list.
     *
     * @param o The integer to remove.
     * @return true if this value is found in the list and successfully removed,
     *         false otherwise
     */
    abstract boolean remove(Integer o);

    /**
     * Check if this list contains the provided value. This method must use
     * ListSet.head as the head of the list.
     *
     * @param o The integer to check for.
     * @return true if this list contains the target value, false otherwise.
     */
    abstract boolean contains(Integer o);
}
```

### Java Volatile

The Java <C>volatile</C> keyword is used to mark a Java variable as "being stored in main memory". More precisely that means, that every read of a volatile variable will be read from the computer's main memory, and not from the CPU cache, and that every write to a volatile variable will be written to main memory, and not just to the CPU cache.


http://tutorials.jenkov.com/java-concurrency/volatile.html#variable-visibility-problems

https://stackoverflow.com/questions/106591/do-you-ever-use-the-volatile-keyword-in-java



https://www.cnblogs.com/chengxiao/p/6528109.html
