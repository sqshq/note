---
title: 4 Balking模式
---

如果现在不适合执行这个操作，或者没必要执行这个操作，就停止处理，直接返回，这就是Balking模式。所谓Balk就是“停止并返回”的意思。


#### 示例程序

示例程序试图实现文本工具的自动保存功能，定期将当前数据内容写入文件中。当数据内容被写入时，会完全覆盖上次写入的内容，只有最新的内容才会被保存。另外，当保存内容未发生改变时，就不再执行写入操作。也就是说，该程序以"数据内容存在不同"为守护条件，如果数据内容相同，则不执行写入操作，直接返回。

| 名字 | 说明 |
| --- | --- |
| Data | 表示可以修改并保存的数据的类 |
| SaverThread |	 定期保存数据内容的类 |
| ChangerThread | 修改并保存数据内容的类 |
| Main | 测试程序行为的类 |


```Java
public class Data {
    private final String filename;  // 保存的文件名称
    private String content;         // 数据内容
    private boolean changed;        // 修改后的内容若未保存，则为true

    public Data(String filename, String content) {
        this.filename = filename;
        this.content = content;
        this.changed = true;
    }

    // 修改数据内容
    public synchronized void change(String newContent) {
        content = newContent;
        changed = true;
    }

    // 若数据内容修改过，则保存到文件中
    public synchronized void save() throws IOException {
        if (!changed) return;
        doSave();
        changed = false;
    }

    // 将数据内容实际保存到文件中
    private void doSave() throws IOException {
        System.out.println(Thread.currentThread().getName() + " calls doSave, content = " + content);
        Writer writer = new FileWriter(filename);
        writer.write(content);
        writer.close();
    }
}
```

```java tab="SaverThread"
// 实现定期保存
public class SaverThread implements Runnable {
    private final Data data;
    private final String name;

    public SaverThread(String name, Data data) {
        this.name = name;
        this.data = data;
    }

    public void run() {
        try {
            while (true) {
                data.save();         // 定期保存数据
                Thread.sleep(1000);  // 休眠约1秒钟
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
```

```java
// 用户修改数据内容，并执行保存处理
public class ChangerThread implements Runnable {
    private final Data data;
    private final String name;
    private final Random random = new Random();
    public ChangerThread(Data data, String name) {
        this.data = data;
        this.name = name;
    }

    public void run() {
        try {
            for (int i = 0; true; i++) {
                data.change("No." + i); // 修改数据
                Thread.sleep(random.nextInt(1000)); // 执行其他操作
                data.save();        // 显式地保存
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

Balking模式中，当守护条件不成立时，线程会直接停止并返回。而Guarded Suspension模式中，当守护条件不成立时，线程会一直等待到成立为止。

![balking](figures/balking.png)


#### 延伸阅读：超时

介于"直接balk并返回"和"等待到守护条件成立为止"这两种阶段的处理方法之间，还有一种处理方法，那就是"在守护条件成立之前等待一段时间"。这种处理称为guarded timed或timeout。

```java
public class Host {
    private final long timeout; //超时时间
    private boolean ready = false; // 方法正常执行时值为true
    public Host(long timeout) {
        this.timeout = timeout;
    }
    // 修改状态
    public synchronized  void setExecutable(boolean on) {
        ready = on;
        notifyAll();
    }

    // 检查状态之后再执行
    public synchronized void execute()
            throws InterruptedException, TimeoutException {
        long start = System.currentTimeMillis(); // 开始时间
        while (!ready) {
            long now = System.currentTimeMillis(); // 当前时间
            long rest = timeout - (now - start); // 剩余的等待时间
            if (rest <= 0) throw new TimeoutException();
            wait(rest);
        }
        doExecute();
    }

    // 实际的处理
    private void doExecute() {
        System.out.println(Thread.currentThread().getName() + "calls do Execute");
    }
}
```