---
title: Python引号
toc: false
date: 2017-10-30
tags: [Python]
---


https://blog.csdn.net/woainishifu/article/details/76105667


Python中单引号，双引号，3个单引号及3个双引号的区别
2017年07月26日 10:21:23 邓无邪 阅读数：37124更多
个人分类： Python
版权声明：本文为博主原创文章，未经博主允许不得转载。	https://blog.csdn.net/woainishifu/article/details/76105667
单引号和双引号
在Python中我们都知道单引号和双引号都可以用来表示一个字符串，比如


str1 = 'python'
str2 = "python" 
str1和str2是没有任何区别的。


我们知道Python以其易用性而著名，所以刚开始看教程学习看到单引号和双引号都可以使用会以为这是Python为了方便程序员，随便用哪个就好，不用担心用错。其实，背后的原因不只是这么简单。举个例子，想想I'm a big fans of Python.这个字符串应该怎么定义。



单引号版本：


str3 = 'I\'m a big fan of Python.'
可以注意到，原来的字符串中有一个'，而Python又允许使用单引号' '来表示字符串，所以字符串中间的'必须用转移字符\才可以。字符串中间只有一个'，这样写看起来还好，但是如果是We all know that 'A' and 'B' are two capital letters.这个字符串呢？
str4 = 'We all know that \'A\' and \'B\' are two capital letters.'
怎么样，是不是看起来就很不好看，而且很容易出错了？这个时候就是双引号也可以表示字符串该体现作用的时候了。下面是str4的双引号版本：


str4_ = "We all know that 'A' and 'B' are two capital letters."
这样是不是看起来就人性化多了？没错，这就是Python支持双引号和单引号都能用来定义字符串的原因。


反之，如果字符串中有双引号，为了避免使用转义符，你可以使用单引号来定义这个字符串。比如：


str5 = 'The teacher said: "Practice makes perfect" is a very famous proverb.'
这就是Python易用性和人性化的一个极致体现，当你用单引号' '定义字符串的时候，它就会认为你字符串里面的双引号" "是普通字符，从而不需要转义。反之当你用双引号定义字符串的时候，就会认为你字符串里面的单引号是普通字符无需转义。



3个单引号及3个双引号
实际上3个单引号和3个双引号不经常用，但是在某些特殊格式的字符串下却有大用处。通常情况下我们用单引号或者双引号定义一个字符串的时候只能把字符串连在一起写成一行，如果非要写成多行，就得在每一行后面加一个\表示连字符，比如：


str1 = "List of name:\
        Hua Li\
        Chao Deng"
而且即使你这样写也不能得到期望的输出：

List of name:
Hua Li
Chao Deng
实际上输出是下面这样的：


>>> str1 = "List of name:\
...         Hua Li\
...         Chao Deng"
>>> print(str1)
List of name:        Hua Li        Chao Deng

那么该如何得到我们期望的一行一个名字的输出格式呢？这就是3个引号的作用了：

>>> str1 = """List of name:
... Hua Li
... Chao Deng
... """
>>> print(str1)
List of name:
Hua Li
Chao Deng


虽然我们也可以通过给字符串加上\n实现：

>>> str1 = "List of name:\nHua Li\nChao Deng"
>>> print(str1)
List of name:
Hua Li
Chao Deng
但是这样在输入的时候看起来就乱了很多不是么？所以这种情况下尽量使用3个引号，至于3个单引号还是双引号都是一样的，只需要注意如果字符串中包含有单引号就要使用双引号来定义就好了。


而且使用3个引号还有一个特别棒的作用就是：加注释！


>>> str1 = """
... List of name:
... Hua Li # LiHua
... Chao Deng # DengChao
... """
>>> print(str1)
 
List of name:
Hua Li # LiHua
Chao Deng # DengChao
如果要实现这种输出效果，仅仅使用单引号或者双引号还能实现吗？