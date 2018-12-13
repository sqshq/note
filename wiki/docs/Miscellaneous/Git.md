---
title: Git
toc: true
date: 2018-01-01
tags: [Git]
---




#### 合并仓库

可以把两个仓库A、B进行合并，并且保存所有的提交历史：

```bash
# 进入A仓库
cd dir-A  
# 添加B仓库
git remote add -f Bproject <url-of-B>  
# 合并B仓库到A仓库，保留历史
git merge -s ours --allow-unrelated-histories --no-commit Bproject/master  
# 读取B仓库信息到dir-B
git read-tree --prefix=dir-B/ -u Bproject/master 
# 提交
git commit -m "Merge B project as our subdirectory" 
# 抽取B仓库作为子项目，使用subtree strategy
git pull -s subtree Bproject master  
```


### 撤销

#### 撤销添加的文件

如果使用`git add <file>`添加了错误的文件, 可以使用`git reset HEAD`命令撤销添加的文件：

```bash
git reset HEAD #如果后面什么都不跟的话，就是上一次add里面的全部撤销
git reset HEAD XXX/XXX/XXX.java #对某个文件进行撤销
```

#### 撤销已经push的commit

使用`git reset`命令可以撤销已经push的commit。

```bash
git reset --soft/hard <commit-id>  # 撤销提交信息
git push origin master –force  ## 强制提交当前版本号，以达到撤销版本号的目的
# 重新提交和推送
git add .
git commit -m  <commit-message>
```

注意mixed/soft/hard区别：

* --mixed  会保留源码,只是将git commit和index信息回退到了某个版本.
* --soft   保留源码,只回退到commit信息到某个版本.不涉及index的回退,如果还需要提交,直接commit即可.
* --hard   源码也会回退到某个版本,commit和index 都会回退到某个版本.(注意,这种方式是改变本地代码仓库源码)


也可以使用`git revert`命令，但是它是把这次撤销作为一次最新的提交。


### ISSUE

#### CRLF will be replaced by LF 

CRLF : windows 环境下的换行符 
LF ： linux 环境下的换行符

关闭自动转换即可

```
git config core.autocrlf false  //将设置中自动转换功能关闭
```


#### refuse to merge

在`git pull`时出现的问题`fatal: refusing to merge unrelated histories`。

处理方案，添加`--allow-unrelated-histories`.


#### 参考资料

[Pro Git](https://git-scm.com/about)