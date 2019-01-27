---
title: MySQL
---

MySQL is an open source, multithread, relational database management system.


### 1 basics

#### client and server

The `server` maintains, controls and protects your data, storing it in files on the computer where the server is running in various formats. It listens for requests from `client`.

For MySQL, `mysqld`(the *d* stands for *daemon*) is the server. `mysql` is a standard MySQL client. With its text-based interface, a user can log in and execute SQL queries.

#### basic command

* The `mysql_safe` script is the most common way to start `mysqld`, because this script can restart the daemon if it crashes.
* The `mysqlaccess` tool creates user accounts and sets their privileges.
* The`mysqladmin` utility can be used to manage the database server itself from the command-line. 
* The `mysqlshow` tool may be used to examine a server’s status, as well as information about databases and tables.
* The `mysqldump` utility is the most popular one for exporting data and table structures to a plain-text file, known as a `dump` file. 
* The command `mysql -u root -p` is usually used to start the client `mysql`, after which the passport should be filled.
* The command `mysql -u root -p -e "SELECT User,Host FROM mysql.user;"` gives a list of username and host combination on the server.

#### GUI

[Sequel Pro](https://sequelpro.com) is a fast, easy-to-use Mac database management application for working with MySQL databases. see [detail in Chinese](https://segmentfault.com/a/1190000006255923)

[WorkBench](https://www.mysql.com/products/workbench) provides data modeling, SQL development, and comprehensive administration tools for server configuration, user administration, backup, and much more.

Although GUIs are easy-to-use, in the long run they're not useful. The text-based `mysql` client causes you to think and remember more, and it's not that difficult to use or confusing. And the command-line method of using `mysql` allows you to interact with the server without much overhead.


#### auto-completion and syntax highlighting

[Mycli](http://www.mycli.net) is a command-line interface which support MariaDB, MySQL with auto-completion and syntax highlighting.

![](figures/mycli.jpg)

### 2 SQL commands

Glossary of commonly used SQL commands:

`ALTER TABLE`

```SQL
ALTER TABLE table_name ADD column datatype;
```
**ALTER TABLE** lets you add columns to a table in a database.


`AND`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_1 = value_1
AND column_2 = value_2;
```
AND is an operator that combines two conditions. Both conditions must be true for the row to be included in the result set.


`AS`

```SQL
SELECT column_name AS 'Alias'
FROM table_name;
```
**AS** is a keyword in SQL that allows you to rename a column or table using an alias.

`AVG`

```SQL
SELECT AVG(column_name)
FROM table_name;
```
**AVG()** is an aggregate function that returns the average value for a numeric column.


`BETWEEN`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN value_1 AND value_2;
```
The BETWEEN operator is used to filter the result set within a certain range. The values can be numbers, text or dates.


`COUNT`

```SQL
SELECT COUNT(column_name)
FROM table_name;
```
**COUNT()** is a function that takes the name of a column as an argument and counts the number of rows where the column is not NULL.

`CREATE TABLE`

```SQL
CREATE TABLE table_name (column1 datatype, column2 datatype, column3 datatype);
```
**CREATE TABLE** creates a new table in the database. It allows you to specify the name of the table and the name of each column in the table.

`DELETE`

```SQL
DELETE FROM table_name WHERE some_column = some_value;
```
**DELETE** statements are used to remove rows from a table.


`GROUP BY`

```SQL
SELECT COUNT(*)
FROM table_name
GROUP BY column_name;
```
**GROUP BY** is a clause in SQL that is only used with aggregate functions. It is used in collaboration with the SELECT statement to arrange identical data into groups.


`INNER JOIN`

```SQL
SELECT column_name(s) FROM table_1
JOIN table_2
ON table_1.column_name = table_2.column_name;
```
An **inner join** will combine rows from different tables if the join condition is true.

`INSERT`

```SQL
INSERT INTO table_name (column_1, column_2, column_3) VALUES (value_1, value_2, value_3);
```
**INSERT** statements are used to add a new row to a table.


`LIKE`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern;
```
**LIKE** is a special operator used with the WHERE clause to search for a specific pattern in a column. SQL `pattern` matching enables you to use `_` to match any single character and `%` to match an arbitrary number of characters (including zero characters).


`LIMIT`

```SQL
SELECT column_name(s)
FROM table_name
LIMIT number;
```
**LIMIT** is a clause that lets you specify the maximum number of rows the result set will have.


`MAX`

```SQL
SELECT MAX(column_name)
FROM table_name;
```
**MAX()** is a function that takes the name of a column as an argument and returns the largest value in that column.


`MIN`

```SQL
SELECT MIN(column_name)
FROM table_name;
MIN() is a function that takes the name of a column as an argument and returns the smallest value in that column.
```

`OR`

```SQL
SELECT column_name
FROM table_name
WHERE column_name = value_1
OR column_name = value_2;
```
**OR** is an operator that filters the result set to only include rows where either condition is true.


`ORDER BY`

```SQL
SELECT column_name
FROM table_name
ORDER BY column_name1, column_name2 ASC|DESC;
```
**ORDER BY** is a clause that indicates you want to sort the result set by a particular column either alphabetically or numerically.


`OUTER JOIN`

```SQL
SELECT column_name(s) FROM table_1
LEFT JOIN table_2
ON table_1.column_name = table_2.column_name;
```
An **outer join** will combine rows from different tables even if the the join condition is not met. Every row in the left table is returned in the result set, and if the join condition is not met, then NULL values are used to fill in the columns from the right table.


`ROUND`

```SQL
SELECT ROUND(column_name, integer)
FROM table_name;
```
**ROUND()** is a function that takes a column name and an integer as an argument. It rounds the values in the column to the number of decimal places specified by the integer.


`SELECT`

```SQL
SELECT column_name FROM table_name;
```
**SELECT** statements are used to fetch data from a database. Every query will begin with SELECT.

`SELECT DISTINCT`

```SQL
SELECT DISTINCT column_name FROM table_name;
```
**SELECT DISTINCT** specifies that the statement is going to be a query that returns unique values in the specified column(s).


`SUM`

```SQL
SELECT SUM(column_name)
FROM table_name;
```
**SUM()** is a function that takes the name of a column as an argument and returns the sum of all the values in that column.


`UPDATE`

```SQL
UPDATE table_name
SET some_column = some_value
WHERE some_column = some_value;
```
**UPDATE** statments allow you to edit rows in a table.


`WHERE`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_name operator value;
```
**WHERE** is a clause that indicates you want to filter the result set to include only rows where the following condition is true. eg. `SELECT * FROM customers WHERE ID=7`;

#### SQL Operators

Comparison Operators and Logical Operators are used in the `WHERE` clause to filter the data to be selected.

**Comparison Operators**

The following comparison operators can be used in the `WHERE` clause:


| Operator | Description |
| --- | --- |
| = | Equal |
| != | Not equal  |
| > | Greater than  |
| < | Less than   |
| >= | Greater than or equal  |
| <= | Less than or equal |
| BETWEEN | Between an inclusive range |

`BETWEEN` Operator:

```SQL
SELECT * FROM customers
WHERE ID BETWEEN 3 AND 7;
```

**Logical Operators**

Logical operators can be used to combine two Boolean values and return a result of **true**, **false**, or **null**.

The following operators exists in SQL:

| Operator | Description |
| --- | --- |
| AND | TRUE if both expressions are TRUE |
| OR | TRUE if either expression is TRUE |
| IN | TRUE if the operand is equal to one of a list of expressions |
| NOT | Returns TRUE if expression is not TRUE  |



The `IN` Operator:

```SQL
SELECT * FROM customers 
WHERE City IN ('New York', 'Los Angeles', 'Chicago');
```

The `NOT IN` Operator:

```SQL
SELECT * FROM customers 
WHERE City NOT IN ('New York', 'Los Angeles', 'Chicago');
```

#### Functions

The `UPPER` function converts all letters in the specified string to uppercase. 
The `LOWER` function converts the string to lowercase.

The following SQL query selects all *Lastnames* as uppercase:

```SQL
SELECT FirstName, UPPER(LastName) AS LastName 
FROM employees;
```

The `SQRT` function returns the square root of given value in the argument.
Similarly, the `AVG` function returns the average value of a numeric column.
The `SUM` function is used to calculate the sum for a column's values.

The `MIN` function is used to return the minimum value of an expression in a `SELECT` statement.

E.g. you might wish to know the minimum salary among the employees:

```SQL
SELECT MIN(salary) AS Salary FROM employees;
```

#### Subqueires

A subquery is a query within another query. Enclose the subquery in parentheses. 

E.g.

```SQL
SELECT FirstName, Salary FROM employees 
WHERE  Salary > (SELECT AVG(Salary) FROM employees) 
ORDER BY Salary DESC;
```

#### Joining Tables

SQL can combine data from multiple tables. In SQL, 'joining tables' means combining data from two or more tables. A table join creates a `temporary table` showing the data from the joined tables.

To join tables, specify them as a comma-separated list in the `FROM` clause:

```SQL
SELECT customers.ID, customers.Name, orders.Name, orders.Amount FROM customers, orders
WHERE customers.ID = orders.Customer_ID
ORDER BY customers.ID
```

**Types of Join**


The following are types of `JOIN` that can be used in SQL:

* `INNER JOIN`: returns rows when there is a match between the tables.
* `LEFT JOIN`: returns rows from the left table, even if there are no matches in the right table.

```SQL
SELECT table1.column1, table2.column2...
FROM table1 LEFT JOIN table2
ON table1.column_name = table2.column_name;
```
If no match is found for a particular row,`NULL `is returned.

* `RIGHT JOIN`
Just like `LEFT JOIN`

#### Backing up and Restoring

**Backing up**

```bash
mysqldump -u user -p database_name > /data/backups/all-dbs.sql
```
**Restoring**

```bash
mysql -u user -p < all-dbs.sql
```


### 3 MySQL架构

#### MySQL逻辑架构

![](figures/mysql_server.jpg)

* Connectors：用不同的客户端程序连接MySQL需要用的到驱动程序
* Management Services&Utilities：系统管理和控制工具
    * 备份和恢复的安全性，复制，集群，管理，配置，迁移和元数据。
* Connection Pool：连接池
    * 进行身份验证、线程重用，连接限制，检查内存，数据缓存；管理用户的连接，线程处理等需要缓存的需求
* SQL Interface(SQL接口)
    * 进行 DML、DDL，存储过程、视图、触发器等操作和管理；用户通过SQL命令来查询所需结果。
* Parser(解析器)
    * 查询翻译对象的特权；SQL命令传递到解析器的时候会被解析器验证和解析。
* Optimizer(查询优化器)：重写查询、决定表的读取顺序，以及选择合适的索引等。
* Caches & Buffers(查询缓存)：存储查询结果
* Plugin Storage Engine(插件式存储引擎)： 存储引擎负责MySQL中数据的存储和提取。

#### 并发控制

在处理并发读或者写时，可以通过实现一个由两种类型的锁组成的锁系统来解决问题，通常被称为共享锁(shared lock)或排他锁(exclusive lock)，也叫做读锁(read lock)和写锁(write lock)。

一种提高共享资源并发性的方式就是让锁定对象更有选择性。尽量只锁定需要修改的部分数据，而不是所有的资源。问题是加锁也需要消耗资源：获得锁、检查锁是否已经解除、释放锁等，都会增加系统的开销。

所谓的锁策略就是在锁的开销和数据的安全性之间寻求平衡。每种MySQL存储引擎都可以实现自己的锁策略和锁力度。

* 表锁(table lock): 最基本的锁策略，并且是开销最小的策略。会锁定整张表。对表进行写操作时，需要先获得写锁。读锁之间是不相互阻塞的。
* 行级锁(row lock): 最大程度地支持并发处理，同时也带来了最大的锁开销。在InnoDB和XtraDB等中实现了行级锁。

#### 事务

**事务**(transaction)是数据库应用中完成单一逻辑功能的操作集合。关系型数据库的事务具有ACID特性，即**原子性**(Atomicity)，**一致性**(Consistency)，**隔离性**(Isolation)，**持久性**(Durability)。

![](figures/ACID.jpg)

**原子性**

事务的**原子性**是指事务是一个**不可再分割的工作单元**，事务中的操作要么都执行，要么都不执行，不可能只执行其中的一部分。

例如资金从账户A转账到账户B时，需要在账户A中进行取出操作，在账户B中进行存入操作。这两个操作必须保证要么都发生要么都不发生。

    
**一致性**
    
事务的**一致性**是指事务执行之前和之后，数据库的完整性约束没有被破坏。例如资金转账前后，账户A和B的余额之和应该是保持不变的。

**隔离性**

事务的**隔离性**是指一个事务所做的修改在最终提交以前，对其他事务是不可见的。


SQL标准中定义了四种隔离级别，每一种级别都规定了一个事务中所做的修改，哪些在事务内和事务间是可见的，哪些是不可见的。较低级别的隔离通常可以执行更高的并发，系统的开销也更低。

* **未提交读**(READ UNCOMMITTED): 事务中的修改，即使没有提交，对其他事务也都是可见的。事务可以读取未提交的数据，这也被称为脏读(dirty read)。在实际应用中一般很少使用。
* **提交读**(READ COMMITTED): 一个事务从开始知道提交之前，所做的任何修改对其他事务都是不可见的。也叫做不可重复读，因为执行两次同样查询，可能得到不一样的结果。
* **可重复读**(REPEATABLE READ): 在同一个事务中多次读取同样记录的结果是一致的。但无法解决幻读(phantom read)的问题: 当某个事务在读取某个范围内的记录时，另外⼀个事务又在该范围内插⼊了新的记录，当之前的事务再次读取该范围的记录时，会产⽣幻⾏。
* **序列化读**(SERIAZABLE)：所有的事务操作都必须串行操作。这种隔离级别最高，但是牺牲了系统的并发性。简单来说，序列化会在读取的每一行数据上都加锁，所以可能导致大量的超时和锁争用的问题。




MySQL默认的事务隔离级别是可重复读。设置MySQL事务隔离级别:

```sql
SET session transaction_isolation='read-committed'
```

**持久性**

事务的**持久性**是指事务执行完成后，该事务对数据库的更改就会永久保存到数据库中。例如当资金转账成功后，即使发生系统故障，账户A、B的余额也应该保持转账成功结束后的新值。 

MySQL默认采用自动提交(AUTOCOMMIT)模式, 即如果不是显式地开始一个事务，则每个查询都被当作一个事务执行提交操作。

MySQL服务器层不管理事务，事务是由下层的存储引擎实现的，所以在同一个事务中，使用多种存储引擎是不可靠的。如果混合使用了事务型和非事务型的表(InnoDB和MyISAM表)，该事务需要回滚，非事务型的表上的变更就无法撤销，这会导致数据库处于不一致的状态。



为了解决**死锁**问题，数据库系统实现了各种死锁检测和死锁超时机制。越复杂的系统，比如InnoDB存储引擎，越能检测到死锁的循环依赖，并立即返回一个错误。或者当查询的时间达到锁等待超时的设定后放弃锁请求，但通常不大友好。InnoDB处理死锁的方式是，将持有最少行级排他锁的事务进行回滚。

InnoDB采用的是**两阶段锁定协议**(two-phase locking protocol)。在事务执行过程中，随时都可以执行锁定，锁只有在执行COMMIT或者ROLLBACK时才被释放，并且所有的锁都是在同一时刻被释放。


#### 多版本并发控制

MySQL的大多数事务型存储引擎实现的都不是简单的行级锁。基于提升并发性能的考虑，它们一般都同时实现了**多版本并发控制**(MVCC)。可以认为MVCC是行级锁的一个变种，但是它在很多情况下必买你了加锁操作，因此开销更低。MVCC的实现，是通过保存数据在某个时间点的快照开实现的。也就是说，不管需要执行多长时间，每个事务看到的数据都是一致的。

InnoDB的MVCC是通过在每行记录后面保存两个隐藏的列来实现的。这两个列，一个保存了行的创建时间，一个保存行的过期时间或删除时间。存储的不是实际的时间值，而是系统版本号(system version number)。每开始一个新事务，系统版本号都会自动自增，事务开始时刻的系统版本号会作为事务的版本号，用来和查询到的每行记录的版本号进行比较。

在进行SELECT操作时，InnoDB只查找版本早于当前事务版本的数据行，这样可以确保事务读取的行，要么是在事务开始前已经存在的，要么是事务自身插入或者修改过的。并且行的删除版本要么为定义，要么大雨当前事务版本号，这样可以确保事务读取到的行，在事务之前未被删除。只有符合上述条件的记录，才能返回作为查询结果。这样保存这两个额外系统版本号，使⼤多数读操作都可以不⽤加锁。



#### 存储引擎


可以使用 `SHOW TABLE STATUS ` 命令显示表的信息，包括存储引擎类型。

```sql
mysql root@localhost:rookery> show table status\G
***************************[ 1. row ]***************************
Name            | bird_families
Engine          | InnoDB
Version         | 10
Row_format      | Dynamic
Rows            | 12
Avg_row_length  | 1365
Data_length     | 16384
Max_data_length | 0
Index_length    | 16384
Data_free       | 0
Auto_increment  | 113
Create_time     | 2017-08-11 00:18:18
Update_time     | 2017-08-12 13:11:47
Check_time      | <null>
Collation       | latin1_bin
Checksum        | <null>
Create_options  |
Comment         |
```

MySQL的一大特定是插件式存储引擎(Pluggable Storage Engine)。

##### InnoDB

`InnoDB`是MySQL默认的事务存储引擎，并且是最重要和使用最广泛的存储引擎。*除非有令人信服的需求去使用不同的引擎，否则应该使用InnoDB引擎。

InnoBD引擎被设计用来处理大量的短期(short-lived)事务，短期事务大部分情况是正常提交的，很少会被回滚。

InnoDB采⽤MVCC来⽀持⾼并发，并且实现了四个标准的隔离级别。 其默认级别是可重复读，并且通过间隙锁(next-key locking)策略防⽌幻读的出现。间隙锁使得InnoDB不仅仅锁定查询涉及的⾏，还会对索引中的间隙进⾏锁定，以防⽌幻影⾏的插⼊。

#### MyISAM存储引擎

MyISAM提供了⼤量的特性，包括全⽂索引、压缩、空间函数（GIS）等，但MyISAM不⽀持事务和⾏级锁，⽽且有⼀个毫⽆疑问的缺陷就是崩溃后⽆法安全恢复。


### 参考

1. 高性能MySQL
2. 
