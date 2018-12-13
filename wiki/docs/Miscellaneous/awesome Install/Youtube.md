---
title: Youtube
date: 2017-12-30
tags: [Youtube]
---


#### 加快下载速度

`Youtube-dl`可以下载Youtube网页的视频，功能很强大。但`Youtube-dl`还有个缺点，就是下载时单线程。简直就是龟速，下载视频往往还比较大，单线程是不可能使用的。

```bash
youtube-dl    https://www.youtube.com/playlist\?list\=kooim   
        --external-downloader aria2c
        --external-downloader-args "-x 16  -k 1M"
```

#### 选择清晰度

使用-F选项：

```Bash
youtube-dl -F url
```

然后选择相应的format code，在下载时加上`-f format-code`（注意，此时f是小写的）。
