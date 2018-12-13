---
title: 4 Balking模式
---

如果现在不适合执行这个操作，或者没必要执行这个操作，就停止处理，直接返回，这就是Balking模式。所谓Balk就是“停止并返回”的意思。


### 示例程序

程序要实现文本工具的自动保存功能，定期将当前数据内容写入文件中。当数据内容被写入时，会完全覆盖上次写入的内容，只有最新的内容才会被保存。另外，当保存内容未发生改变时，就不再执行写入操作。也就是说，该程序以“数据内容存在不同”为守护条件，如果数据内容相同，则不执行写入操作，直接返回。

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
        if (!changed) {
            return;
        }
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

Balking模式中，当守护条件不成立时，线程会直接停止并返回。而Guarded Suspension模式中，当守护条件不成立时，线程会一直等待到成立为止。