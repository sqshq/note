---
title: Tomcat
---

[Tomcat](http://tomcat.apache.org)是由Apache开发的一个Servlet容器，实现了对Servlet和JSP的支持，也包含了一个简单的服务器。



Tomcat固定的目录结构

* `/work`: Tomcat把由JSP生成的Servlet放于此目录下
* `/webapps`: 当发布Web应用时，默认情况下把Web应用文件防御此目录下
* `/logs`:存放Tomcat的日志文件
* `/share/lib`: 存放所有Web应用都可以访问的Jar文件
* `/common/lib`: 存放Tomcat服务器以及所有Web应用都可以访问的Jar应用
* `/server/webapps`: 存放Tomcat自带的两个Web应用：admin应用和manager应用
* `/server/lib`: 存放Tomcat服务器所需的Jar文件
* `/conf`: 存放各种配置文件
* `/bin`: 存放脚本文件