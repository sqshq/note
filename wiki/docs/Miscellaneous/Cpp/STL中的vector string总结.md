---
title: STL中的vector string总结
toc: false
date: 2017-08-17
tags: [Cpp]
---


vector<string>在C++编程中经常会被使用。


##初始化

```cpp
#include <string>
#include <vector>

using namespace std;


int main(){
    // push_back的方式
    vector<string> str1(4);
    str1.push_back("a");
    str1.push_back("b");
    str1.push_back("c");
    str1.push_back("d");

    // 类似于数组的方式
    vector <string> str2(4);
    str2[1] = "a";
    str2[2] = "b";
    str2[3] = "c";
    str2[4] = "d";

    //使用构造函数的方式
    string str3[] = {"a", "b", "c", "d"};
    vector<string> v(str3, str3+4);
}
```





