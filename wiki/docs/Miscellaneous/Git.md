---
title: Git
toc: true
date: 2018-01-01
tags: [Git]
---

在`git pull`时出现的问题`fatal: refusing to merge unrelated histories`。

处理方案，添加`--allow-unrelated-histories`.

## repositories 合并

You can merge repository A into a subdirectory of a project B using the subtree merge strategy. 

```bash
git remote add -f Bproject /path/to/B
git merge -s ours --allow-unrelated-histories --no-commit Bproject/master
git read-tree --prefix=dir-B/ -u Bproject/master
git commit -m "Merge B project as our subdirectory"
git pull -s subtree Bproject master
```

