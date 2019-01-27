<div id="kp_box_476" data-pid="476"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_476-794&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_476-794&quot;,&quot;con&quot;:&quot;,,&quot;}">

</div>

<div style="display:none;">

![]()

</div>

<div id="mainBox" class="container clearfix">

<div class="recommend-right">

</div>

<div class="blog-content-box">

<div class="article-header-box">

<div class="article-header">

<div class="article-title-box">

[原]{.article-type .type-1 .float-left}
Redis 入门 慕课网,笔记 {#redis-入门-慕课网笔记 .title-article}
======================

</div>

<div class="article-info-box">

<div class="article-bar-top">

[2017年06月21日 12:10:31]{.time}
[我爱圆溜溜](https://me.csdn.net/fulq1234){.follow-nickName}
[阅读数：665]{.read-count}

</div>

<div class="operating">

</div>

</div>

</div>

</div>

<div id="article_content"
class="article_content clearfix csdn-tracking-statistics"
data-pid="blog" data-mod="popu_307" data-dsm="post">

<div id="content_views" class="htmledit_views">

01-NoSQL的概述
--------------

NoSQL = Not Only SQL\
非关系型数据库\
\
\
为什么需要NoSQL,\
高并发读写\
海量数据的高效率存储和访问\
高可扩展性和高可用性\
\
\
NoSQL数据库的四大分类\
\
\
键值(Key-Value)存储\
\
\
02-NoSQL的概述
--------------

\
\
应用场景\
缓存\
任务队列\
网址访问统计\
数据过期处理\
应用排行榜\
分布式集群结构中的session分离\
\
\
03-Redis的安装
--------------

搭建环境\
虚拟机：VMware 10.0.02\
linux系统:centOS-6.5\
SSH客户端:SecureCRT 7.3 SecureFx7.3\

\

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
安装过程：
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
 
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
 用su命令改变用户
```

（1）安装编译器：yum install gcc-c++ （2）进入root目录,
[wget ]{style="font-family:Verdana, Arial, Helvetica, sans-serif;font-size:14px;"}[http://download.redis.io/releases/redis-3.0.7.tar.gz](http://download.redis.io/releases/redis-3.2.3.tar.gz)
``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
  （3）解压Redis压缩包：tar -zxvf redis-3.0.7.tar.gz
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
  （4）进入Redis目录进行编译：make
  （5）安装Redis,指定安装目录为/usr/local/redis：make PREFIX=/usr/local/redis install
  （6）将redis.conf拷贝到Redis安装目录：cp redis.conf /usr/local/redis
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
  （7）进入安装目录，更改redis.conf文件：vim redis.conf --> daemonize no 改为 yes
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
  （8）启动redis前端模式,该模式命令窗口始终被占用: ./redis-server
  （9）启动redis后端模式：./bin/redis-server redis.conf
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
  （10）查看redis是否启动: ps -ef|grep -i redis 
```

``` {style="font-size:14px;line-height:28px;color:rgb(20,25,30);"}
```

``` {style="color:rgb(20,25,30);font-size:14px;line-height:28px;"}
  （11）关闭redis 。方法一,kill -9 方法二: ./bin/redis-cli shutdown
```

``` {style="color:rgb(20,25,30);font-size:14px;line-height:28px;"}
```

![](https://img-blog.csdn.net/20170621154145132?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
\

5-1 Jedis入门
-------------

java调用redis服务，推荐使用Jedis

pom.xml

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency> 
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
            <version>2.3</version>
        </dependency> 
        <dependency>
            <groupId>redis.clients</groupId>
            <artifactId>jedis</artifactId>
            <version>2.7.0</version>
        </dependency>
      </dependencies>

\

测试方法\
    package com.immoc.jedis;

    import org.junit.Test;

    import redis.clients.jedis.Jedis;
    import redis.clients.jedis.JedisPool;
    import redis.clients.jedis.JedisPoolConfig;

    public class JedisDemo1 {
        
        @Test
        public void demo1(){
            //1.设置IP地址和端口
            Jedis jedis = new Jedis("192.168.136.130",6379);
            //2.保存数据
            jedis.set("age", "100");
            //3.获取数据
            String age = jedis.get("age");
            System.out.println(age);
            //4.释放资源
            jedis.close();
        }
        
        
        @Test
        /**
         * 使用连接池
         */
        public void demo2(){
            //获取连接池的配置对象
            JedisPoolConfig config = new JedisPoolConfig();
            //设置最大连接数
            config.setMaxTotal(30);
            //设置最大空闲连接数
            config.setMaxIdle(10);
            //获得连接池
            JedisPool jedisPool = new JedisPool(config,"192.168.136.130",6379);
            //获取核心对象
            Jedis jedis = null;
            try{
                //通过连接池或得连接
                jedis = jedisPool.getResource();
                //设置数据
                jedis.set("name", "张三");
                //获取数据
                String name = jedis.get("name");
                System.out.println(name);
            }catch(Exception e){
                e.printStackTrace();
            }finally{
                //释放资源
                if(jedis != null){
                    jedis.close();
                }
                if(jedisPool != null){
                    jedisPool.close();
                }
            }
        }
    }

\
\
服务器，需要保证6379端口，开启

开启的方法

vim /etc/sysconfig/iptables\
![](https://img-blog.csdn.net/20170621163222645?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
\
启动防火墙:service iptables restart\

查看开放的端口:netstat -tln

\

\

6-1 redis数据结果之字符串
-------------------------

![](https://img-blog.csdn.net/20170621174949727?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\

\

 6-2.数据结构之哈希

命令:myhash username jack\
解释:定义Hash变量，key是username;value是jack\
\
命令:hmset myhash2 username rose age 21\
解释:定义多个Hash变量\
\
命令:hget myhash username\
解释:得到Hash变量，key是username的值\
\
命令:hmget myhash username age\
解释:得到Hash变量，可以指定多个key值\
\
命令:hgetall myhash\
解释:得到myhash的所有key和value值\
\
命令:hdel myhash2 username age\
解释:删除myhash2的多个key\
\
命令:del myhash2\
解释:直接删除变量myhash2\
\
命令:hincrby myhash age 5\
解释:变量age值增加5\
\
命令:hexists myhash username\
解释:判断myhash是否存在key值username。如果存在，就返回1；如果不存在，就返回0;

\
![](https://img-blog.csdn.net/20170705103237842?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
\
\

  6-3.数据结构之list\
存储list\
ArrayList使用数组方式\
LinkedList使用双向链表\
双向链表中添加数据\
双向链表中删除数据\
\
\
lpush 从左侧添加数据到链表\
rpush 从右侧添加数据到链表\
lpop 左侧弹出,弹出后，链表中就不存在了\
rpop 右侧弹出\
llen 查看链表长度,如果参数不存在，返回0\
lpushx 左侧插入\
lrom 删除列表\
lset list 3 mm :往链表list里面第3个位置里插入mm\
linsert list4 before b ll :往链表list4里面元素b的前面插入ll\
linsert list4 after b 22:在b后面插入\
rpoplpush list5 list6 :把list右边元素弹出，插入到list6的左侧

![](https://img-blog.csdn.net/20170705115542905?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
\
  6-4.数据结构之set\
存储Set\
和List类型不同的是,Set集合中不允许出现重复的元素\
存储set常用命令\
sadd:添加\
srem:删除\
smembers:查看参数\
sismember:判断是否存在指定元素\
sdiff:差集运算\
sinter:交集运算\
sunion:并集运算\
sdiffstore my1 mya1 myb1:把集合mya1和myb1的差集交给变量my1\
sinterstore\
sunionstore\
\
![](https://img-blog.csdn.net/20170705165508314?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
  6-5.数据结构之sorted-set\
Sorted-Set中的成员在集合中的位置是有序的\
\
\
zadd 添加\
zscore 查看值\
zcard 查看长度\
zrem 删除\
zrange mysort 0 -1
withscores:根据范围查找，0:最开始;-1:最后一个.widthscores是带着数组显示\
zrevrange mysort 0 -1 widthscores:排序\
zremrangebyrank:根据范围删除\
zremrangebyscore:根据score的范围删除

![](https://img-blog.csdn.net/20170705172032267?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
\
  7-1.keys的通用操作\
\
\
\
keys \*:或得所有keys:\
del:删除\
exists:是否存在，存在返回1，不存在返回0\
rename:重命名\
expire:设置过期时间\
ttl:查看剩下时间\
type:查看类型

![](https://img-blog.csdn.net/20170706170926625?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\

\
  8-1.redis的特性\
\
\
\
多数据库\
\
\
默认选择0号数据库。一共有0到15个数据库\
select:选择数据库\
move:移动到哪个数据库\
multi exec discard:实现事务\
multi:开启事务\
exec:提交\
discard:回滚

![](https://img-blog.csdn.net/20170706172115726?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZnVscTEyMzQ=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)\
\
  9-1.redis的持久化的概述\
\
RDB持久化\
默认,在指定的时间间隔里面，把数据写入\
AOF持久化\
\
\
无持久化\
\
\
同时使用RDB和AOF\
\
\
  9-2. 持久化的RDB的方式\
\
\
  9-3.持久化的AOF的方式\
  \

\

spring应用场景

spring-redis.xml

\

    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="
            http://www.springframework.org/schema/task http://www.springframework.org/schema/task/spring-task.xsd
            http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd"
        default-autowire="byName" default-lazy-init="false">
        
        <bean id="jedisPoolConfig" class="redis.clients.jedis.JedisPoolConfig">
            <property name="maxTotal" value="50" />
            <property name="maxIdle" value="10" />
            <property name="maxWaitMillis" value="1000" />
            <property name="testOnBorrow" value="true" />
        </bean>
        <bean id="jedisPool" class="redis.clients.jedis.JedisPool">
            <constructor-arg index="0" ref="jedisPoolConfig"/>
            <constructor-arg index="1" value="${redis.host}"/>
            <constructor-arg index="2" value="${redis.port}"/>
            <constructor-arg index="3" value="1000"/>
            <constructor-arg index="4" value="${redis.pwd}"/>
        </bean>
    </beans>

\

RedisService.java

    package com.wjtc.wechat.store.service.impl;

    import org.apache.commons.lang3.StringUtils;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.stereotype.Component;

    import com.wjtc.core.util.HttpClientUtil;
    import com.wjtc.wechat.common.bean.other.WxAuthorizer;

    import redis.clients.jedis.Jedis;
    import redis.clients.jedis.JedisPool;

    @Component
    public class RedisService {
        @Autowired
        private JedisPool jedisPool;
        
        @Value("${wechat_token_url}")
        private String wechat_token_url;
        /**
         * 根据公众号的appid获取公众号的令牌
         * @param appid 公众号的appid
         * @return
         */
        public String get(WxAuthorizer author) {
            String token = null;
            Jedis jedis = null;
            try {
                jedis = jedisPool.getResource();
                token = jedis.get(author.getAppid());
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                if (jedis != null) {
                    jedis.close();
                }
            }
            if (StringUtils.isBlank(token)) {
                token = HttpClientUtil.doGet(wechat_token_url + "?authorizer_appid=" + author.getAppid() + "&authorizer_refresh_token=" + author.getRefresh_token());
                System.out.println("token=" + token);
                if (StringUtils.isBlank(token) || "error".equals(token)) {
                    token = null;
                    return token;
                }
            }
            token = token.replace("\"", "");
            return token;
            
        }
        
        
    }

\
\
\
\
\

\

</div>

</div>

</div>

<div class="hide-article-box hide-article-pos text-center">

<div class="border">

</div>

[阅读更多]{#btn-readmore .btn .article-footer-btn}
[收藏]{}
<div class="btn article-footer-btn bds_weixin article-footer-share-btn"
data-cmd="weixin" title="分享">

[分享]{}
<div class="bdsharebuttonbox">

[](# "分享"){.bds_weixin .clear-share-style-article-footer}

</div>

</div>

</div>

<div id="dmp_ad_58">

<div id="kp_box_58" data-pid="58"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_58-402&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_58-402&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div style="width:100%;background:#fff;border:3px solid #fff;">

<div id="three_ad1" class="mediav_ad">

</div>

</div>

</div>

</div>

[]{#commentBox}
<div class="comment-box">

<div class="comment-edit-box d-flex">

[]{#commentsedit}
<div class="user-img">

[![](//g.csdnimg.cn/static/user-img/anonymous-User-img.png){.show_loginbox}](javascript:void(0);)

</div>

<div class="opt-box">

<div id="ubbtools" class="add_code">

[**](#insertcode)

</div>

<div class="csdn-tracking-statistics tracking-click"
style="display: none;" data-mod="popu_384">

[发表评论](#){.comment_area_btn}

</div>

<div id="myDrap" class="dropdown">

[]{.dropdown-face .d-flex .align-items-center}
<div class="txt-selected text-truncate">

添加代码片

</div>

-   [HTML/XML]{}
-   [objective-c]{}
-   [Ruby]{}
-   [PHP]{}
-   [C]{}
-   [C++]{}
-   [JavaScript]{}
-   [Python]{}
-   [Java]{}
-   [CSS]{}
-   [SQL]{}
-   [其它]{}

</div>

<div class="right-box">

[还能输入*1000*个字符]{#tip_comment .tip}

</div>

</div>

</div>

<div class="comment-list-container">

[]{#comments}
<div class="comment-list-box">

</div>

<div id="commentPage" class="pagination-box d-none">

</div>

<div class="opt-box text-center">

</div>

</div>

</div>

<div class="recommend-box">

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/rocksteadypro/article/details/79162667,BlogCommendFromBaidu_0&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/rocksteadypro/article/details/79162667,BlogCommendFromBaidu_0&quot;}">

<div class="content">

[](https://blog.csdn.net/rocksteadypro/article/details/79162667 "linux+redis实战教程")
#### linux+*redis*实战教程 {#linuxredis实战教程 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[01-25]{.date .hover-show} [ 452]{.read-num .hover-hide}

</div>

[[0pnf There is a surprise Linux+Redis实战教程 Linux介绍与安装
linux\_开发软件安装=命令步骤 常用命令【重点】 ...]{.desc
.oneline}](https://blog.csdn.net/rocksteadypro/article/details/79162667 "linux+redis实战教程")
[[来自： [
ROCK]{.blog_title}](https://blog.csdn.net/rocksteadypro)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/xyt1033/10115951,BlogCommendFromBaidu_1&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/xyt1033/10115951,BlogCommendFromBaidu_1&quot;}">

[](https://download.csdn.net/download/xyt1033/10115951)
<div class="content">

<div>

[下载]{.type}
#### linux+*redis*实战资料 {#linuxredis实战资料 .text-truncate .oneline .clearfix}

[11-13]{.data .float-right}

</div>

<div class="desc oneline">

内含 redis-3.0.0.tar.gz ,
有三个txt文件，记录了linux下jdk、mysql、tomcat、redis详细安装教程

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/xiaoye142034/article/details/79122562,BlogCommendFromBaidu_2&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/xiaoye142034/article/details/79122562,BlogCommendFromBaidu_2&quot;}">

<div class="content">

[](https://blog.csdn.net/xiaoye142034/article/details/79122562 "Linux+Redis实战教程_day01_Redis入门_安装与使用")
#### Linux+*Redis*实战教程\_day01\_*Redis入门*\_安装与使用 {#linuxredis实战教程_day01_redis入门_安装与使用 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[01-21]{.date .hover-show} [ 235]{.read-num .hover-hide}

</div>

[[]{.desc
.oneline}](https://blog.csdn.net/xiaoye142034/article/details/79122562 "Linux+Redis实战教程_day01_Redis入门_安装与使用")
[[来自： [
:)一位靓仔偶然路过的博客]{.blog_title}](https://blog.csdn.net/xiaoye142034)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_59" data-pid="59"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_59-517&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_59-517&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad1" class="mediav_ad">

</div>

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/goatgoat215103/10133489,BlogCommendFromBaidu_3&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/goatgoat215103/10133489,BlogCommendFromBaidu_3&quot;}">

[](https://download.csdn.net/download/goatgoat215103/10133489)
<div class="content">

<div>

[下载]{.type}
#### *Redis*培训（内部使用.ppt ） {#redis培训内部使用.ppt .text-truncate .oneline .clearfix}

[11-26]{.data .float-right}

</div>

<div class="desc oneline">

Redis培训，内部员工培训用，Redis基础，对于想学Redis的可以下载学习。

</div>

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/g290095142/10149848,BlogCommendFromBaidu_4&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/g290095142/10149848,BlogCommendFromBaidu_4&quot;}">

[](https://download.csdn.net/download/g290095142/10149848)
<div class="content">

<div>

[下载]{.type}
#### *Redis入门*\_超详细版.PDF {#redis入门_超详细版.pdf .text-truncate .oneline .clearfix}

[12-07]{.data .float-right}

</div>

<div class="desc oneline">

Redis入门\_超详细版.PDF
个人收集电子书，仅用学习使用，不可用于商业用途，如有版权问题，请联系删除！

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/smartbetter/article/details/53117527,BlogCommendFromGuangxin_5&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/smartbetter/article/details/53117527,BlogCommendFromGuangxin_5&quot;}">

<div class="content">

[](https://blog.csdn.net/smartbetter/article/details/53117527 "Linux 下 Redis 分布式集群安装使用")
#### Linux 下 *Redis* 分布式集群安装使用 {#linux-下-redis-分布式集群安装使用 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[11-14]{.date .hover-show} [ 1.1万]{.read-num .hover-hide}

</div>

[[Linux 下 Redis 分布式集群安装使用。这里 Linux 选择 CentOS 7.2。Redis
主从复制的功能非常强大，它可以避免 Redis
单点故障；构建读写分离架构，满足读多写少的应用...]{.desc
.oneline}](https://blog.csdn.net/smartbetter/article/details/53117527 "Linux 下 Redis 分布式集群安装使用")
[[来自： [
郭朝的博客]{.blog_title}](https://blog.csdn.net/smartbetter)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u011486068/article/details/52798008,BlogCommendFromGuangxin_6&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u011486068/article/details/52798008,BlogCommendFromGuangxin_6&quot;}">

<div class="content">

[](https://blog.csdn.net/u011486068/article/details/52798008 "redis 模糊删除key")
#### *redis* 模糊删除key {#redis-模糊删除key .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[10-12]{.date .hover-show} [ 2.1万]{.read-num .hover-hide}

</div>

[[redis 模糊删除key由于在我们的项目中使用Spring
Cached和Redis结合的方式对一部分数据做数据库缓存，当缓存和数据库数据不一致时（由于手动改数据库引起），就得清空数据库的缓存，这就...]{.desc
.oneline}](https://blog.csdn.net/u011486068/article/details/52798008 "redis 模糊删除key")
[[来自： [
暗里着迷的博客]{.blog_title}](https://blog.csdn.net/u011486068)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/hhfff123/article/details/51277081,BlogCommendFromGuangxin_7&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/hhfff123/article/details/51277081,BlogCommendFromGuangxin_7&quot;}">

<div class="content">

[](https://blog.csdn.net/hhfff123/article/details/51277081 "hadoop正式学习之redis------redis的学习和操作1")
#### hadoop正式学习之*redis*------*redis*的学习和操作1 {#hadoop正式学习之redis------redis的学习和操作1 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[04-28]{.date .hover-show} [ 1449]{.read-num .hover-hide}

</div>

[[1：redis简介  
Redis是一种面向“键/值”对数据类型的内存数据库，可以满足我们对海量数据的读写需求
    redis的键只能是string类型     redis的值支持多种数据类...]{.desc
.oneline}](https://blog.csdn.net/hhfff123/article/details/51277081 "hadoop正式学习之redis------redis的学习和操作1")
[[来自： [
hhfff123的博客]{.blog_title}](https://blog.csdn.net/hhfff123)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_60" data-pid="60"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_60-43&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_60-43&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad8" class="mediav_ad">

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/nrs12345/article/details/17996981,BlogCommendFromGuangxin_8&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/nrs12345/article/details/17996981,BlogCommendFromGuangxin_8&quot;}">

<div class="content">

[](https://blog.csdn.net/nrs12345/article/details/17996981 "redis批量删除key")
#### *redis*批量删除key {#redis批量删除key .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[01-08]{.date .hover-show} [ 1.7万]{.read-num .hover-hide}

</div>

[[用linux的xargs命令，把前一个命令的结果当作后一个命令的参数，比如要删除redis中所有doctor\_开头的key，我们可以这么写
redis-cli KEYS "doctor\_\*"...]{.desc
.oneline}](https://blog.csdn.net/nrs12345/article/details/17996981 "redis批量删除key")
[[来自： [
nrs12345的专栏]{.blog_title}](https://blog.csdn.net/nrs12345)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box type_hot_word">

<div class="content clearfix oneline">

##### 文章热词 {#文章热词 .float-left}

<div class="word float-left">

[ [Electron入门](https://edu.csdn.net/courses/o364_s7104_k%20)]{} [
[入门讲解](https://edu.csdn.net/course/play/7221/145886%20)]{} [
[UG教程入门](https://edu.csdn.net/courses/o363_s7131_k%20)]{} [
[3Dmax入门学习](https://edu.csdn.net/courses/o363_s7121_k%20)]{} [
[Python网络爬虫技术入门](https://edu.csdn.net/course/play/8216/168583%20)]{}

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/gdlingshao/article/details/76836854,BlogCommendFromGuangxin_9&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/gdlingshao/article/details/76836854,BlogCommendFromGuangxin_9&quot;}">

<div class="content">

[](https://blog.csdn.net/gdlingshao/article/details/76836854 "redis key 模糊查询")
#### *redis* key 模糊查询 {#redis-key-模糊查询 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[08-07]{.date .hover-show} [ 1.2万]{.read-num .hover-hide}

</div>

[[一开始使用 keys（）
这种形式，大发现网上大量文章表示，这种形式会非常耗费内存。
于是改一下方式，使用hash， (key hkey
hvalue),把要模糊查询的值放到hkey上面。然后使用s...]{.desc
.oneline}](https://blog.csdn.net/gdlingshao/article/details/76836854 "redis key 模糊查询")
[[来自： [
zling工作室]{.blog_title}](https://blog.csdn.net/gdlingshao)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box blog-expert-recommend-box">

<div class="d-flex">

<div class="blog-expert-recommend">

<div class="blog-expert">

<div class="blog-expert-flexbox">

</div>

</div>

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u012957549/article/details/78495526,BlogCommendFromQuerySearch_10&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u012957549/article/details/78495526,BlogCommendFromQuerySearch_10&quot;}">

<div class="content">

[](https://blog.csdn.net/u012957549/article/details/78495526 "nginx 从入门到实践 -基础篇（2）")
#### nginx 从*入门*到实践 -基础篇（2） {#nginx-从入门到实践--基础篇2 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[11-10]{.date .hover-show} [ 1378]{.read-num .hover-hide}

</div>

[[上篇说到了linux的安装 目录基本讲解 以及启动访问。
下面继续探索。]{.desc
.oneline}](https://blog.csdn.net/u012957549/article/details/78495526 "nginx 从入门到实践 -基础篇（2）")
[[来自： [
u012957549的博客]{.blog_title}](https://blog.csdn.net/u012957549)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_33400820/article/details/79214519,BlogCommendFromQuerySearch_11&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_33400820/article/details/79214519,BlogCommendFromQuerySearch_11&quot;}">

<div class="content">

[](https://blog.csdn.net/weixin_33400820/article/details/79214519 "慕课网_《Redis入门》学习总结")
#### *慕课网*\_《*Redis入门*》学习总结 {#慕课网_redis入门学习总结 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[01-31]{.date .hover-show} [ 153]{.read-num .hover-hide}

</div>

[[https://segmentfault.com/a/1190000009530905 时间：2017年05月21日星期日
说明：本文部分内容均来自慕课网。@慕课网：http://www.imoo...]{.desc
.oneline}](https://blog.csdn.net/weixin_33400820/article/details/79214519 "慕课网_《Redis入门》学习总结")
[[来自： [
weixin\_33400820的博客]{.blog_title}](https://blog.csdn.net/weixin_33400820)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/walykyy/article/details/83094622,BlogCommendFromQuerySearch_12&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/walykyy/article/details/83094622,BlogCommendFromQuerySearch_12&quot;}">

<div class="content">

[](https://blog.csdn.net/walykyy/article/details/83094622 "HIVE 走近大数据之Hive进阶---慕课网---总结笔记--后续持续更新")
#### HIVE 走近大数据之Hive进阶---*慕课网*---总结*笔记*--后续持续更新 {#hive-走近大数据之hive进阶---慕课网---总结笔记--后续持续更新 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[10-16]{.date .hover-show} [ 47]{.read-num .hover-hide}

</div>

[[HIVE进阶学习笔记 1、load加载数据   
 1、语法：local本地路径，没有则是默认读取HDFS文件路径，partition数据存储到分区表内
        load data \[loca...]{.desc
.oneline}](https://blog.csdn.net/walykyy/article/details/83094622 "HIVE 走近大数据之Hive进阶---慕课网---总结笔记--后续持续更新")
[[来自： [
walykyy的博客]{.blog_title}](https://blog.csdn.net/walykyy)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_61" data-pid="61"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_61-557&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_61-557&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad13" class="mediav_ad">

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/yanlovehan/article/details/81534750,BlogCommendFromQuerySearch_13&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/yanlovehan/article/details/81534750,BlogCommendFromQuerySearch_13&quot;}">

<div class="content">

[](https://blog.csdn.net/yanlovehan/article/details/81534750 "慕课网~redis入门~笔记~（二）安装")
#### *慕课网*\~*redis入门*\~*笔记*\~（二）安装 {#慕课网redis入门笔记二安装 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[08-09]{.date .hover-show} [ 55]{.read-num .hover-hide}

</div>

[[ https://www.imooc.com/learn/839 Redis的安装 搭建环境 虚拟机：Vmware
Linux系统：Centos 7 SSH工具：FinalShell ...]{.desc
.oneline}](https://blog.csdn.net/yanlovehan/article/details/81534750 "慕课网~redis入门~笔记~（二）安装")
[[来自： [
刘岩的专栏]{.blog_title}](https://blog.csdn.net/yanlovehan)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/yanlovehan/article/details/81532462,BlogCommendFromQuerySearch_14&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/yanlovehan/article/details/81532462,BlogCommendFromQuerySearch_14&quot;}">

<div class="content">

[](https://blog.csdn.net/yanlovehan/article/details/81532462 "慕课网~redis入门~笔记~（一）概述")
#### *慕课网*\~*redis入门*\~*笔记*\~（一）概述 {#慕课网redis入门笔记一概述 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[08-09]{.date .hover-show} [ 61]{.read-num .hover-hide}

</div>

[[ https://www.imooc.com/learn/839 课程介绍 NoSql的概述 Redis的概述
...]{.desc
.oneline}](https://blog.csdn.net/yanlovehan/article/details/81532462 "慕课网~redis入门~笔记~（一）概述")
[[来自： [
刘岩的专栏]{.blog_title}](https://blog.csdn.net/yanlovehan)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/gsm123/article/details/52563424,BlogCommendFromBaidu_15&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/gsm123/article/details/52563424,BlogCommendFromBaidu_15&quot;}">

<div class="content">

[](https://blog.csdn.net/gsm123/article/details/52563424 "redis入门（一）")
#### *redis入门*（一） {#redis入门一 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-17]{.date .hover-show} [ 596]{.read-num .hover-hide}

</div>

[[简介Redis是一个开源的、高性能的、基于健值对的缓存与存储系统，通过提供多种健值数据类型来适应不同场景下的缓存与存储需求。Redis支持的键值数据类型
字符串类型 列表类型 散列类型 集合类型 有序...]{.desc
.oneline}](https://blog.csdn.net/gsm123/article/details/52563424 "redis入门（一）")
[[来自： [
持之以恒，大巧若拙]{.blog_title}](https://blog.csdn.net/gsm123)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/ldld1717/article/details/79355219,BlogCommendFromQuerySearch_16&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/ldld1717/article/details/79355219,BlogCommendFromQuerySearch_16&quot;}">

<div class="content">

[](https://blog.csdn.net/ldld1717/article/details/79355219 "十小时入门大数据学习笔记（二）")
#### 十小时*入门*大数据学习*笔记*（二） {#十小时入门大数据学习笔记二 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[02-23]{.date .hover-show} [ 936]{.read-num .hover-hide}

</div>

[[第二章 初识Hadoop2.1Hadoop概述名称由来：项目作者的孩子对黄色大象玩具的命名开源、分布式存储与分布式计算的平台 Hadoop能做什么：1. 搭建大型数据仓库，PB级数据的存储、处理、分析...]{.desc
.oneline}](https://blog.csdn.net/ldld1717/article/details/79355219 "十小时入门大数据学习笔记（二）")
[[来自： [
进击的小怪兽]{.blog_title}](https://blog.csdn.net/ldld1717)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u011010851/article/details/79472073,BlogCommendFromQuerySearch_17&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u011010851/article/details/79472073,BlogCommendFromQuerySearch_17&quot;}">

<div class="content">

[](https://blog.csdn.net/u011010851/article/details/79472073 "Linux基础命令及概念_【慕课网课笔记】")
#### Linux基础命令及概念\_【*慕课网*课*笔记*】 {#linux基础命令及概念_慕课网课笔记 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[03-09]{.date .hover-show} [ 116]{.read-num .hover-hide}

</div>

[[1.Linux严格区分大小写；2.Linux中所有内容以文件形式保存；3.Linux文件不区分扩展名；靠权限区分；4.文件类型-文件d目录l软链接文件（快捷方式） 块设备文件 字符设备文件 套接字文件...]{.desc
.oneline}](https://blog.csdn.net/u011010851/article/details/79472073 "Linux基础命令及概念_【慕课网课笔记】")
[[来自： [
Aye]{.blog_title}](https://blog.csdn.net/u011010851)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_62" data-pid="62"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_62-556&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_62-556&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad18" class="mediav_ad">

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u012957549/article/details/78484770,BlogCommendFromQuerySearch_18&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u012957549/article/details/78484770,BlogCommendFromQuerySearch_18&quot;}">

<div class="content">

[](https://blog.csdn.net/u012957549/article/details/78484770 "nginx 从入门到实践 -基础篇（1）")
#### nginx 从*入门*到实践 -基础篇（1） {#nginx-从入门到实践--基础篇1 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[11-08]{.date .hover-show} [ 2912]{.read-num .hover-hide}

</div>

[[文章地址:http://www.haha174.top/article/details/251862一. nginx
概述nginx是一个开源且高性能、可靠的HTTP中间件、代理服务
这里只是简单的...]{.desc
.oneline}](https://blog.csdn.net/u012957549/article/details/78484770 "nginx 从入门到实践 -基础篇（1）")
[[来自： [
u012957549的博客]{.blog_title}](https://blog.csdn.net/u012957549)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/u014270696/10775896,BlogCommendFromQuerySearch_19&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/u014270696/10775896,BlogCommendFromQuerySearch_19&quot;}">

[](https://download.csdn.net/download/u014270696/10775896)
<div class="content">

<div>

[下载]{.type}
#### 一站式学习*Redis* 从*入门*到高可用分布式实践 {#一站式学习redis-从入门到高可用分布式实践 .text-truncate .oneline .clearfix}

[11-09]{.data .float-right}

</div>

<div class="desc oneline">

一站式学习Redis 从入门到高可用分布式实践
一门内容非常丰富的Redis课程，基于原Redis课程进行升级。由阿里云Redis开发规范原作者为你深入讲解每个技术点。课程包含Redis基础，使用经验介绍、Java，Python客户端示范...

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/zoucanfa/article/details/78915460,BlogCommendFromQuerySearch_20&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/zoucanfa/article/details/78915460,BlogCommendFromQuerySearch_20&quot;}">

<div class="content">

[](https://blog.csdn.net/zoucanfa/article/details/78915460 "慕课学习史上最全零基础入门HTML5和CSS笔记")
#### 慕课学习史上最全零基础*入门*HTML5和CSS*笔记* {#慕课学习史上最全零基础入门html5和css笔记 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[12-27]{.date .hover-show} [ 1356]{.read-num .hover-hide}

</div>

[[慕课学习史上最全零基础入门HTML5和CSS笔记Html和CSS的关系
学习web前端开发基础技术需要掌握：HTML、CSS、JavaScript语言。下面我们就来了解下这三门技术都是用来实现什么...]{.desc
.oneline}](https://blog.csdn.net/zoucanfa/article/details/78915460 "慕课学习史上最全零基础入门HTML5和CSS笔记")
[[来自： [
zoucanfa的博客]{.blog_title}](https://blog.csdn.net/zoucanfa)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/eadghd/10444315,BlogCommendFromQuerySearch_21&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/eadghd/10444315,BlogCommendFromQuerySearch_21&quot;}">

[](https://download.csdn.net/download/eadghd/10444315)
<div class="content">

<div>

[下载]{.type}
#### *Redis*从*入门*到高可用，分布式实践 {#redis从入门到高可用分布式实践 .text-truncate .oneline .clearfix}

[05-29]{.data .float-right}

</div>

<div class="desc oneline">

第1章 Redis初识
带领听众进入Redis的世界，了解它的前世今生、众多特性、应用场景、安装配置、简单使用，可以让听众对Redis有一个全面的认识。
第2章 API的理解和使用 全面介绍了Redis提供的5种数据结构字符串（strin...

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/M7KiSE/article/details/80079452,BlogCommendFromQuerySearch_22&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/M7KiSE/article/details/80079452,BlogCommendFromQuerySearch_22&quot;}">

<div class="content">

[](https://blog.csdn.net/M7KiSE/article/details/80079452 "慕课网程序设计入门——C语言（ 翁恺老师）学习笔记1、tips")
#### *慕课网*程序设计*入门*——C语言（ 翁恺老师）学习*笔记*1、tips {#慕课网程序设计入门c语言-翁恺老师学习笔记1tips .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[04-27]{.date .hover-show} [ 337]{.read-num .hover-hide}

</div>

[[课程链接：http://www.icourse163.org/course/ZJU-1990011、scanf(&quot;  
     &quot;,)：引号里的内容是一定要输入的内容，空格 仅可...]{.desc
.oneline}](https://blog.csdn.net/M7KiSE/article/details/80079452 "慕课网程序设计入门——C语言（ 翁恺老师）学习笔记1、tips")
[[来自： [
M7KiSE的博客]{.blog_title}](https://blog.csdn.net/M7KiSE)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_63" data-pid="63"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_63-555&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_63-555&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad23" class="mediav_ad">

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/kingmore96/article/details/80203861,BlogCommendFromQuerySearch_23&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/kingmore96/article/details/80203861,BlogCommendFromQuerySearch_23&quot;}">

<div class="content">

[](https://blog.csdn.net/kingmore96/article/details/80203861 "IntelliJ IDEA 学习笔记--慕课网视频")
#### IntelliJ IDEA 学习*笔记*--*慕课网*视频 {#intellij-idea-学习笔记--慕课网视频 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[05-06]{.date .hover-show} [ 500]{.read-num .hover-hide}

</div>

[[无处不在的跳转 项目的跳转 ctrl+Alt+\[ 或 \] 文件的跳转 ctrl+e
最近的文件 ctrl+shift+e 最近编辑的文件 浏览修改位置的跳转
ctrl+shift+bac...]{.desc
.oneline}](https://blog.csdn.net/kingmore96/article/details/80203861 "IntelliJ IDEA 学习笔记--慕课网视频")
[[来自： [
GNin的博客]{.blog_title}](https://blog.csdn.net/kingmore96)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/it_you_know/10593128,BlogCommendFromQuerySearch_24&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/it_you_know/10593128,BlogCommendFromQuerySearch_24&quot;}">

[](https://download.csdn.net/download/it_you_know/10593128)
<div class="content">

<div>

[下载]{.type}
#### *redis*从*入门*到高可用，分布式实践 {#redis从入门到高可用分布式实践-1 .text-truncate .oneline .clearfix}

[08-09]{.data .float-right}

</div>

<div class="desc oneline">

redis从入门到高可用以及分布式实践，非常系统的介绍了redis，值的大家看看。

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_20367813/article/details/79139909,BlogCommendFromQuerySearch_25&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_20367813/article/details/79139909,BlogCommendFromQuerySearch_25&quot;}">

<div class="content">

[](https://blog.csdn.net/qq_20367813/article/details/79139909 "慕课网2小时学会Spring Boot第二讲笔记")
#### *慕课网*2小时学会Spring Boot第二讲*笔记* {#慕课网2小时学会spring-boot第二讲笔记 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[01-23]{.date .hover-show} [ 169]{.read-num .hover-hide}

</div>

[[A、Result对象固定返回格式 B、为了解决逻辑在一个地方处理，抛异常来处理
    默认的Exception只接受message数据     自定义的接受多个，如加code
C、捕获得到的...]{.desc
.oneline}](https://blog.csdn.net/qq_20367813/article/details/79139909 "慕课网2小时学会Spring Boot第二讲笔记")
[[来自： [
qq\_20367813的博客]{.blog_title}](https://blog.csdn.net/qq_20367813)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/qq_37202894/9905728,BlogCommendFromQuerySearch_26&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/qq_37202894/9905728,BlogCommendFromQuerySearch_26&quot;}">

[](https://download.csdn.net/download/qq_37202894/9905728)
<div class="content">

<div>

[下载]{.type}
#### Java*入门*第一季 {#java入门第一季 .text-truncate .oneline .clearfix}

[07-20]{.data .float-right}

</div>

<div class="desc oneline">

慕课网Java入门第一季笔记整理

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_40078053/article/details/79869321,BlogCommendFromQuerySearch_27&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_40078053/article/details/79869321,BlogCommendFromQuerySearch_27&quot;}">

<div class="content">

[](https://blog.csdn.net/weixin_40078053/article/details/79869321 "Nginx详细入门到精通笔记一")
#### Nginx详细*入门*到精通*笔记*一 {#nginx详细入门到精通笔记一 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[04-11]{.date .hover-show} [ 717]{.read-num .hover-hide}

</div>

[[简介Nginx是高效可靠的http中间件，支持海量的并发请求，稳定开源可靠，代理服务环境调试确认： 1.确认系统网络2.确认yum可用3.确认关闭iptables规则4.确认停用selinux安装调试...]{.desc
.oneline}](https://blog.csdn.net/weixin_40078053/article/details/79869321 "Nginx详细入门到精通笔记一")
[[来自： [
胡芳文白白的博客]{.blog_title}](https://blog.csdn.net/weixin_40078053)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_64" data-pid="64"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_64-81&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_64-81&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad28" class="mediav_ad">

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/cuiping1993/article/details/78018597,BlogCommendFromQuerySearch_28&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/cuiping1993/article/details/78018597,BlogCommendFromQuerySearch_28&quot;}">

<div class="content">

[](https://blog.csdn.net/cuiping1993/article/details/78018597 "springboot慕课网2小时入门课程总结")
#### springboot*慕课网*2小时*入门*课程总结 {#springboot慕课网2小时入门课程总结 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-18]{.date .hover-show} [ 1180]{.read-num .hover-hide}

</div>

[[慕课网视频地址：http://www.imooc.com/video/13598
springboot慕课网2小时入门课程总...]{.desc
.oneline}](https://blog.csdn.net/cuiping1993/article/details/78018597 "springboot慕课网2小时入门课程总结")
[[来自： [
Neven的博客]{.blog_title}](https://blog.csdn.net/cuiping1993)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_41139830/article/details/82795588,BlogCommendFromQuerySearch_29&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_41139830/article/details/82795588,BlogCommendFromQuerySearch_29&quot;}">

<div class="content">

[](https://blog.csdn.net/qq_41139830/article/details/82795588 "React简书开发实战课程笔记——1")
#### React简书开发实战课程*笔记*——1 {#react简书开发实战课程笔记1 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-21]{.date .hover-show} [ 268]{.read-num .hover-hide}

</div>

[[这是我在看了imooc中的React简书开发实战课程之后记下的笔记，在这做下备份，以便日后复习。
1、dangerouslySetInnerHTML属性 当React元素包含html标签时，如...]{.desc
.oneline}](https://blog.csdn.net/qq_41139830/article/details/82795588 "React简书开发实战课程笔记——1")
[[来自： [
Jarns的博客]{.blog_title}](https://blog.csdn.net/qq_41139830)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/powersn/article/details/53501111,BlogCommendFromQuerySearch_30&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/powersn/article/details/53501111,BlogCommendFromQuerySearch_30&quot;}">

<div class="content">

[](https://blog.csdn.net/powersn/article/details/53501111 "慕课网JAVA基础第二季最后的一个作业")
#### *慕课网*JAVA基础第二季最后的一个作业 {#慕课网java基础第二季最后的一个作业 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[12-07]{.date .hover-show} [ 573]{.read-num .hover-hide}

</div>

[[package com.imooc; import java.util.Scanner; //创建一个Car类 public
class Car { String name ; int ...]{.desc
.oneline}](https://blog.csdn.net/powersn/article/details/53501111 "慕课网JAVA基础第二季最后的一个作业")
[[来自： [
powersn的Java之旅]{.blog_title}](https://blog.csdn.net/powersn)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/marvinysh/10492465,BlogCommendFromQuerySearch_31&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/marvinysh/10492465,BlogCommendFromQuerySearch_31&quot;}">

[](https://download.csdn.net/download/marvinysh/10492465)
<div class="content">

<div>

[下载]{.type}
#### *Redis*从*入门*到高可用，分布式实践 （完整13章版本） {#redis从入门到高可用分布式实践-完整13章版本 .text-truncate .oneline .clearfix}

[06-22]{.data .float-right}

</div>

<div class="desc oneline">

全13章 第1章 Redis初识
带领听众进入Redis的世界，了解它的前世今生、众多特性、应用场景、安装配置、简单使用，可以让听众对Redis有一个全面的认识。
第2章 API的理解和使用 全面介绍了Redis提供的5种数据结构字符串（...

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/wang10253174289/article/details/81362803,BlogCommendFromQuerySearch_32&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/wang10253174289/article/details/81362803,BlogCommendFromQuerySearch_32&quot;}">

<div class="content">

[](https://blog.csdn.net/wang10253174289/article/details/81362803 "初学Redis（自己做笔记用）")
#### 初学*Redis*（自己做*笔记*用） {#初学redis自己做笔记用 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[08-02]{.date .hover-show} [ 96]{.read-num .hover-hide}

</div>

[[1 redis是什么?   Redis是一个开源的使用ANSI
C语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。换句话说，Redis就像是一个H...]{.desc
.oneline}](https://blog.csdn.net/wang10253174289/article/details/81362803 "初学Redis（自己做笔记用）")
[[来自： [
wang10253174289的博客]{.blog_title}](https://blog.csdn.net/wang10253174289)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_65" data-pid="65"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_65-84&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_65-84&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div id="three_ad33" class="mediav_ad">

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/lxh123456789asd/article/details/80845775,BlogCommendFromQuerySearch_33&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/lxh123456789asd/article/details/80845775,BlogCommendFromQuerySearch_33&quot;}">

<div class="content">

[](https://blog.csdn.net/lxh123456789asd/article/details/80845775 "redis入门学习笔记（Windows）")
#### *redis入门*学习*笔记*（Windows） {#redis入门学习笔记windows .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[06-28]{.date .hover-show} [ 124]{.read-num .hover-hide}

</div>

[[待续。。。。。在windows上部署redis服务redis-server --service-install
redis.windows.conf启动redis服务redis-server --se...]{.desc
.oneline}](https://blog.csdn.net/lxh123456789asd/article/details/80845775 "redis入门学习笔记（Windows）")
[[来自： [
lxh123456789asd的博客]{.blog_title}](https://blog.csdn.net/lxh123456789asd)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/zjt980452483/10628522,BlogCommendFromQuerySearch_34&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/zjt980452483/10628522,BlogCommendFromQuerySearch_34&quot;}">

[](https://download.csdn.net/download/zjt980452483/10628522)
<div class="content">

<div>

[下载]{.type}
#### 最新*redis*从*入门*到高可用，分布式实践教程 {#最新redis从入门到高可用分布式实践教程 .text-truncate .oneline .clearfix}

[08-27]{.data .float-right}

</div>

<div class="desc oneline">

非常详细的Redis教程，不仅手把手教你如何安装使用，还系统讲解使用Redis之后运维过程中可能出现的问题和解决办法，希望能帮助大家。

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/valada/article/details/79909232,BlogCommendFromQuerySearch_35&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/valada/article/details/79909232,BlogCommendFromQuerySearch_35&quot;}">

<div class="content">

[](https://blog.csdn.net/valada/article/details/79909232 "Redis 入门到分布式实践")
#### *Redis* *入门*到分布式实践 {#redis-入门到分布式实践 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[04-12]{.date .hover-show} [ 384]{.read-num .hover-hide}

</div>

[[课程简介 这是一门 Redis 从零基础开始逐步成为 Redis
专家的进阶教程，主要包括认识 Redis、基础 API 的理解和使用、使用 Redis
客户端、Redis 高级功能、Redis 持久...]{.desc
.oneline}](https://blog.csdn.net/valada/article/details/79909232 "Redis 入门到分布式实践")
[[来自： [
GitChat]{.blog_title}](https://blog.csdn.net/valada)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/lovezhaohaimig/article/details/80399582,BlogCommendFromQuerySearch_36&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/lovezhaohaimig/article/details/80399582,BlogCommendFromQuerySearch_36&quot;}">

<div class="content">

[](https://blog.csdn.net/lovezhaohaimig/article/details/80399582 "Redis从入门到精通：中级篇")
#### *Redis*从*入门*到精通：中级篇 {#redis从入门到精通中级篇 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[05-26]{.date .hover-show} [ 203]{.read-num .hover-hide}

</div>

[[摘要:
原文链接：http://www.cnblogs.com/xrq730/p/8944539.html，转载请注明出处，谢谢
本文目录 上一篇文章以认识Redis为主，写了Redis系列的第一篇，...]{.desc
.oneline}](https://blog.csdn.net/lovezhaohaimig/article/details/80399582 "Redis从入门到精通：中级篇")
[[来自： [
lovezhaohaimig的博客]{.blog_title}](https://blog.csdn.net/lovezhaohaimig)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_26915707/article/details/82795135,BlogCommendFromQuerySearch_37&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_26915707/article/details/82795135,BlogCommendFromQuerySearch_37&quot;}">

<div class="content">

[](https://blog.csdn.net/qq_26915707/article/details/82795135 "Python3入门机器学习经典算法与应用3")
#### Python3*入门*机器学习经典算法与应用3 {#python3入门机器学习经典算法与应用3 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-20]{.date .hover-show} [ 353]{.read-num .hover-hide}

</div>

[[3-1 Jupter notebook基础 3-2 Jupter notebook中的魔法命令 1.执行脚本    
%run file/hello.py     hello('ming') ...]{.desc
.oneline}](https://blog.csdn.net/qq_26915707/article/details/82795135 "Python3入门机器学习经典算法与应用3")
[[来自： [
qq\_26915707的博客]{.blog_title}](https://blog.csdn.net/qq_26915707)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_66" data-pid="66"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_66-808&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_66-808&quot;,&quot;con&quot;:&quot;,,&quot;}">

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/polo_longsan/article/details/78955441,BlogCommendFromQuerySearch_38&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/polo_longsan/article/details/78955441,BlogCommendFromQuerySearch_38&quot;}">

<div class="content">

[](https://blog.csdn.net/polo_longsan/article/details/78955441 "redis学习笔记（1）：redis基础")
#### *redis*学习*笔记*（1）：*redis*基础 {#redis学习笔记1redis基础 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[01-02]{.date .hover-show} [ 560]{.read-num .hover-hide}

</div>

[[redis是一个远程内存数据库，共有5中数据类型：STRING(字符串)，LIST(列表)，SET(集合)，HASH(散列)，ZSET(有序集合)。5中数据类型的基本操作：
1、字符串 redis...]{.desc
.oneline}](https://blog.csdn.net/polo_longsan/article/details/78955441 "redis学习笔记（1）：redis基础")
[[来自： [
polo\_longsan的专栏]{.blog_title}](https://blog.csdn.net/polo_longsan)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/clh386/article/details/78622879,BlogCommendFromQuerySearch_39&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/clh386/article/details/78622879,BlogCommendFromQuerySearch_39&quot;}">

<div class="content">

[](https://blog.csdn.net/clh386/article/details/78622879 "史上最全的SpringMVC学习笔记（慕课网）")
#### 史上最全的SpringMVC学习*笔记*（*慕课网*） {#史上最全的springmvc学习笔记慕课网 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[11-24]{.date .hover-show} [ 440]{.read-num .hover-hide}

</div>

[[史上最全的SpringMVC学习笔记
，包括springmvc+spring+Hibernate配置文件，通过jquery和Ajax与后台交互。...]{.desc
.oneline}](https://blog.csdn.net/clh386/article/details/78622879 "史上最全的SpringMVC学习笔记（慕课网）")
[[来自： [
clh386的博客]{.blog_title}](https://blog.csdn.net/clh386)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/mys_mys/article/details/82563450,BlogCommendFromQuerySearch_40&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/mys_mys/article/details/82563450,BlogCommendFromQuerySearch_40&quot;}">

<div class="content">

[](https://blog.csdn.net/mys_mys/article/details/82563450 "10小时入门大数据（一）------大数据概述")
#### 10小时*入门*大数据（一）------大数据概述 {#小时入门大数据一------大数据概述 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-10]{.date .hover-show} [ 153]{.read-num .hover-hide}

</div>

[[1、环境参数 Linux—CentOS(6.4) Hadoop—CDH(5.7) 开发工具：IDEA
2、大数据生态圈 Hadoop...]{.desc
.oneline}](https://blog.csdn.net/mys_mys/article/details/82563450 "10小时入门大数据（一）------大数据概述")
[[来自： [
倩mys的博客]{.blog_title}](https://blog.csdn.net/mys_mys)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_37508578/article/details/80507093,BlogCommendFromQuerySearch_41&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_37508578/article/details/80507093,BlogCommendFromQuerySearch_41&quot;}">

<div class="content">

[](https://blog.csdn.net/weixin_37508578/article/details/80507093 "慕课网电商实战学习笔记")
#### *慕课网*电商实战学习*笔记* {#慕课网电商实战学习笔记 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[06-06]{.date .hover-show} [ 161]{.read-num .hover-hide}

</div>

[[　1.项目初始化　　1.ideal相关操作　　\*ideal中加载本地maven\*ideal中加载本地jdkideal设置常用工具的快捷键（以前是eclipse用的多，习惯了就改为eclipse，也可以...]{.desc
.oneline}](https://blog.csdn.net/weixin_37508578/article/details/80507093 "慕课网电商实战学习笔记")
[[来自： [
weixin\_37508578的博客]{.blog_title}](https://blog.csdn.net/weixin_37508578)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/baidu_24352355/10399275,BlogCommendFromQuerySearch_42&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/baidu_24352355/10399275,BlogCommendFromQuerySearch_42&quot;}">

[](https://download.csdn.net/download/baidu_24352355/10399275)
<div class="content">

<div>

[下载]{.type}
#### ZooKeeper分布式专题与Dubbo微服务*入门*课程 {#zookeeper分布式专题与dubbo微服务入门课程 .text-truncate .oneline .clearfix}

[05-08]{.data .float-right}

</div>

<div class="desc oneline">

ZooKeeper分布式专题与Dubbo微服务入门 第1章 分布式系统概念与ZooKeeper简介
对分布式系统以及ZooKeeper进行简介，使得大家对其有大致的了解 第2章
ZooKeeper安装 如何安装ZooKeeper以及对Zo...

</div>

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_67" data-pid="67"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_67-808&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_67-808&quot;,&quot;con&quot;:&quot;,,&quot;}">

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/woshiyiyiyeye/10201039,BlogCommendFromQuerySearch_43&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/woshiyiyiyeye/10201039,BlogCommendFromQuerySearch_43&quot;}">

[](https://download.csdn.net/download/woshiyiyiyeye/10201039)
<div class="content">

<div>

[下载]{.type}
#### 十小时大数据*入门* 视频资源 百度云 {#十小时大数据入门-视频资源-百度云 .text-truncate .oneline .clearfix}

[01-11]{.data .float-right}

</div>

<div class="desc oneline">

十小时大数据入门 hadoop介绍入门 视频资源 仅供学习，如果喜欢请购买正版。

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_40581617/article/details/80595019,BlogCommendFromQuerySearch_44&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/weixin_40581617/article/details/80595019,BlogCommendFromQuerySearch_44&quot;}">

<div class="content">

[](https://blog.csdn.net/weixin_40581617/article/details/80595019 "redis入门视频分享")
#### *redis入门*视频分享 {#redis入门视频分享 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[06-06]{.date .hover-show} [ 173]{.read-num .hover-hide}

</div>

[[转载请注明出处哈:http://carlosfu.iteye.com/blog/2240426    
近期给实习生培训redis相关课程，同时录制了一份视频，比较入门，不才分享给大家。 
  声明：...]{.desc
.oneline}](https://blog.csdn.net/weixin_40581617/article/details/80595019 "redis入门视频分享")
[[来自： [
weixin\_40581617的博客]{.blog_title}](https://blog.csdn.net/weixin_40581617)]{.blog_title_box
.oneline}

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/baidu_33251031/9326149,BlogCommendFromQuerySearch_45&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/baidu_33251031/9326149,BlogCommendFromQuerySearch_45&quot;}">

[](https://download.csdn.net/download/baidu_33251031/9326149)
<div class="content">

<div>

[下载]{.type}
#### *慕课网*《Html Css》*笔记* {#慕课网html-css笔记 .text-truncate .oneline .clearfix}

[12-04]{.data .float-right}

</div>

<div class="desc oneline">

慕课网《Html Css》笔记

</div>

</div>

</div>

<div
class="recommend-item-box recommend-box-ident recommend-download-box clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/fjzzmike/10257452,BlogCommendFromQuerySearch_46&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://download.csdn.net/download/fjzzmike/10257452,BlogCommendFromQuerySearch_46&quot;}">

[](https://download.csdn.net/download/fjzzmike/10257452)
<div class="content">

<div>

[下载]{.type}
#### 10小时*入门*大数据 {#小时入门大数据 .text-truncate .oneline .clearfix}

[02-24]{.data .float-right}

</div>

<div class="desc oneline">

链接: https://pan.baidu.com/s/1smuDvdF 密码: f3qp
Kafka-原理剖析及实战演练视频教程 Kafka-极客学院 610-10小时入门大数据

</div>

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/m0_37638508/article/details/80502718,BlogCommendFromQuerySearch_47&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/m0_37638508/article/details/80502718,BlogCommendFromQuerySearch_47&quot;}">

<div class="content">

[](https://blog.csdn.net/m0_37638508/article/details/80502718 "去哪儿vue笔记")
#### 去哪儿vue*笔记* {#去哪儿vue笔记 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[05-29]{.date .hover-show} [ 318]{.read-num .hover-hide}

</div>

[[一.打开index.html  修改里面的 name='viewport'  &amp;lt;meta
name=&quot;viewport&quot; content=&quot;width=de...]{.desc
.oneline}](https://blog.csdn.net/m0_37638508/article/details/80502718 "去哪儿vue笔记")
[[来自： [
m0\_37638508的博客]{.blog_title}](https://blog.csdn.net/m0_37638508)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-ad-box">

<div id="kp_box_68" data-pid="68"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_68-808&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_68-808&quot;,&quot;con&quot;:&quot;,,&quot;}">

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/pansaky/article/details/80259048,BlogCommendFromQuerySearch_48&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/pansaky/article/details/80259048,BlogCommendFromQuerySearch_48&quot;}">

<div class="content">

[](https://blog.csdn.net/pansaky/article/details/80259048 "软件测试理论整理（源自慕课网视频学习整理）")
#### 软件测试理论整理（源自*慕课网*视频学习整理） {#软件测试理论整理源自慕课网视频学习整理 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[05-09]{.date .hover-show} [ 375]{.read-num .hover-hide}

</div>

[[软件的测试方法/手段： 黑盒/白盒|静态/动态|手工/自动化
按照测试阶段划分： →单元测试：基于代码逻辑实现的测试
→集成测试：基于模块、部件集成的测试
→系统测试：基于软件需求、功能实现的全量测试...]{.desc
.oneline}](https://blog.csdn.net/pansaky/article/details/80259048 "软件测试理论整理（源自慕课网视频学习整理）")
[[来自： [
pansaky的博客]{.blog_title}](https://blog.csdn.net/pansaky)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/cherryshi520/article/details/52606548,BlogCommendFromQuerySearch_49&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/cherryshi520/article/details/52606548,BlogCommendFromQuerySearch_49&quot;}">

<div class="content">

[](https://blog.csdn.net/cherryshi520/article/details/52606548 "慕课网学习笔记")
#### *慕课网*学习*笔记* {#慕课网学习笔记 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-21]{.date .hover-show} [ 252]{.read-num .hover-hide}

</div>

[[1. 站点连接服务器 访问方式 ftp]{.desc
.oneline}](https://blog.csdn.net/cherryshi520/article/details/52606548 "慕课网学习笔记")
[[来自： [
cherryshi520的博客]{.blog_title}](https://blog.csdn.net/cherryshi520)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/Dr_Neo/article/details/46941859,BlogCommendHotData_0&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/Dr_Neo/article/details/46941859,BlogCommendHotData_0&quot;}">

<div class="content">

[](https://blog.csdn.net/Dr_Neo/article/details/46941859 "Eclipse中离线安装ADT插件详细教程")
#### Eclipse中离线安装ADT插件详细教程 {#eclipse中离线安装adt插件详细教程 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[07-18]{.date .hover-show} [ 49489]{.read-num .hover-hide}

</div>

[[在搭建Android开发环境的时候，我们需要为Eclipse安装ADT（Android
Development
Tools）插件，这个插件可以为用户提供一个强大的Android集成开发环境。通过给Ec...]{.desc
.oneline}](https://blog.csdn.net/Dr_Neo/article/details/46941859 "Eclipse中离线安装ADT插件详细教程")
[[来自： [
Dr.Neo的专栏]{.blog_title}](https://blog.csdn.net/Dr_Neo)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/meng564764406/article/details/52444644,BlogCommendHotData_1&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/meng564764406/article/details/52444644,BlogCommendHotData_1&quot;}">

<div class="content">

[](https://blog.csdn.net/meng564764406/article/details/52444644 "将Excel文件导入数据库（POI+Excel+MySQL+jsp页面导入）第一次优化")
#### 将Excel文件导入数据库（POI+Excel+MySQL+jsp页面导入）第一次优化 {#将excel文件导入数据库poiexcelmysqljsp页面导入第一次优化 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-05]{.date .hover-show} [ 5322]{.read-num .hover-hide}

</div>

[[本篇文章是根据我的上篇博客，给出的改进版，由于时间有限，仅做了一个简单的优化。相关文章：将excel导入数据库2018年4月1日，新增下载地址链接：点击打开源码下载地址十分抱歉，这个链接地址没有在这篇...]{.desc
.oneline}](https://blog.csdn.net/meng564764406/article/details/52444644 "将Excel文件导入数据库（POI+Excel+MySQL+jsp页面导入）第一次优化")
[[来自： [
Lynn\_Blog]{.blog_title}](https://blog.csdn.net/meng564764406)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/wuchengzeng/article/details/50037611,BlogCommendHotData_2&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/wuchengzeng/article/details/50037611,BlogCommendHotData_2&quot;}">

<div class="content">

[](https://blog.csdn.net/wuchengzeng/article/details/50037611 "jquery/js实现一个网页同时调用多个倒计时(最新的)")
#### jquery/js实现一个网页同时调用多个倒计时(最新的) {#jqueryjs实现一个网页同时调用多个倒计时最新的 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[11-25]{.date .hover-show} [ 5021]{.read-num .hover-hide}

</div>

[[jquery/js实现一个网页同时调用多个倒计时(最新的)
最近需要网页添加多个倒计时. 查阅网络,基本上都是千遍一律的不好用.
自己按需写了个.希望对大家有用. 有用请赞一个哦!...]{.desc
.oneline}](https://blog.csdn.net/wuchengzeng/article/details/50037611 "jquery/js实现一个网页同时调用多个倒计时(最新的)")
[[来自： [
websites]{.blog_title}](https://blog.csdn.net/wuchengzeng)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/jimo_lonely/article/details/78782262,BlogCommendHotData_3&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/jimo_lonely/article/details/78782262,BlogCommendHotData_3&quot;}">

<div class="content">

[](https://blog.csdn.net/jimo_lonely/article/details/78782262 "前后端分离之Springboot后端")
#### 前后端分离之Springboot后端 {#前后端分离之springboot后端 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[12-12]{.date .hover-show} [ 9834]{.read-num .hover-hide}

</div>

[[这是上一篇博客前后端分离之Java后端的重写. 源码
前后端分离的后端主要解决的就2个问题 :
跨域访问(CORS)和token校验,下面快速说明.1.项目环境使用Intellij IDE.
项...]{.desc
.oneline}](https://blog.csdn.net/jimo_lonely/article/details/78782262 "前后端分离之Springboot后端")
[[来自： [
jimo\_lonely的博客]{.blog_title}](https://blog.csdn.net/jimo_lonely)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/roguesir/article/details/77104246,BlogCommendHotData_4&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/roguesir/article/details/77104246,BlogCommendHotData_4&quot;}">

<div class="content">

[](https://blog.csdn.net/roguesir/article/details/77104246 "人脸检测工具face_recognition的安装与应用")
#### 人脸检测工具face\_recognition的安装与应用 {#人脸检测工具face_recognition的安装与应用 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[08-11]{.date .hover-show} [ 7820]{.read-num .hover-hide}

</div>

[[人脸检测工具face\_recognition的安装与应用]{.desc
.oneline}](https://blog.csdn.net/roguesir/article/details/77104246 "人脸检测工具face_recognition的安装与应用")
[[来自： [
roguesir的博客]{.blog_title}](https://blog.csdn.net/roguesir)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_36892341/article/details/73918672,BlogCommendHotData_5&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/qq_36892341/article/details/73918672,BlogCommendHotData_5&quot;}">

<div class="content">

[](https://blog.csdn.net/qq_36892341/article/details/73918672 "linux上安装Docker(非常简单的安装方法)")
#### linux上安装Docker(非常简单的安装方法) {#linux上安装docker非常简单的安装方法 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[06-29]{.date .hover-show} [ 78671]{.read-num .hover-hide}

</div>

[[最近比较有空，大四出来实习几个月了，作为实习狗的我，被叫去研究Docker了，汗汗！
Docker的三大核心概念：镜像、容器、仓库
镜像：类似虚拟机的镜像、用俗话说就是安装文件。
容器：类似一个轻量...]{.desc
.oneline}](https://blog.csdn.net/qq_36892341/article/details/73918672 "linux上安装Docker(非常简单的安装方法)")
[[来自： [
我走小路的博客]{.blog_title}](https://blog.csdn.net/qq_36892341)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/boling_cavalry/article/details/76857936,BlogCommendHotData_6&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/boling_cavalry/article/details/76857936,BlogCommendHotData_6&quot;}">

<div class="content">

[](https://blog.csdn.net/boling_cavalry/article/details/76857936 "Docker下实战zabbix三部曲之一：极速体验")
#### Docker下实战zabbix三部曲之一：极速体验 {#docker下实战zabbix三部曲之一极速体验 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[08-10]{.date .hover-show} [ 14019]{.read-num .hover-hide}

</div>

[[用docker来缩减搭建时间，让读者们尽快投入zabbix系统的体验和实践]{.desc
.oneline}](https://blog.csdn.net/boling_cavalry/article/details/76857936 "Docker下实战zabbix三部曲之一：极速体验")
[[来自： [
boling\_cavalry的博客]{.blog_title}](https://blog.csdn.net/boling_cavalry)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/jackfrued/article/details/44921941,BlogCommendHotData_7&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/jackfrued/article/details/44921941,BlogCommendHotData_7&quot;}">

<div class="content">

[](https://blog.csdn.net/jackfrued/article/details/44921941 "Java面试题全集（上）")
#### Java面试题全集（上） {#java面试题全集上 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[04-08]{.date .hover-show} [ 912537]{.read-num .hover-hide}

</div>

[[2013年年底的时候，我看到了网上流传的一个叫做《Java面试题大全》的东西，认真的阅读了以后发现里面的很多题目是重复且没有价值的题目，还有不少的参考答案也是错误的，于是我花了半个月时间对这个所谓的《...]{.desc
.oneline}](https://blog.csdn.net/jackfrued/article/details/44921941 "Java面试题全集（上）")
[[来自： [
骆昊的技术专栏]{.blog_title}](https://blog.csdn.net/jackfrued)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/yangwei282367751/article/details/52426911,BlogCommendHotData_8&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/yangwei282367751/article/details/52426911,BlogCommendHotData_8&quot;}">

<div class="content">

[](https://blog.csdn.net/yangwei282367751/article/details/52426911 "关于计算时间复杂度和空间复杂度")
#### 关于计算时间复杂度和空间复杂度 {#关于计算时间复杂度和空间复杂度 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[09-04]{.date .hover-show} [ 33644]{.read-num .hover-hide}

</div>

[[相信学习编程的同学，或多或少都接触到算法的时间复杂度和空间复杂度了，那我来讲讲怎么计算。
       常用的算法的时间复杂度和空间复杂度
一，求解算法的时间复杂度，其具体步骤是： 　　⑴ 找出算法...]{.desc
.oneline}](https://blog.csdn.net/yangwei282367751/article/details/52426911 "关于计算时间复杂度和空间复杂度")
[[来自： [
杨威的博客]{.blog_title}](https://blog.csdn.net/yangwei282367751)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/gefangshuai/article/details/50328451,BlogCommendHotData_9&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/gefangshuai/article/details/50328451,BlogCommendHotData_9&quot;}">

<div class="content">

[](https://blog.csdn.net/gefangshuai/article/details/50328451 "关于SpringBoot bean无法注入的问题（与文件包位置有关）")
#### 关于SpringBoot bean无法注入的问题（与文件包位置有关） {#关于springboot-bean无法注入的问题与文件包位置有关 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[12-16]{.date .hover-show} [ 27791]{.read-num .hover-hide}

</div>

[[问题场景描述整个项目通过Maven构建，大致结构如下：
核心Spring框架一个module spring-boot-base service和dao一个module
server-core 提供系统...]{.desc
.oneline}](https://blog.csdn.net/gefangshuai/article/details/50328451 "关于SpringBoot bean无法注入的问题（与文件包位置有关）")
[[来自： [
开发随笔]{.blog_title}](https://blog.csdn.net/gefangshuai)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/xiaolang85/article/details/13021339,BlogCommendHotData_10&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/xiaolang85/article/details/13021339,BlogCommendHotData_10&quot;}">

<div class="content">

[](https://blog.csdn.net/xiaolang85/article/details/13021339 "ZooKeeper系列之二:Zookeeper常用命令")
#### ZooKeeper系列之二:Zookeeper常用命令 {#zookeeper系列之二zookeeper常用命令 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[10-25]{.date .hover-show} [ 284072]{.read-num .hover-hide}

</div>

[[ZooKeeper服务命令:     
在准备好相应的配置之后，可以直接通过zkServer.sh
这个脚本进行服务的相关操作 1. 启动ZK服务:       sh
bin/zkServer...]{.desc
.oneline}](https://blog.csdn.net/xiaolang85/article/details/13021339 "ZooKeeper系列之二:Zookeeper常用命令")
[[来自： [
xiaolang85的专栏]{.blog_title}](https://blog.csdn.net/xiaolang85)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u014682691/article/details/50787366,BlogCommendHotData_11&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/u014682691/article/details/50787366,BlogCommendHotData_11&quot;}">

<div class="content">

[](https://blog.csdn.net/u014682691/article/details/50787366 "12种排序算法详解")
#### 12种排序算法详解 {#种排序算法详解 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[03-03]{.date .hover-show} [ 26626]{.read-num .hover-hide}

</div>

[[作者：寒小阳 时间：2013年9月。
出处：http://blog.csdn.net/han\_xiaoyang/article/details/12163251。
声明：版权所有，转载请...]{.desc
.oneline}](https://blog.csdn.net/u014682691/article/details/50787366 "12种排序算法详解")
[[来自： [
u014682691的专栏]{.blog_title}](https://blog.csdn.net/u014682691)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-item-box recommend-box-ident type_blog clearfix"
data-track-view="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/xu__cg/article/details/53011258,BlogCommendHotData_12&quot;}"
data-track-click="{&quot;mod&quot;:&quot;popu_387&quot;,&quot;con&quot;:&quot;,https://blog.csdn.net/xu__cg/article/details/53011258,BlogCommendHotData_12&quot;}">

<div class="content">

[](https://blog.csdn.net/xu__cg/article/details/53011258 "Java设计模式学习08——组合模式")
#### Java设计模式学习08——组合模式 {#java设计模式学习08组合模式 .text-truncate .oneline}

<div class="info-box d-flex align-content-center">

[11-02]{.date .hover-show} [ 696]{.read-num .hover-hide}

</div>

[[一、组合模式适用场景把部分和整体的关系用树形结构来表示，从而使客户端可以使用统一的方式对部分对象和整体对象进行管理。二、组合模式结构
抽象构件(Conponent)角色：所有类的共有接口，定义了叶子和...]{.desc
.oneline}](https://blog.csdn.net/xu__cg/article/details/53011258 "Java设计模式学习08——组合模式")
[[来自： [
小小本科生成长之路]{.blog_title}](https://blog.csdn.net/xu__cg)]{.blog_title_box
.oneline}

</div>

</div>

<div class="recommend-loading-box">

![](https://csdnimg.cn/release/phoenix/images/feedLoading.gif)

</div>

<div class="recommend-end-box">

没有更多推荐了，[返回首页](https://blog.csdn.net/){.c-blue .c-blue-hover
.c-blue-focus}

</div>

</div>

<div id="asideProfile" class="aside-box">

<div class="profile-intro d-flex">

<div class="avatar-box d-flex justify-content-center flex-column">

[![](https://avatar.csdn.net/A/6/2/3_fulq1234.jpg){.avatar_pic}](https://blog.csdn.net/fulq1234)

</div>

<div class="user-info d-flex justify-content-center flex-column">

[我爱圆溜溜](https://blog.csdn.net/fulq1234){#uid}

</div>

<div class="opt-box d-flex justify-content-center flex-column">

[ [关注]{#btnAttent .btn .btn-sm .btn-red-hollow .attention}
]{.csdn-tracking-statistics .tracking-click data-mod="popu_379"}

</div>

</div>

<div class="data-info d-flex item-tiling">

[原创](https://blog.csdn.net/fulq1234?t=1)
:   [[126]{.count}](https://blog.csdn.net/fulq1234?t=1)

<!-- -->

粉丝
:   [39]{#fan .count}

<!-- -->

喜欢
:   [9]{.count}

<!-- -->

评论
:   [11]{.count}

</div>

<div class="grade-box clearfix">

等级：

:   

<!-- -->

访问：
:   7万+

<!-- -->

积分：
:   1939

<!-- -->

排名：
:   3万+

</div>

</div>

<div class="csdn-tracking-statistics mb8 box-shadow" data-pid="blog"
data-mod="popu_4" style="height:250px;">

<div id="cpro_u2734133" class="aside-content text-center">

<div id="kp_box_56" data-pid="56"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_56-76&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_56-76&quot;,&quot;con&quot;:&quot;,,&quot;}">

</div>

</div>

</div>

<div id="asideNewArticle" class="aside-box">

### 最新文章 {#最新文章 .aside-title}

<div class="aside-content">

-   [Bootstrap table
    下载Excel文件，](https://blog.csdn.net/fulq1234/article/details/86293139)
-   [Spring
    Boot利用poi导出Excel](https://blog.csdn.net/fulq1234/article/details/86234451)
-   [Thymeleaf常用th标签](https://blog.csdn.net/fulq1234/article/details/85003273)
-   [css样式](https://blog.csdn.net/fulq1234/article/details/84718394)
-   [js实现等待效果](https://blog.csdn.net/fulq1234/article/details/84718358)

</div>

</div>

<div id="asideCategory" class="aside-box flexible-box">

### 个人分类 {#个人分类 .aside-title}

<div class="aside-content">

-   [[maven]{.title .oneline} [3篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/6499302){.clearfix}
-   [[android]{.title .oneline} [3篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/6499336){.clearfix}
-   [[javaSE]{.title .oneline} [12篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/6530905){.clearfix}
-   [[linux]{.title .oneline} [6篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7361893){.clearfix}
-   [[c\#]{.title .oneline} [6篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7389307){.clearfix}
-   [[spring]{.title .oneline} [22篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7405877){.clearfix}
-   [[其它]{.title .oneline} [19篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7491933){.clearfix}
-   [[struts]{.title .oneline} [4篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7645468){.clearfix}
-   [[hadoop]{.title .oneline} [8篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7664934){.clearfix}
-   [[scratch]{.title .oneline} [1篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/7788042){.clearfix}
-   [[jQuery]{.title .oneline} [1篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/category/8477713){.clearfix}

</div>

[展开]{.btn .btn-link-blue .flexible-btn}

</div>

<div id="asideArchive" class="aside-box flexible-box">

### 归档 {#归档 .aside-title}

<div class="aside-content">

-   [2019年1月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2019/01)
-   [2018年12月 [1篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/12)
-   [2018年11月 [1篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/11)
-   [2018年10月 [4篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/10)
-   [2018年9月 [6篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/09)
-   [2018年7月 [5篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/07)
-   [2018年6月 [10篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/06)
-   [2018年5月 [11篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/05)
-   [2018年4月 [3篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/04)
-   [2018年3月 [5篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/03)
-   [2018年2月 [8篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/02)
-   [2018年1月 [11篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2018/01)
-   [2017年12月 [5篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/12)
-   [2017年11月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/11)
-   [2017年10月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/10)
-   [2017年9月 [7篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/09)
-   [2017年8月 [1篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/08)
-   [2017年7月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/07)
-   [2017年6月 [4篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/06)
-   [2017年5月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/05)
-   [2017年4月 [3篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/04)
-   [2017年3月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/03)
-   [2017年2月 [7篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/02)
-   [2017年1月 [3篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2017/01)
-   [2016年12月 [4篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2016/12)
-   [2016年11月 [11篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2016/11)
-   [2016年3月 [3篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2016/03)
-   [2015年5月 [2篇]{.count
    .float-right}](https://blog.csdn.net/fulq1234/article/month/2015/05)

</div>

[展开]{.btn .btn-link-blue .flexible-btn}

</div>

<div id="asideHotArticle" class="aside-box">

### 热门文章 {#热门文章 .aside-title}

<div class="aside-content">

-   [webuploader上传遇到的问题](https://blog.csdn.net/fulq1234/article/details/63252281)

    阅读量：[15004]{}

-   [FrameMaker从零到学习编码](https://blog.csdn.net/fulq1234/article/details/53433868)

    阅读量：[5017]{}

-   [maven的中央仓库位置:https://repo.maven.apache.org/maven2](https://blog.csdn.net/fulq1234/article/details/53005474)

    阅读量：[4970]{}

-   [SpringBoot实战和原理分析学习](https://blog.csdn.net/fulq1234/article/details/79129845)

    阅读量：[2843]{}

-   [用jackson实现json和字符串直接的转换](https://blog.csdn.net/fulq1234/article/details/61919598)

    阅读量：[2552]{}

</div>

</div>

<div id="asideNewComments" class="aside-box">

### 最新评论 {#最新评论 .aside-title}

<div class="aside-content">

-   [webuploader上传遇到的问题](https://blog.csdn.net/fulq1234/article/details/63252281#comments){.title
    .text-truncate}

    [fulq1234](https://my.csdn.net/fulq1234){.user-name}：\[reply\]qq\_37505395\[/reply\]
    不客气

-   [webuploader上传遇到的问题](https://blog.csdn.net/fulq1234/article/details/63252281#comments){.title
    .text-truncate}

    [qq\_37505395](https://my.csdn.net/qq_37505395){.user-name}：一开始我还以为是开了多台实例的问题呢，现在才发现不是，插件是多线程上传，多谢楼主

-   [EasyUi](https://blog.csdn.net/fulq1234/article/details/53445015#comments){.title
    .text-truncate}

    [shichuwu](https://my.csdn.net/shichuwu){.user-name}：EasyUI学习了，感谢小编的分享

-   [c\#学习1](https://blog.csdn.net/fulq1234/article/details/79163171#comments){.title
    .text-truncate}

    [Aran\_WDX](https://my.csdn.net/Aran_WDX){.user-name}：基础很详细，感谢分享

-   [c\#学习1](https://blog.csdn.net/fulq1234/article/details/79163171#comments){.title
    .text-truncate}

    [cangsheng45](https://my.csdn.net/cangsheng45){.user-name}：清楚详细

</div>

</div>

<div id="asideFooter">

<div class="aside-box">

<div id="kp_box_57" data-pid="57"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_57-707&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_57-707&quot;,&quot;con&quot;:&quot;,,&quot;}">

</div>

</div>

<div class="aside-box">

<div class="persion_article">

</div>

</div>

</div>

</div>

<div class="mask-dark">

</div>

<div class="super-private private-box">

<div class="private-title">

##### 私密 {#私密 .title}

<div class="private-close">

</div>

</div>

<div class="private-content">

[私密原因:]{.select-name}
<div class="select">

<div class="input-mod">

[请选择设置私密原因]{.select-active data-index=""}
<div class="select-button">

</div>

</div>

-   广告
-   抄袭
-   版权
-   政治
-   色情
-   无意义
-   其他

</div>

<div class="other">

[其他原因:]{.other-name}
<div class="textarea-box">

<div class="number">

120

</div>

</div>

</div>

</div>

<div class="private-footer">

<div class="private-close">

取消

</div>

<div class="private-send private-form no-active">

确定

</div>

</div>

</div>

<div class="private-error super-private">

<div class="private-title">

##### 出错啦 {#出错啦 .title}

<div class="private-close">

</div>

</div>

<div class="private-content">

系统繁忙，请稍后再试

</div>

<div class="private-footer">

<div class="private-close">

取消

</div>

<div class="private-send close-active">

确定

</div>

</div>

</div>

<div class="pulllog-box" style="display: block;">

<div class="pulllog clearfix">

[ ]{.text .float-left}
<div id="dmp_ad_69">

<div id="kp_box_69" data-pid="69"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_69-796&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_69-796&quot;,&quot;con&quot;:&quot;,,&quot;}">

<div
style="float:left;margin-right:5px;border:1px solid #f13d3d;padding:2px 5px 0px 5px;">

[2019人工智能薪资趋势](https://edu.csdn.net/topic/ai30?utm_source=ditong)

</div>

<div
style="float:left;margin-right:5px;border:1px solid #00BFFF;padding:2px 5px 0px 5px;background:#FFF0F5;">

[Python实战技巧](https://edu.csdn.net/topic/python115?utm_source=ditong)

</div>

<div
style="float:left;margin-right:5px;border:1px solid #f13d3d;padding:2px 5px 0px 5px;">

[数据库沙龙](https://t.csdnimg.cn/mWQl)

</div>

<div
style="float:left;margin-right:5px;border:1px solid #00BFFF;padding:2px 5px 0px 5px;background:#FFF0F5;">

[2018
年度课程榜单](https://gitbook.cn/gitchat/columns?tag=榜单&utm_source=wzl190104)

</div>

<div style="float:left;">

</div>

</div>

</div>

<div class="pulllog-btn float-right clearfix">

<div class="float-left csdn-tracking-statistics tracking-click"
data-mod="popu_557">

[登录]{.pulllog-login}

</div>

<div
class="pulllog-sigin float-left csdn-tracking-statistics tracking-click"
data-mod="popu_558">

[注册](https://passport.csdn.net/account/mobileregister)

</div>

</div>

</div>

</div>

<div id="loginWrap" style="display:none">

</div>

<div class="tool-box">

-   [ [点赞]{.no-active} [取消点赞]{.active} ]{.hover-show .text-box
    .text}

    0

-   [评论]{.hover-show .text}

-   <div id="liTocBox">

    </div>

    [目录]{.hover-show .text}
    <div class="toc-container">

    <div class="pos-box">

    <div class="icon-arrow">

    </div>

    <div class="scroll-box">

    <div class="toc-box">

    </div>

    </div>

    </div>

    <div class="opt-box">

    </div>

    </div>

-   [收藏]{.hover-show .text}
-   [](# "手机看"){.bds_weixin .clear-share-style}
    [ 手机看 ]{.hover-show .text .text3}
-   [上一篇]{.hover-show .text .text3}
-   [下一篇]{.hover-show .text .text3}
-   <div id="kp_box_73" data-pid="73"
    data-track-view="{&quot;mod&quot;:&quot;kp_popu_73-97&quot;,&quot;con&quot;:&quot;,,&quot;}"
    data-track-click="{&quot;mod&quot;:&quot;kp_popu_73-97&quot;,&quot;con&quot;:&quot;,,&quot;}">

    <div id="_360_interactive">

    </div>

    ![](//img-ads.csdn.net/2016/201608021757063065.png)

    </div>

-   [更多]{.hover-show .text}
    -   [上一篇]{.hover-show .text .text3}
    -   [下一篇]{.hover-show .text .text3}

</div>

<div class="fourth_column">

<div class="title-box">

**猿学习**

</div>

<div id="kp_box_456" data-pid="456"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_456-721&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_456-721&quot;,&quot;con&quot;:&quot;,,&quot;}">

[](https://edu.csdn.net/topic/python115?utm_source=blogright)
<div class="blogkp1">

![](http://img-ads.csdn.net/2018/201812181221437658.png){width="100"
height="100"}

</div>

<div id="kp_box_457" data-pid="457"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_457-681&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_457-681&quot;,&quot;con&quot;:&quot;,,&quot;}">

![](http://img-ads.csdn.net/2019/201901081453403307.jpg){width="100"
height="100"}

</div>

<div id="kp_box_458" data-pid="458"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_458-640&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_458-640&quot;,&quot;con&quot;:&quot;,,&quot;}">

[](https://gitchat.csdn.net/column/5a7d1a13a7f22b3dffca7e49?utm_source=csdn100)
<div class="blogkp3">

![](http://img-ads.csdn.net/2018/201811091452349556.png){width="100"
height="100"}
###### Python 爬虫和数据分析实战

[]{style="position:absolute;right:0;bottom:0;background:url(https://img-ads.csdn.net/2016/201608021757063065.png) no-repeat;width:33px;height:18px;display:block;z-index: 9999;"}

</div>

</div>

<div id="kp_box_459" data-pid="459"
data-track-view="{&quot;mod&quot;:&quot;kp_popu_459-687&quot;,&quot;con&quot;:&quot;,,&quot;}"
data-track-click="{&quot;mod&quot;:&quot;kp_popu_459-687&quot;,&quot;con&quot;:&quot;,,&quot;}">

![](http://img-ads.csdn.net/2018/201811231432284520.jpg){width="100"
height="100"}

</div>

</div>

</div>
