---
title: 6 Read-Write Lock模式
---

在Read-Write Lock模式中，当线程执行读取操作时，多个线程可以同时读取，但不可以写入；当线程写入时，其他线程不可以读取和写入。

一般来说，执行互斥处理会降低程序性能。但如果把针对写入的互斥处理和针对读取的互斥处理分别来考虑，则可以提高程序性能。

### 示例程序


```Java
public class Data {
    private final char[] buffer;
    private final ReadWriteLock lock = 
                new ReentrantReadWriteLock(true /* fair */);
    private final Lock readLock = lock.readLock();
    private final Lock writeLock = lock.writeLock();

    public Data(int size) {
        this.buffer = new char[size];
        Arrays.fill(buffer, '*');
    }
    
    public char[] read() throws InterruptedException {
        readLock.lock();
        try {
            return doRead();
        } finally {
            readLock.unlock();
        }
    }
    
    public void write(char c) throws InterruptedException {
        writeLock.lock();
        try {
            doWrite(c);
        } finally {
            writeLock.unlock();
        }
    }
    
    private char[] doRead() {
        char[] newbuf = new char[buffer.length];
        System.arraycopy(buffer, 0, newbuf, 0, buffer.length);
        return newbuf;
    }
    
    private void doWrite(char c) {
        Arrays.fill(buffer, c);
    }
}
```