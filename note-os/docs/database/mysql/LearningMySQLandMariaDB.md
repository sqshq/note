### **Learning MySQL and MariaDB**


### 1 Introduction

MySQL is an open source, multithreaded, relational database management system.

Many features contribute to MySQL’s standing as a superb database system. Its **speed** is one of its most prominent features. MySQL and MariaDB are remarkably **scalable**, and are able to handle tens of thousands of tables and billions of rows of data.

### 2 Installing MySQL

You may visit [Official website](https://dev.mysql.com/downloads/mysql/) to download mysql community edition. Remember to choose <C>.dmg</C> package, which is easy to configure and start. To finish installation, set a password of your mysql server.  Don't forget to export mysql path to your bash configure file. 

To validate the completion of installation, just go to System Preferences and check whether the option of MySQL exists. 


#### Setting Initial Password for root

You can change the password for the root user in MySQL in a few ways. One way is to use the administration utility, <C>mysqladmin</C>. Enter the following from the command line:

```
mysqladmin -u root -p flush-privileges password "new_pwd"
```

### 3 The Basics and the mysql Client


#### The mysql Client

With the <C>mysql</C> client, you may interact with the MySQL or MariaDB server from the command line.


#### Connecting to the Server

Once you know your MySQL username and password, you can connect to the MySQL server with the <C>mysql</C> client.

```bash
mysql -u root -p
```

### 4 Creating Databases and Tables

#### Creating a Database

Use the SQL statement CREATE DATABASE.

```sql
create database database-name;
```

To validate your creation of the database, 

```sql
show databases;
```



To delete a database, using the SQL statement DROP DATABASE

```sql
drop database database-name;
```


### 13 Backing Up and Restoring Databases

#### Making Backups

If you have shell or telnet access to your web server, you can backup your MySQL data by using the <C>mysqldump</C> command. 

```bash
$ mysqldump --opt -u [uname] -p[pass] [dbname] > [backupfile.sql]
```

If you want to back up all the databases in the server at one time you should use the <C>--all-databases</C> option. It tells MySQL to dump all the databases it has in storage.

```bash
$ mysqldump -u root -p --all-databases > alldb_backup.sql
```

#### Restoring Backups

If data is lost in MySQL, but you’ve been using <C>mysqldump</C> to make regular backups of the data, you can use the dump files to restore the data.

```Java
mysql -u [uname] -p[pass] [db_to_restore] < [backupfile.sql]
```