---
title: Youtube
date: 2017-12-30
tags: [Youtube]
---


`Youtube-dl`可以下载Youtube网页的视频，功能很强大。但`Youtube-dl`还有个缺点，就是下载时单线程。简直就是龟速，下载视频往往还比较大，单线程是不可能使用的。

```bash
youtube-dl    https://www.youtube.com/playlist\?list\=PLrmLmBdmIlpslxZUHHWmfOzNn6cA7jvyh   --external-downloader aria2c --external-downloader-args "-x 16  -k 1M"
```


