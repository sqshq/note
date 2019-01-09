---
title: Head First Servlets and JSP
---


### 1 前言


#### HTML速成指南

详见[HTML5参考手册](http://www.w3school.com.cn/html5/html5_reference.asp)

| 标记 |  描述 |
| --- | --- |
| `<!-- -->` | 在这里加注释 |
| `<a>` | 通常用来放一个超链接 |
| `<align>` | 对内容左对齐、右对齐、居中，或调整行距 |
| `<body>` | 定义文本体的边界 |
| `<br>` | 行分隔 |
| `<center>` | 将内容居中 |
| `<form>` | 定义一个表单 |
| `<h1>` | 一级标题 |
| `<head>` | 定义文档首部的边界 | 
| `<html>` | 定义HTML文档的边界 |
| `<input type>` | 在表单中定义一个输入组件 |
| `<p>` | 一个新段落 |
| `<title>` | HTML文档的标题 | 


#### 单靠Web服务器


如果需要动态页面，而且希望能够把数据保存到服务器上，只依靠Web服务器是不够的。Web服务器应用只提供静态页面。需要CGI或者Servlet这样的辅助应用生成非静态的即时页面，而且能够与Web服务器通信。

也就是说即时页面在请求到来之前并不存在，请求到来后，辅助应用写出HTML，Web服务器再把这个HTML交回给客户。

### 2 Web应用体系结构

Servlet没有`main()`方法。它们受控于另一个Java应用，这个Java应用称为容器(如[Tomcat](http://tomcat.apache.org) )。如果Web服务器应用(如Apache)得到一个指向某servlet的请求，此时服务器不是把请求交给servlet本身，而是交给部署该servlet的容器。要由容器向servlet提供HTTP请求和响应，而且要由容器调用servlet的方法(如`doPost`/`doGet`)。

![servlet_need_a_containe](figures/servlet_need_a_container.png)

容器能提供什么？

* 通信支持：无需建立ServerSocket、监听端口、创建流，就能轻松让servlet与Web服务器对话。
* 生命周期管理：容器控制servlet的生与死，负责加载类、实例化和初始化servlet、调用servlet方法。
* 多线程支持：自动为每个servlet请求创建一个新线程。
* 声明方式实现安全：可以使用XML部署描述文件来配置安全性，而不必将其硬编码写到servlet或其他类代码中。也就是说不用修改Java源文件、不用重新编译就能管理和修改配置。
* JSP支持：负责把JSP代码翻译成Java代码。


#### 部署描述文件

部署描述文件(DD，一般为`web.xml`)可以将URL映射到servlet。

```xml
<servlet>  // 将内部名映射到完全限定类名
    <servlet-name>HelloWorld</servlet-name>
    <servlet-class>com.headfirstservletsjsp.servlet.HelloWorld</servlet-class>
</servlet>

<servlet-mapping> // 将内部名映射到公共URL名
    <servlet-name>HelloWorld</servlet-name>
    <url-pattern>/hello</url-pattern>  // 公共URL名，客户看到的
</servlet-mapping>
```

部署描述文件有以下优点：

* 尽量少改动已经测试过的源代码
* 即使你手上并没有源代码，也可以对应用的工程进行调整
* 不用重新编译和测试任何代码，也可以让应用适用不同的资源(如数据库)
* 可以更容易地维护动态安全信息，如访问控制列表和安全角色



### 3 MVC模式

MVC即**模型-视图-控制器**(model-view-controller)模式。MVC就是把业务逻辑从servlet中抽出来，把它放在一个模型中。所谓模型就是一个可重用的普通Java类，是业务数据和处理该数据的方法的组合。

![mv](figures/mvc.png)


* 控制器(Controller) - 负责转发请求，对请求进行处理。
* 视图(View) - 界面设计人员进行图形界面设计。
* 模型(Model) - 程序员编写程序应有的功能（实现算法等等）、数据库专家进行数据管理和数据库设计(可以实现具体的功能)。




### 4 Servlet请求和响应

#### 生命周期

![servlet_life](figures/servlet_life.png)


Servlet生命周期中重要时刻

| 时刻 | 何时调用  | 作用 | 是否覆盖 |
| --- | --- | --- | --- |
| `init()` | servlet实例创建后，并在servlet能为客户请求提供服务之前，容器要对servlet调用`init()` | 使你在servlet处理客户请求之前有机会对其初始化 | 有可能。如果有初始化代码(如得到一个数据库连接，或向其他对象注册)，就要覆盖servlet类中的`init()方法`。|
| `service()` | 第一个客户请求到来时，容器会开始一个新线程，并调用servlet的`service()`方法 | 查看请求，确定HTTP方法(GET, POST等), 并在servlet上调用对应的方法。 | 不应该覆盖`service()`方法 |
| `doGet()`/`doPost()` | `service()`方法根据请求的HTTP方法来调用`doGet()`或`doPost()` | 你的Web应用想要做什么，就要由这个方法负责 | 至少要覆盖其中之一 |
| `destroy()` | 需要释放内存或者容器关闭时 | 关闭数据库连接、停止后台线程等 | 一般不覆盖  |

第一个客户请求到来时，容器会开始一个线程，并调用servlet的`service()`方法。后续客户请求到来时，容器再创建或找到另一个线程，并调用servlet的`service()`方法。也就是**容器运行多个线程来处理对一个servlet的多个请求**。

![servlet_threads](figures/servlet_threads.png)

#### 加载和初始化

容器找到servlet类文件时，servlet的生命周期开始。这基本上都是在容器启动时发生(例如，运行Tomcat时)。容器启动时，它会寻找已经部署的Web应用，然后开始搜索servlet类文件。加载类可能在容器启动时发生，也可能在第一个客户使用时进行。

**`init()`总是在第一个`service()`调用之前完成**。

servlet初始化后产生`ServletConfig`对象和`ServletContext`对象：

* `ServletConfig`对象
    * 每个servlet都有一个`ServletConfig`对象
    * 用于向servlet传递部署时信息，当你不想把这个信息硬编码到servlet中(servlet初始化参数），如数据库名
    * 用于访问`ServletContext`
    * 参数在部署描述文件中配置
* `ServletContext`对象
    * 每个Web应用有一个`ServletContext`
    * 用于访问Web应用参数 
    
#### 请求
    
GET请求本质上讲是幂等的。它们应当能多次运行而不会对服务器产生任何副作用。GET请求不应该修改服务器上的任何东西。

POST本质上讲不是幂等的，所以要适当地设计和编写代码，如果客户错误地把一个请求发送了两次，应该能正确地加以处理。

简单的超链接往往意味着GET请求：

```html
<a href="http://baidu.com"> click here </a>
```

如果在表单中明确说`method="POST"`，那么毫无疑问这就是一个POST请求。如果在表单`<form>`中没有说`method="POST"`，就会默认为GET请求。

```html
<form method="POST" action=SelectBeer.do">
```

`request.getParameter(parameterName)`返回单个参数，返回值总是个String。如果对应一个给定的参数名有多个参数值，要使用`request.getParameterValues(parameterName)`方法来返回一个String数组。

从请求对象还可以得到其他东西，包括首部、cookie、会话、查询串和输入流：

| 方法 | 详细信息 |
| --- | --- |
| `request.getHeader("User-Agent")` | 客户的平台和浏览器信息 |
| `request.getCookies()` | 与请求相关的cookie |
| `request.getSession()` | 与客户相关的会话session |

    
#### 响应

`javax.servlet.ServletResponse`接口示意：

![servlet_response](figures/servletResponse.png)

大多数情况下，使用响应只是为了向客户发送数据，会对响应response调用两个方法：`setContentType()`和`getWriter()`。在此之后，只需要完成I/O即可。

`setContentType()`设置了HTTP首部中的内容类型：告诉了浏览器返回类型，浏览器会采取相应的操作：例如，打开PDF阅读器或者视频播放器，或者呈现HTML，又或者把响应的字节保存为一个下载文件。

`ServletResponse`接口提供了两个流用于输出：`ServletOutputStream`用于输出字节, `PrintWriter`用于输出字符数据。

```Java
// 把文本数据打印到一个字符流
PrintWriter writer = response.getWriter();
writer.println("some text and HTML");

// 写其他的任何内容
ServletOutputStream out = response.getOutputStream();
out.write(aByteArray);
```

重定向：当确定无法完成工作以后，servlet可以调用重定向方法`sendRedirect()`:

```Java
if (worksForMe) {
    // handle the request
} else {
    response.sendRedirect("http://www.oreilly.com");
}
```

请求分派：当servlet讲请求该给Web应用的另一部分(例如，JSP)。

```Java
RequestDispatcher view = 
    request.getRequestDispatcher("result.jsp")
view.forward(request, response);
```

请求分派(详见下一章)在服务器端发生，而重定向在客户端进行。请求分派把请求传递给服务器上的另一个组件(通常在同一个Web应用中)。请求重定向只是告诉浏览器去访问另一个URL。


### 5 Servlet属性和监听者

#### 初始化参数

servlet不仅可以把请求参数传递给`doGet()`或者`doPost()`，而且还可以有初始化参数。


在部署描述文件(web.xml)中给定一个参数名(param-name)和一个参数值(param-value)。

```xml
<init-param>
    <param-name>adminEmail</param-name>
    <param-value>likewecare@wickedljdsf.com</param-value>
</init-param>
```
在servlet中，使用getServletConfig返回ServletConfig，通过getInitParameter获取参数。

```java
out.println(getServletConfig().getInitParameter("adminEmail"));
```

容器初始化一个servlet时，会为这个servlet建一个唯一的`ServletConfig`，容器从部署配置文件读出servlet初始化参数，并把这些参数交给`ServletConfig`,然后把`ServletConfig`传递给servlet的`init()`方法。

容器建立一个servlet时，它会读取部署配置文件，并为`ServletConfig`创建名/值对。此后容器不会再读初始化参数。一旦参数置于`ServletConfig`中，就不会再读了，除非你重新部署servlet。

!!! question
    如果修改XML来改变一个初始化参数的值，servlet或Web应用的其余部分什么时候能看到这个改变呢？
    
    只有当Web应用重新部署时才会看到。servlet只会初始化一次，就是在它生命刚开始时初始化，也正是在这个时候会为它提供`ServletConfig`和`ServletContext`。

![servlet_init_paramete](figures/servlet_init_parameter.png)

上下文初始化参数context-param与servlet初始化参数init-param很类似，只不过上下文参数对整个Web应用可用，而不只针对一个servlet。所有servlet都可以访问上下文初始化参数，而且如果值有变化，只需在一个地方修改就行了。



```xml tab="配置文件"
<context-param>
    <param-name>adminEmail</param-name>
    <param-value>likewecare@wickedljdsf.com</param-value>
</context-param>
```

```Java tab="Servlet代码"
out.println(getServletContext().getInitParameter("adminEmail");
```

**每个servlet有一个ServletConfig，每个Web应用有一个ServletContext**。

![servlet_context_config](figures/servlet_context_config.png)

servlet初始化参数和上下文初始化参数之间的区别：

| 类别  | 上下文初始化参数 | Servlet初始化参数 |
| --- | --- | --- | 
| 部署描述文件 | 在`<web-app>`元素中，但是不在具体的<servlet>元素内: `<context-param>` | 在每个特定servlet的`<servlet>`元素中: `<init-param>` |
| Servlet代码 | getServlet<span style="color:red">Context</span>().getInitParameter("foo"); | getServlet<span style="color:red">Config()</span>.getInitParameter("foo") |
| 可用性 | 对Web应用中的所有servlet和JSP都可用 | 只对配置了`<init-param>`的相应servlet可用  | 

#### ServletContext

ServletContext是JSP或servlet与容器及其Web应用其他部分的一个连接。

![ServletContext_API](figures/ServletContext_API.png)

!!! note "两种方式得到ServletContext"
    
    servlet的`ServletConfig`对象拥有该servlet的`ServletContext`的一个引用。所以可以用以下方式获取: `getServletConfig().getServletContext()`

#### 监听者

如果希望应用初始化参数是一个数据库DataSource呢？

我们需要监听一个上下文初始化事件，这样就能得到上下文初始化参数，并在应用为客户提供服务之前运行一些代码。所以需要一个单独的对象，它能做到：

* 上下文初始化(应用正在得到部署)时得到通知
    * 从ServletContext得到上下文初始化参数
    * 使用初始化参数查找名建立一个数据库连接
    * 把数据库连接存储为一个属性，使得Web应用的各个部分都能访问
* 上下文撤销(应用取消部署或结束)时得到通知
    * 关闭数据库连接  


![servletContextListene](figures/servletContextListener.png)

如何告诉容器已经为应用建立了一个监听者? 也就是说如何注册监听者？在部署描述文件中使用`<listener>`元素：

```xml
<listener>
    <listener-class> </listener-class>
</listener>
```

!!! example "一个简单的ServletContextListener"
    
    下面这个例子中，把String初始化参数转化为一个真正的对象——一个`Dog`。监听者的任务是得到有关狗的品种的上下文初始化参数，然后使用这个String来构造一个`Dog`对象。监听者再把这个`Dog`对象放到一个`ServletContext`属性中，以便servlet获取。
        
    `Dog` 例子：
        
    * 监听者对象向`ServletContextEvent`对象请求`ServletContext`对象的一个引用。
    * 监听者使用这个`ServletContext`引用得到“breed”的上下文初始化参数，这是一个String，表示狗的品种。
    * 监听者使用这个狗品种String构造一个`Dog`对象。
    * 监听者使用`ServletContext`引用在`ServletContext`中设置Dog属性。
    * 这个Web应用的测试servlet从`ServletContext`得到`Dog`对象，并调用这个`Dog`的`getBreed()`方法。
    
    一个需要三个类和一个部署描述文件：
        
    * `MyServletContextListener`实现了`ServletContextListener`，它得到上下文初始化参数，创建`Dog`，并把`Dog`设置为上下文属性；
    * `Dog`类由`MyServletContextListener`实例化，并设置在`ServletContext`中，以便servlet获取；
    * `ListenerTester`扩展了`HttpServlet`，它验证监听者，从上下文得到`Dog`属性，然后调用`Dog`的`getBreed()`，并把结果打印到响应。
    
    ```Java tab="Dog"
    public class Dog implements Serializable {
        private String breed;
        public Dog(String breed) {
            this.breed = breed;
        }
        
        public String getBreed() {
            return breed;
        }
        
        public String toString() {
            return String.format("A %s Dog.", breed);
        }
    }
    ```
    
    ```Java tab="ListenerTester"
    public class ListenerTester extends HttpServlet {
        protected void doGet(HttpServletRequest request, 
                HttpServletResponse response)
                throws ServletException, IOException {
            response.setContentType("text/html");
            ServletContext sc = getServletContext();
            Dog dog = (Dog) sc.getAttribute("dog");
            System.out.println(dog);
            PrintWriter out = response.getWriter();
            out.println(dog.getBreed());
        }
    }
    ```
        
    ```Java tab="MyServletContextListener"
    public class MyServletContextListener implements ServletContextListener {
        public void contextInitialized(ServletContextEvent sce) {
           ServletContext sc  = sce.getServletContext();
           String breedOfDog = sc.getInitParameter("breed");
           Dog dog = new Dog(breedOfDog);
           sc.setAttribute("dog", dog);
        }
        public void contextDestroyed(ServletContextEvent sce) {
            //do nothing here
        }
    }
    ```
    
    ```xml tab="web.xml"
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app 省略>
        
        <servlet>
            <servlet-name>testListener</servlet-name>
            <servlet-class>com.headfirstservletsjsp.servlet.ListenerTester</servlet-class>
        </servlet>
        
        <servlet-mapping>
            <servlet-name>testListener</servlet-name>
            <url-pattern>/testListener</url-pattern>
        </servlet-mapping>
        
        <listener>
            <listener-class>com.headfirstservletsjsp.servlet.MyServletContextListener</listener-class>
        </listener>
        
        <context-param>
            <param-name>breed</param-name>
            <param-value>incredibleDog</param-value>
        </context-param>
    </web-app>
    ```
    
    
常见的监听者


| 场景 | 监听者接口 | 时间类型 |
| --- | --- | --- |
| 你想知道一个Web应用上下文中是否增加、删除或替换了一个属性 | `ServletContextAttributeListener` | `ServletContextAttributeEvent` |
| 你想知道有多少个并发用户。也就是说，你想跟踪活动的会话 | `HttpSessionListener` | `HttpSessionEvent` |
| 每次请求到来时你都想知道，以便建立日志记录 | `ServletRequestListener` | `ServletRequestEvent` |
| 增加、删除或替换一个请求属性时你希望能够知道 | `ServletRequestAttributeListener` | `ServletRequestAttributeEvent` |
| 你有一个属性类(这个类表示的对象放在一个属性中)，而且你希望这个类型的对象在绑定到一个会话或从会话删除时得到通知 | `HttpSessionBindingListener` | `HttpSessionBindingEvent` |
| 增加、删除或替换一个会话属性时你希望能够知道 | `HttpSessionAttributeListener` | `HttpSessionBindingEvent` |
| 你想知道是否创建或撤销了一个上下文 | `ServletContextListener` | `ServletContextEvent` |
| 你哟一个属性类，而且希望这个类型的对象在其绑定的会话迁移到另一个JMV时得到通知 | `HttpSessionActivationListener` | `HttpSessionEvent` |

#### 属性

属性就是一个对象(例如上面例子中的dog对象)，可以设置到`ServletContext`, `HttpServletRequest`, `HttpSession`中，可以把它简单地认为是一个映射实例对象中的名/值对(name/value pair)。在实际中，我们并不知道也不关心它具体如何实现，我们关心的是属性所在的作用域：谁能看到这个属性，以及属性能存活多久。

!!! note "属性v.s.参数"
    
    |     | 属性 | 参数 |
    | --- | --- | --- |
    | 类型 | 上下文(Context)、请求(Request)、会话(Sesssion) | 应用/上下文初始化参数、请求参数、Servlet初始化参数 |
    | 设置方法 | `setAttribute(String name, Object value)` | 不能设置应用和Servlet初始化参数，只能在部署配置文件中设置 |
    | 返回类型 | `Object` | `String` |
    | 获取方法 | `getAttribute(String name)` | `getInitParameter(String name)` |


属性的三个作用域: 上下文、请求和会话，分别由`ServletContext`、`ServletRequest`和`HttpSession`接口处理。每个接口中对应属性的API完全相同：`getAttribute()`, `setAttribute()`, `removeAttribute()`, `getAttributeNames()`。

![three_attribute_scopes](figures/three_attribute_scopes.png)

#### 属性和线程安全

**上下文作用域不是线程安全的！**：应用中的每一部分都能访问上下文属性，所以可能有多个servlet，也就是说有多个线程

![context_scopte_is_not_thread_safe](figures/context_scopte_is_not_thread_safe.png)

那么怎么解决呢？

同步`doGet()`等服务方法：同步服务方法可以防止同一个servlet中的其他线程访问上下文属性，但是不能阻止另外一个不同servlet的访问。例如上图中，如果线程A正在访问上下文属性，而且同步了服务方法，那么线程C不可以访问，但是线程B可以访问。

所以正确的方法不是对servlet加锁，而是需要对上下文加锁。

```java
public void doGet(HttpServletRequest request, HttpServletResponse response)
                        throws IOException, ServletException {
    response.setContextType("text/html");
    PrintWriter out = response.getWriter();
    synchronized(getServletContext()) { // 同步块：得到上下文锁
        getServletContext().setAttribute("foo", "42");
        out.println(getServletContext.getAttribute("foo"));
    }
}
```

那么会话属性是线程安全的吗？也不是，因为客户可能打开一个浏览器窗口。所以和上面的方法类似，要将`HttpSession`对象进行同步。

只有请求属性和局部变量是线程安全的。

实例变量也不是线程安全的。因为可以有多个客户对一个servlet作出请求，这意味着有多个线程在运行该servlet代码，而且所有线程都能访问servlet的实例变量。

!!! Summary "线程不安全的划上对勾"

    * [x] 上下文作用域属性
    * [x] 会话作用域属性
    * [ ] 请求作用域属性
    * [x] servlet中的实例变量
    * [ ] 服务方法中的局部变量
    * [x] servlet中的静态变量





### 6 会话管理

#### cookie

如何能跨多个请求保留客户特定的状态？使用`HttpSession`: `HttpSession`兑现给可以保存跨同一个客户<font color="red">多个</font>请求的会话状态。换句话说，与一个特定客户的整个会话期间，HttpSession会持久存储。

容器怎么知道客户是谁？通过cookie作为唯一的会话ID。具体请参见[计算机网络：自顶向下](../../OS/计算机网络 自顶向下/2 应用层.md#cookies)。

容器几乎做了关于cookie的所有工作：

* 对于一个新会话，容器会生成会话ID、创建新的cookie对象、把会话ID放到cookie中、把cookie设置为响应的一部分等；
* 对于后续的请求，容器会从请求的cookie得到会话ID，将这个会话ID与现有的会话匹配，并把会话与当前请求关联。

无论在响应中<span style="color:red">发送</span>一个会话cookie，还是从请求中得到会话ID，都只需要一句话，余下的所有事情容器都帮你做好了：

```java
HttpSession session = request.getSession();
```

如果想知道会话是已经存在，还是刚刚创建的，可以访问`session.isNew()`方法：

```Java
public void doGet(HttpServletRequest request, HttpServletResponse response)
                        throws IOException, ServletException {
    response.setContentType("text/html");
    PrintWriter out = response.getWriter();
    HttpSession session = response.getSession();
    if (session.isNew) out.println("This is a new session");
    else out.println("Welcome back!");
}
```

如果不能用cookie，即有的浏览器禁用了cookie怎么办呢？可以使用URL重写(url rewriting)：把会话ID附加到访问应用的各个URL的最后。

![url_rewriting](figures/url_rewriting.png)

只有告诉响应要对URL编码，URL重写才能奏效：

```Java
public void doGet(HttpServletRequest request, HttpServletResponse response)
                        throws IOException, ServletException {
    response.setContentType("text/html");
    PrintWriter out = response.getWriter();
    HttpSession session = response.getSession();
    out.println("<html><body>");
    out.println("<a href=\"" + response.encodeURL("/BeerTest.do") 
                    + "\"> click me </a>");
    out.println("</body></html>");
}
```

容器看到一个`getSession()`调用，而且没有从客户的请求得到会话ID，容器就知道它必须尝试与客户建立一个新的会话。此时，容器并不知道cookie是否工作，所以向客户返回第一个响应时，它同时尝试cookie和URL重写这两种做法。

静态页面不可能完成URL重写，使用URL重写只有一种可能，这就是作为会话的一部分的所有页面都是动态生成的。

#### 会话管理

如果一个会话太长时间都不活动，怎样识别并撤销这个会话？

会话有3种死法：超时、在会话对象上调用`invalidate()`，应用结束(崩溃或取消部署)。可以在部署配置文件中配置会话超时，例如设置为15分钟：

```xml
<session-config> 
    <sessioin-timeout>15</session-timeout>
</session-config>
```

可以调用会话对象的`setMaxInactiveInterval()`设置某个特定会话实例的超时: `:::java session.setMaxInactiveInterval(15*60);`(注意单位为秒)

#### 定制cookie

默认地，cookie与会话的寿命一样长：一旦客户离开浏览器，cookie就会消失。但也可以告诉cookie在客户端上待得更久一些，甚至在浏览器关闭之后还持久保存：

```java
// 创建一个新的Cookie
Cookie cookie = new Cookie("username", name);
// 设置cookie的存活时间：单位为秒
cookie.setMaxAge(30*60);
// 把cookie发送到客户
response.addCookie(cookie);
// 从客户得到cookie
Cookie[] cookies = request.getCookies();
```

!!! example "简单的定制cookie示例"

### 7 使用JSP
### 无脚本的JSP
### 9 使用JSTL
### 10 定制标记开发
### 11 Web应用部署
### 12 Web应用安全
### 13 过滤器和包装器
### 模式和struts