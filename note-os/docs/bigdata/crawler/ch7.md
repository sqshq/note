### **Python3网络爬虫开发实战 - 7 动态渲染页面爬取**

我们可以直接使用模拟浏览器运行的方式来实现爬取，这样就可以做到在浏览器中看到是什么样，抓取的源码就是什么样，也就是可见即可爬。

Selenium是一个自动化测试工具，利用它可以驱动浏览器执行特定的动作，如点击、下拉等操作，同时还可以获取浏览器当前呈现的页面的源代码 ，做到可见即可爬。 对于一些JavaScript动态渲染的页面来说，此种抓取方式非常有效。

### Selenium的使用

Selenium在使用前需要安装Selenium库和Chrome Drive.

#### 声明浏览器对象

Selenium 支持非常多的浏览器，如 Chrome、Firefox、Edge 等. 


```Python
from selenium import webdriver
browser = webdriver.Chrome()
browser = webdriver.Safari()
```

这样我们就完成了浏览器对象的初始化并赋值为browser对象，接下来我们要做的就是调用browser对象，让其执行各个动作，就可以模拟浏览器操作了。

#### 访问页面

我们可以用<C>get()</C>方法来请求一个网页，参数传入链接URL即可，比如在这里我们用<C>get()</C>方法访问淘宝，然后打印出源代码，代码如下：

```python
browser.get('https://www.taobao.com')
print(browser.page_source)
browser.close()
```

运行之后我们便发现弹出了 Chrome 浏览器，自动访问了淘宝，然后控制台输出了淘宝页面的源代码，随后浏览器关闭。


#### 查找节点

Selenium 提供了一系列查找节点的方法。 比如，

* <C>find_element_by_name(）</C>是根据<C>name</C>值获取.
* <C>find_element_by_id()</C>是根据<C>id</C>获取。
* <C>find_elements_by_xpath</C>是根据Xpath获取。
* <C>find_elements_by_class_name</C>是根据class name 获取。
* <C>find_elements_by_css_selector</C>是根据css selector获取。

例如，想要从淘宝页面中提取搜索框这个节点，

```python
input_first = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')
```

另外Selenium还提供了通用的<C>find_element()</C>方法，它需要传入两个参数，一个是查找的方式 <C>By</C>，另一个就是值，实际上它就是<C>find_element_by_id/name/xpath()</C>这种方法的通用函数版本，比如<C>find_element_by_id(id)</C>就等价于<C>find_element(By.ID, id)</C>，二者得到的结果完全一致。

如果要查找所有满足条件的节点，而不是一个节点，那就需要用<C>find_elements()</C>这样的方法，方法名称中element多了一个s，注意区分。

例如查找淘宝左侧导航条的所有条目

```python
lis = browser.find_elements_by_css_selector('.service-bd li')
```

和刚才一样，也可可以直接<C>find_elements()</C>方法来选择，所以也可以这样来写：

```python
lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
```


#### 获取节点信息

我们可以使用 get_attribute() 方法来获取节点的属性，那么这个的前提就是先选中这个节点。

每个 WebEelement 节点都有 text 属性，我们可以通过直接调用这个属性就可以得到节点内部的文本信息了，就相当于 BeautifulSoup 的 get_text() 方法、PyQuery 的 text() 方法。

另外 WebElement 节点还有一些其他的属性，比如 id 属性可以获取节点 id，location 可以获取该节点在页面中的相对位置，tag_name 可以获取标签名称，size 可以获取节点的大小，也就是宽高，这些属性有时候还是很有用的。


#### 节点交互

Selenium 可以驱动浏览器来执行一些操作，
     
输入文字用 send_keys() 方法，清空文字用 clear() 方法，另外还有按钮点击，用 click() 方法。