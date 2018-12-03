---
title: EOF
toc: false
date: 2017-08-17
tags: [C]
---

In computing, `end-of-file` (commonly abbreviated `EOF`) is a condition in a computer operating system _where no more data can be read from a data source_. The data source is usually called a file or stream.



EOF在Unix系统上对应的是`Control-D`，在Windows上是`Control-Z`。


例如下面输入2个数字的C++程序`test.cpp`:

```Cpp
#include <iostream>

int main()
{
        int x, y;
        while ( std::cin >> x >> y )
        std::cout << '/' << x << '/' << y << "/\n";
        if ( std::cin.eof() )
                std::cout << "End of input\n";
        else
                std::cout << "There was an error\n";
}
```

在输入两个字符`5 6`之后，打印出`/5/6/`，然后在键入`ctrl-D`即`EOF`，程序输出"End of input"，否则输出"There was an error"。

```bash
$./test
5 6
/5/6/
End of input
$./test
5 6
/5/6/
a
There was an error
```

