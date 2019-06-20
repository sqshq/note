---
title: HTML
---

### 简介

HTML指**超文本标记语言**(**H**yper**T**ext **M**akeup **L**anguage)，可以实现图片、链接、音乐等多种元素，由W3C(万维网联盟)制定。

HTML**标签**(tag)是由*尖括号*包围的关键词(如`:::html <html>`)，它通常成对出现，第一个标签是*开始标签*(start tag, 如`:::html <p>`)，第二个标签是*结束标签*(end tag, 如`:::html </p>`)。

```html
<开始标签>内容</结束标签>
```

HTML**元素**指的是从开始标签到结束标签的所有代码(例如`:::html <p>This is a paragraph</p>`)。


!!! Tip "使用小写标签"
    
    HTML标签对大小写不敏感：`:::html <p>`等同于`:::html <P>`。W3C推荐使用小写。



典型的HTML文件如下所示:

```html
<!DOCTYPE html> 
<html> 
<head>
    <title>...<title>
    <link>...</link>
    <style>...</style>
    <script>...</script>
    ...
</head>
<body> 
    ...
</body> 
</html>
```

* `:::html <html>`标签是HTML页面的根元素，该标签的结束标志为`:::html </html>`。
* `:::html <head>`标签定义了头部元素，其包含了文档的元信息(meta-information)，可以插入脚本，样式文件等。
    * `:::html <title>`标签定义了文档的标题。
    * `:::html <link>`标签通常用于链接[样式表](CSS.md): `:::html <link rel="stylesheet" type="text/css" href="style.css">`
    * `:::html <style>`标签定义[内部样式表](CSS.md)。
    * `:::html <script>`标签用于加载脚本文件，例如[JavaScript](JavaScript.md)。
* `:::html <body>`元素定义文档的主体，即网页可见的页面内容。



#### 基本元素

* HTML标题(heading)是通过`:::html <h1>-<h6>`标签进行定义的。`:::html <h1>`定义最大的标题，`:::html <h6>`定义最小的标题。
* HTML水平线用`:::html <hr>`标签创建，用于分隔内容，在视觉上将文档分隔成各个部分。
* HTML注释可以提高可读性，使代码更容易被人理解。格式为`:::html <!--注释-->`。
* HTML段落是通过`:::html <p>`标签定义的。
* HTML换行使用`:::html <br/>`标签，可以理解为简单的输入一个空行。
* HTML使用标签`:::html <a>`设置超文本链接，具体格式为`:::html <a href="url" target=""></a>`。`target`属性值可以是`_blank`(新窗口打开)。

默认情况下，HTML会自动地在块级元素前后添加一个额外的空行，比如段落、标题元素前后。

#### 属性

HTML元素可以设置**属性**，一般位于开始标签内，以名/值对(name=value)的形式出现，属性值应该始终被包括在引号内。下面列出了适用于大多数元素的属性：

| 属性 | 描述 |
| --- | --- |
| class | 定义一个或多个类名(classname) |
| id | 定义元素的唯一id |
| style | 规定元素的内联样式 |
| title | 描述元素的额外信息(作为工具条使用) |

#### 文本格式化

HTML中存在一些格式化文本的标签，来调整文本样式。

* `:::html <strong>`, `:::html <b>`标签定义粗体文本。
* `:::html <em>`, `:::html <i>`标签定义斜体文本。
* `:::html <small>`, `:::html <big>`标签定义缩小/放大字体。
* `:::html <sub>`, `:::html <sup>`定义上标/下标字。

#### 图像

在HTML中，图像由`:::html <img>`标签定义，使用源属性(src)指定图像的URL地址，alt属性指定当图片无法加载时显示的文本。

```html
<img src="" alt="">
```

#### 表格

表格由`:::html <table>`标签定义，表格的行用`:::html <tr>`(table row)标签定义，单元格由`:::html <td>`(table data)标签定义。表格的表头使用`:::html <th>`标签进行定义。表格可以分为表格的页眉(thead)、主体(tbody)、页脚(tfoot)。

表格的基本结构为：

```html
<table>
    <thead>
        <tr>
            <th> </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td> </td>
        <tr>
    </tbody>
    <tfoot> </tfoot>
</table>
```

#### 列表

HTML支持有序、无序和定义列表。

**无序列表**(unordered list)使用粗体圆点进行标记，典型格式为

```html
<ul>
    <li>...</li>
    <li>...</li>
</ul>
```

**有序列表**使用数字标记，典型格式为

```html
<ol>
    <li>...</li>
    <li>...</li>
</ol>
```

#### 表单

HTML表单用于收集用户输入，包含表单元素。表单元素是允许用户在表单中输入内容的元素，例如文本域、下拉列表、单选框、复选框。


多数情况下被用到的表单元素是输入元素`:::html <input>`，其输入类型由类型属性(type)定义，常见输入类型如下：

* 文本域(Text Fields): `:::html <form> <input type="text"></form>`
* 密码字段: `:::html <form> <input type="password"></form>`
* **单选按钮**(Radio Buttons)：`:::html <form> <input type="radio"></form>`

!!! Example "单选按钮"
    
    ```html
    <form>
        <label><input type="radio" name="indoor-outdoor" value="indoor">indoor</label><br/>
        <label><input type="radio" name="indoor-outdoor" value="outdoor">outdoor</label>
    </form>
    ```
    
    效果如下
    <form>
    <label><input type="radio" name="indoor-outdoor" value="indoor">indoor</label><br/>
    <label><input type="radio" name="indoor-outdoor" value="outdoor">outdoor</label>
    </form>
    
* **复选框**(Checkboxes)： `:::html <form> <input type="checkbox"></form>`

!!! Example "复选框"

    ```html
    <form>
    <label><input type="checkbox" name="personality"></label>cat<br/>
    <label><input type="checkbox" name="personality"></label>dog<br/>
    <label><input type="checkbox" name="personality"></label>elephant<br/>
    </form>
    ```
    
    效果如下：
    <form>
    <label><input type="checkbox" name="personality"></label>cat<br/>
    <label><input type="checkbox" name="personality"></label>dog<br/>
    <label><input type="checkbox" name="personality"></label>elephant<br/>
    </form>
    
* **提交按钮**(Submit Button)： `:::html <form action="" method=""><input type="submit"></form>`。当用户点击确认按钮时，表单的内容会传送到另一个文件。表单的动作属性(action)定义了目的文件的文件名。由动作属性定义的这个文件通常会对接收到的数据进行相关的处理。例如利用[Servlet处理](Head First Servlets and JSP.md)。

!!! Example "用表单发送电子邮件"

    ```html
    <form action="MAILTO:someone@example.com" method="post" enctype="text/plain">
        Name:<input type="text" name="name" value="your name"><br>
        E-mail:<input type="text" name="mail" value="your email"><br>
        Comment:<input type="text" name="comment" value="your comment" size="50"><br>
        <input type="submit" value="Send">
    </form>
    ```
    
    效果如下：
    <form action="MAILTO:someone@example.com" method="post" enctype="text/plain">
    Name:<input type="text" name="name" value="your name" style="border: 1pt solid #aaa"><br>
    E-mail:<input type="text" name="mail" value="your email" style="border: 1pt solid #aaa"><br>
    Comment:<input type="text" name="comment" value="your comment" size="50" style="border: 1pt solid #aaa"><br>
    <input type="submit" value="Send">
    </form>

文本域(Textarea): 用户可以在文本域中写入文本：`:::html <textarea rows="10" cols="30">`


#### 字符实体

在HTML中不能使用某些符号，例如小于号(<)和大于号(>)，因为浏览器会误认为它们是标签。这些字符必须使用字符实体(character entities)，其通用格式为`:::html &entity_name;`。常见的字符实体有：

* 小于号: `:::html &lt;`
* 大于号: `:::html &gt;`
* 不间断空格，浏览器会截短空格，多个空格只保留一个空格：`:::html &nbsp;`


### HTML5

HTML5是HTML最新的版本，在2004年由W3C完成标准制定。
        