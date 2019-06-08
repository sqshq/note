---
title: MyBatis
---


#### 概述

> [MyBatis](http://www.mybatis.org/mybatis-3/zh/index.html)是一款优秀的持久层框架，它支持定制化SQL、存储过程以及高级映射。MyBatis避免了几乎所有的JDBC代码和手动设置参数以及获取结果集。MyBatis可以使用简单的XML或注解来配置和映射原生信息，将接口和Java的POJOs映射成数据库中的记录。

ORM: 对象关系映射(Object Relation Mapping)

* object: java中的实体内对象
* mapping：object和relation之间的映射
* relation: 数据库中的表

![orm 模型](figures/orm.png)

ORM模型可以用传统JDBC实现，但是传统JDBC程序的设计缺陷

* 大量配置信息硬编码：将数据库位置、密码等保存在代码中，违反软件开发的[OCP原则](../Java/Head First设计模式/3 Decorator Pattern.md#2-the-open-closed-principle)
* 大量的无关业务处理的编码：数据库连接的打开和关闭，sql语句的建立和发送
* 扩展优化极为不便：数据库连接池

适合于：

* 更加关注SQL优化的项目
* 需求频繁更新改动的项目

![mybatis_framework](figures/mybatis_framework.png)




####  案例：蛋糕网站


[项目地址](https://github.com/techlarry/Cake)

蛋糕网站使用MySQL数据库，首先建立名为cake的数据库以及名为cake的表。

```sql
mysql> create database cake default character set utf8;
Query OK, 1 row affected, 1 warning (0.17 sec)

mysql> use cake;
Database changed
mysql> create table cake
    -> (
    -> id bigint(20) not null auto_increment,
    -> category_id bigint(20) not null,
    -> name varchar(45) not null,
    -> level int(2) default null,
    -> price int(9) default null,
    -> small_img mediumblob,
    -> create_time datetime not null,
    -> update_time datetime not null,
    -> primary key (id)
    -> )
    -> engine=innodb auto_increment=1 default charset=utf8;
Query OK, 0 rows affected, 1 warning (0.21 sec)
mysql> create table category
    -> (
    -> id bigint(20) not null auto_increment,
    -> name varchar(45) not null,
    -> create_time datetime not null,
    -> update_time datetime not null,
    -> primary key (id)
    -> )
    -> engine=innodb auto_increment=1 default charset=utf8;
Query OK, 0 rows affected, 1 warning (0.11 sec)
```

类似于JDBCUtils，创建一个MyBatisUtils类

```java
public class MyBatisUtils {
    private static SqlSessionFactory sqlSessionFactory;
    private static Reader reader;
    static {
        try {
            String resource = "config.xml";
            reader = Resources.getResourceAsReader(resource);
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(reader);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static SqlSession openSession() {
        return sqlSessionFactory.openSession();
    }
}
```

创建Cake类，有Id, categoryId, name, price等属性。这里的重点是创建一个CakeMapper:


```java
public interface CakeMapper {

    /**
     * 分页查询蛋糕
     * @param skip  跳过的记录数，也就是从哪条开始查询
     * @param size  要查询的记录数
     * @return  蛋糕集合
     */
    @Select("select * from cake order by create_time desc limit #{skip}, #{size}")
    @Results({
                @Result(id = true, column = "id", property = "id"),
                @Result(column = "category_id", property = "categoryId"),
                @Result(column = "name", property = "name"),
                @Result(column = "level", property = "level"),
                @Result(column = "price", property = "price"),
                @Result(column = "create_time", property = "createTime"),
                @Result(column = "update_time", property = "updateTime")
            })
    List<Cake> getCakes(@Param("skip") Integer skip, @Param("size") Integer size);

    /**
     * 根据分类分页查询蛋糕
     * @param categoryId    蛋糕分类ID
     * @param skip  跳过的记录数，也就是从哪条开始查询
     * @param size  要查询的记录数
     * @return  蛋糕集合
     */
    @Select("select id, category_id categoryId, name, level, price, create_time createTime, update_time updateTime " +
            "from cake where category_id = #{categoryId} order by create_time desc limit #{skip}, #{size}")
    List<Cake> getCakesByCategoryId(@Param("categoryId")Long categoryId, @Param("skip") Integer skip,  @Param("size") Integer size);

    /**
     * 根据分类ID进行蛋糕数量的统计
     * @param categoryId    分类ID
     * @return  分类下蛋糕数量
     */
    @Select("select count(*) from cake where category_id = #{categoryId}")
    int countCakesByCategoryId(@Param("categoryId")Long categoryId);

    /**
     * 保存蛋糕信息
     * @param cake  蛋糕信息
     */
    @Insert("insert into cake(category_id, name, level, price, small_img, create_time, update_time) " +
            "value (#{cake.categoryId}, #{cake.name}, #{cake.level}, #{cake.price}, #{cake.smallImg}, " +
            "#{cake.createTime}, #{cake.updateTime})")
    void addCake(@Param("cake") Cake cake);

    /**
     * 查询蛋糕图片信息
     * @param id    蛋糕ID
     * @return  只包含图片的蛋糕实体
     */
    @Select("select small_img smallImg from cake where id = #{id} for update")
    Cake getImg(@Param("id")Long id);

}
```


#### XML映射文件

MyBatis的强大之处在于它的映射语句。SQL映射文件只有很少的几个顶级元素：

* `insert` – 映射插入语句
* `delete` – 映射删除语句
* `update` – 映射更新语句
* `select` – 映射查询语句
* `resultMap` – 是最复杂也是最强大的元素，用来描述如何从数据库结果集中来加载对象。
* `cache` – 对给定命名空间的缓存配置。
* `cache-ref` – 对其他命名空间缓存配置的引用。
* `sql` – 可被其他语句引用的可重用语句块。

[[详细用法](http://www.mybatis.org/mybatis-3/zh/sqlmap-xml.html)]