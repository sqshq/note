---
title: Maven
date: 2017-10-30
tags: [Java]
---

Maven is a build tool which automatically manages dependencies, source compilation, test compilation, and test execution.

### Compiling
#### Compiling with Maven from the Command Line

If you wish to compile the source using Maven from the command line, simply issue the following command from the command line from inside the root directory:

 ```bash
 $ mvn compile
 ```
 
#### Compiling with Maven from IntelliJ

[Maven-Intellij IDEA](https://www.jetbrains.com/help/idea/maven-support.html)

Go to `File > New > Project from Existing Sources...` and select the root directory. You should receive an "Import Project" prompt like the one shown below. Select the "Import project from external model" radio button, select "Maven" from the list below, and click through the following prompts to complete the import.

Open the Maven Projects pane by navigating to "View > Tool Windows > Maven Projects".

### POM配置
详见[POM Reference](https://maven.apache.org/pom.html)

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                      http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
 
  <!-- The Basics -->
  <groupId>...</groupId>
  <artifactId>...</artifactId>
  <version>...</version>
  <packaging>...</packaging>
  <dependencies>...</dependencies>
  <parent>...</parent>
  <dependencyManagement>...</dependencyManagement>
  <modules>...</modules>
  <properties>...</properties>
 
  <!-- Build Settings -->
  <build>...</build>
  <reporting>...</reporting>
 
  <!-- More Project Information -->
  <name>...</name>
  <description>...</description>
  <url>...</url>
  <inceptionYear>...</inceptionYear>
  <licenses>...</licenses>
  <organization>...</organization>
  <developers>...</developers>
  <contributors>...</contributors>
 
  <!-- Environment Settings -->
  <issueManagement>...</issueManagement>
  <ciManagement>...</ciManagement>
  <mailingLists>...</mailingLists>
  <scm>...</scm>
  <prerequisites>...</prerequisites>
  <repositories>...</repositories>
  <pluginRepositories>...</pluginRepositories>
  <distributionManagement>...</distributionManagement>
  <profiles>...</profiles>
</project>
```

#### 一个基本maven项目的pom.xml配置


第一部分,项目坐标，信息描述等

```xml
<modelVersion>4.0.0</modelVersion>
<groupId>com.company.project</groupId>
<artifactId>module</artifactId>
<packaging>war</packaging>
<version>0.0.1-SNAPSHOT</version>
<name>test Maven Webapp</name>
<url>http://maven.apache.org</url>
```

* modelVersion：pom文件的模型版本

关于group id和artifact id，为了便于多人多模块协同开发管理（以后会讲），建议使用以下命名规范

* group id：com.公司名.项目名
* artifact id：功能模块名

* packaging：项目打包的后缀，war是web项目发布用的，默认为jar
* version: artifact模块的版本
* name和url：相当于项目描述，可删除
* group id + artifact id +version :项目在仓库中的坐标


第二部分,引入jar包

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-csv</artifactId>
        <version>1.5</version>
    </dependency>
</dependencies>
```

上面引入了Apache commons csv项目，可以在[官网](http://commons.apache.org/proper/commons-csv)找到Maven设置。

* dependency：引入资源jar包到本地仓库，要引入更多资源就在<dependencies>中继续增加<dependency>
* group id+artifact id+version：资源jar包在仓库中的坐标
* scope：作用范围，test指该jar包仅在maven测试时使用，发布时会忽略这个包。需要发布的jar包可以忽略这一配置

第三部分,构建项目

```xml
<build>
	<finalName>helloworld</finalName>
	<plugins>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-compiler-plugin</artifactId>
			<version>3.5.1</version>
			<configuration>
				<source>1.7</source>
				<target>1.7</target>
			</configuration>
		</plugin>
		<plugin>
			<groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-resources-plugin</artifactId>
			<version>3.0.1</version>
			<configuration>
				<encoding>UTF-8</encoding>
			</configuration>
		</plugin>
	</plugins>
</build>
```

* build：项目构建时的配置
* finalName：在浏览器中的访问路径，如果将它改成helloworld，再执行maven--update，这时运行项目的访问路径是 http://localhost:8080/helloworld/, 而不是项目名的  http://localhost:8080/test
* plugins：插件，之前篇章已经说过，第一个插件是用来设置java版本为1.7，第二个插件是我刚加的，用来设置编码为utf-8
* group id+artifact id+version：插件在仓库中的坐标
* configuration：设置插件的参数值

