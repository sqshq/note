---
title: 3 - 基本库的使用
toc: false
date: 2017-10-30
---


### 1 使用Urllib

Urllib库是Python内置的HTTP请求库([官方文档链接](https://docs.python.org/3/library/urllib.html))， 它包含四个模块：

* <C>request</C>模块，最基本的HTTP请求模块，可以用来模拟发送请求，就像在浏览器里输入网址然后敲击回车一样，只需要给库方法传入URL还有额外的参数，就可以模拟实现这个过程了。
* <C>error</C>模块即异常处理模块，如果出现请求错误，我们可以捕获这些异常，然后进行重试或其他操作保证程序不会意外终止。
* <C>parse</C>模块，用来解析URL。
* <C>robotparser</C>模块，用来解析robots.txt文件。

#### 1.1 发送请求

使用Urllib的[request模块](https://docs.python.org/3/library/urllib.request.html)可以方便地实现Request的发送并得到Response。

<hh>urlopen()</hh>

<C>urllib.request</C>模块提供了最基本的构造HTTP请求的方法，利用它可以模拟浏览器的一个请求发起过程，同时它还带有处理authenticaton(授权验证)，redirections(重定向)，cookies(浏览器Cookies)以及其它内容。

我们来感受一下它的强大之处，以Python官网为例，我们来把这个网页抓下来:

```Python
import urllib.request
# 打开网页
response = urllib.request.urlopen('https://www.python.org')
# 得到返回的网页内容
print(response.read().decode('utf-8'))
# 查看返回类型： <class 'http.client.HTTPResponse'>
print(type(response))
```

<C>urlopen</C>返回一个<C>HTTPResponse</C>对象，调用对象的<C>read()</C>方法可以得到返回的网页内容，调用<C>status</C>属性就可以得到返回结果的状态码，如200代表请求成功，404代表网页未找到等，调用<C>getheaders()</C>返回响应的头信息。

```Python
>>> response.status
200
>>> response.getheaders()
[('Server', 'nginx'), ('Content-Type', 'text/html; charset=utf-8'), ('X-Frame-Options', 'SAMEORIGIN'), ('x-xss-protection', '1; mode=block'), ('X-Clacks-Overhead', 'GNU Terry Pratchett'), ('Via', '1.1 varnish'), ('Content-Length', '49419'), ('Accept-Ranges', 'bytes'), ('Date', 'Fri, 19 Oct 2018 01:31:34 GMT'), ('Via', '1.1 varnish'), ('Age', '1228'), ('Connection', 'close'), ('X-Served-By', 'cache-iad2144-IAD, cache-bur17551-BUR'), ('X-Cache', 'HIT, HIT'), ('X-Cache-Hits', '1, 1'), ('X-Timer', 'S1539912694.426186,VS0,VE1'), ('Vary', 'Cookie'), ('Strict-Transport-Security', 'max-age=63072000; includeSubDomains')]
```

如果我们想给链接传递一些参数该怎么实现呢？我们首先看一下<C>urlopen()</C>函数的API：

```python
urllib.request.urlopen(url, data=None, [timeout, ]*, 
    cafile=None, capath=None, cadefault=False, context=None)
```

下面我们详细说明下这几个参数的用法。

**data参数**

<C>data</C>参数是可选的，如果要添加<C>data</C>，它要是字节流编码格式的内容，即<C>bytes</C>类型，可以通过<C>bytes()</C>方法进行转化，另外如果传递了这个 <C>data</C>参数，它的请求方式就不再是GET方式请求，而是POST。

```python
import urllib.parse
import urllib.request
# 转码成bytes(字节流)类型
data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
# 请求站点
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
# 返回网页内容
print(response.read())
```

**timeout参数**

<C>timeout</C>参数可以设置超时时间，单位为秒。如果请求超出了设置的这个时间还没有得到响应，就会抛出异常<C>urllib.error.URLError</C>。如果不指定，就会使用全局默认时间。可以通过设置超时时间C>timeout</C>来控制一个网页如果长时间未响应就跳过它的抓取，利用try-except语句就可以实现这样的操作:

```python
try:
    response = urllib.request.urlopen('http://httpbin.org/get', 
        timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')
```

<hh>Request</hh>

<C>urlopen()</C>方法也可以接收<C>Request</C>对象。<C>urlopen(url,...)</C>可以实现最基本请求的发起，但这几个简单的参数并不足以构建一个完整的请求，如果请求中需要加入Headers等信息，我们就可以利用更强大的<C>Request</C>类来构建一个请求。

<C>Request</C>类的构造方法：

```python
class urllib.request.Request(url, data=None, headers={}, 
    origin_req_host=None, unverifiable=False, method=None)
```

* <C>url</C>参数是URL。
* <C>data</C>参数如果要传必须传bytes(字节流)类型的，如果是一个字典，可以先用 <C>urllib.parse</C>模块里的<C>urlencode()</C>编码。
* <C>headers</C>参数是Request Headers，字典格式，你可以在构造Request时通过<C>headers</C>参数直接构造，也可以通过调用Request实例的<C>add_header()</C>方法来添加。
* <C>origin_req_host</C>参数指的是请求方的 host 名称或者 IP 地址.
* <C>unverifiable</C>参数指的是这个请求是否是无法验证的，默认是False
* <C>method</C>参数它用来指示请求使用的方法，比如GET，POST，PUT等等

下面看一个具体的例子

```python
from urllib import request, parse

url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'Germey'
}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
```


<hh>高级用法</hh>

有没有发现，在上面的过程中，我们虽然可以构造 Request，但是一些更高级的操作，比如 Cookies处理，代理设置等操作我们该怎么办？这时我们可以使用Handler。

<C>urllib.request</C>模块里的<C>BaseHandler</C>类，它是所有其他<C>Handler</C>的父类，它提供了最基本的<C>Handler</C>的方法，例如 <C>default_open()</C>、<C>protocol_request()</C>方法等。接下来就有各种 <C>Handler</C>子类继承这个<C>BaseHandler</C>类，举例几个如下：

* <C>HTTPDefaultErrorHandler</C>用于处理 HTTP 响应错误，错误都会抛出 HTTPError 类型的异常。
* <C>HTTPRedirectHandler</C>用于处理重定向。
* <C>HTTPCookieProcessor</C>用于处理 Cookies。
* <C>ProxyHandler</C>用于设置代理，默认代理为空。
* <C>HTTPPasswordMgr</C>用于管理密码，它维护了用户名密码的表。
* <C>HTTPBasicAuthHandler</C>用于管理认证，如果一个链接打开时需要认证，那么可以用它来解决认证问题。


#### 1.2 处理异常

Urllib的error模块定义了由request模块产生的异常。如果出现了问题，request模块便会抛出error模块中定义的异常。

<hh>URLError</hh>
URLError类来自Urllib库的error模块，它继承自OSError类，是error异常模块的基类，由request模块生的异常都可以通过捕获这个类来处理。它具有一个属性reason，即返回错误的原因。

```python
from urllib import request, error
try:
    # 打开不存在的网站
    response = request.urlopen('http://www.pythonfs.org')
except error.URLError as e:
    print(e.reason)
```

<hh>HTTPError</hh>

HTTPError是URLError的子类，专门用来处理HTTP请求错误，比如认证请求失败等等。

它有三个属性:

* code，返回 HTTP Status Code，即状态码，比如 404 网页不存在，500 服务器内部错误等等。
* reason，同父类一样，返回错误的原因。
* headers，返回 Request Headers。

```python
from urllib import request, error
try:
    # 打开不存在的网站
    response = request.urlopen('http://www.pythonfs.org')
except error.HTTPError as e:
    print(e.reason, e.code, e.headers)
```

#### 1.3 解析链接
#### 1.4 分析Robots协议
<hh>Robots协议</hh>

Robots协议也被称作爬虫协议、机器人协议，它的全名叫做网络爬虫排除标准(Robots Exclusion Protocol)，用来告诉爬虫和搜索引擎哪些页面可以抓取，哪些不可以抓取。它通常是一个叫做 robots.txt 的文本文件，放在网站的根目录下，例如[https://www.jd.com/robots.txt](https://www.jd.com/robots.txt) 。

当爬虫访问一个站点时，它首先会检查下这个站点根目录下是否存在robots.txt文件，如果存在，搜索爬虫会根据其中定义的爬取范围来爬取。如果没有找到这个文件，那么搜索爬虫便会访问所有可直接访问的页面。

下面我们看一下京东的robots.txt的样例

```
User-agent: * 
Disallow: /?* 
Disallow: /pop/*.html 
Disallow: /pinpai/*.html?* 
User-agent: EtaoSpider 
Disallow: / 
User-agent: HuihuiSpider 
Disallow: / 
User-agent: GwdangSpider 
Disallow: / 
User-agent: WochachaSpider 
Disallow: /
```

最简单的robots.txt只有两条规则：

* User-agent：指定对哪些爬虫生效
* Disallow：指定要屏蔽的网址。以正斜线(/)开头，可以列出特定的网址或模式。要屏蔽整个网站，使用正斜线即可;要屏蔽某一目录以及其中的所有内容，在目录名后添加正斜线;要屏蔽某个具体的网页，就指出这个网页。

<hh>robotparser</hh>


robotparser模块提供了一个类，叫做RobotFileParser。它可以根据某网站的 robots.txt文件来判断一个爬取爬虫是否有权限来爬取这个网页。

使用非常简单，首先看一下它的声明

```
urllib.robotparser.RobotFileParser(url='')
```

使用这个类的时候非常简单，只需要在构造方法里传入robots.txt的链接即可。当然也可以声明时不传入，默认为空，再使用<C>set_url()</C>方法设置一下也可以。

有常用的几个方法分别介绍一下：

* <C>set_url()</C>，用来设置 robots.txt 文件的链接。如果已经在创建 RobotFileParser 对象时传入了链接，那就不需要再使用这个方法设置了。
* <C>read()</C>，读取 robots.txt 文件并进行分析，注意这个函数是执行一个读取和分析操作，如果不调用这个方法，接下来的判断都会为 False，所以一定记得调用这个方法，这个方法不会返回任何内容，但是执行了读取操作。
* <C>parse()</C>，用来解析 robots.txt 文件，传入的参数是 robots.txt 某些行的内容，它会按照 robots.txt 的语法规则来分析这些内容。
* <C>can_fetch()</C>，方法传入两个参数，第一个是 User-agent，第二个是要抓取的 URL，返回的内容是该搜索引擎是否可以抓取这个 URL，返回结果是 True 或 False。
* <C>mtime()</C>，返回的是上次抓取和分析 robots.txt 的时间，这个对于长时间分析和抓取的搜索爬虫是很有必要的，你可能需要定期检查来抓取最新的 robots.txt。
* <C>modified()</C>，同样的对于长时间分析和抓取的搜索爬虫很有帮助，将当前时间设置为上次抓取和分析 robots.txt 的时间。

以上是这个类提供的所有方法，下面我们用实例来感受一下：


```
from urllib.robotparser import RobotFileParser
rp = RobotFileParser()
rp.set_url('https://www.jd.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'https://miaosha.jd.com')) // True
print(rp.can_fetch('GwdangSpider', "https://miaosha.jd.com")) // False
```


### 2 使用Requests

在前面一节我们了解了Urllib的基本用法，但是其中确实有不方便的地方。比如处理网页验证、处理Cookies等等，需要写Opener、Handler来进行处理。为了更加方便地实现这些操作，在这里就有了更为强大的库Requests，有了它，Cookies、登录验证、代理设置等操作都不是事儿。

[Requests官方文档](http://docs.python-requests.org/)

#### GET请求
首先让我们来构建一个最简单的 GET 请求，请求的链接为：http://httpbin.org/get，它会判断如果如果是 GET 请求的话，会返回响应的 Request 信息。

```Python
import requests
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get("https://www.zhihu.com/explore", headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles = re.findall(pattern, r.text)
print(titles)
```

#### POST请求

```Python
import requests

data = {'name': 'germey', 'age': '22'}
r = requests.post("http://httpbin.org/post", data=data)
print(r.text)
```

#### 文件上传

我们知道 Reqeuests 可以模拟提交一些数据，假如有的网站需要我们上传文件，我们同样可以利用它来上传，实现非常简单，实例如下：

```python
import requests

files = {'file': open('favicon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files=files)
print(r.text)
```

#### Cookie

可以直接用 Cookies 来维持登录状态。登录知乎，将 Headers 中的 Cookies 复制下来，将其设置到 Headers 里面，发送Request。

```Python
import requests

headers = {
    'Cookie': '知乎的Cookie',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}
r = requests.get('https://www.zhihu.com', headers=headers)
print(r.text)
```

#### 会话维持
在Requests中，如果直接利用<C>get()</C>或<C>post()</C>等方法的确可以做到模拟网页的请求。但是这实际上是相当于不同的会话，即不同的Session，也就是说相当于你用了两个浏览器打开了不同的页面。

设想这样一个场景，我们第一个请求利用了<C>post()</C>方法登录了某个网站，第二次想获取成功登录后的自己的个人信息，你又用了一次<C>get()</C> 方法去请求个人信息页面。实际上，这相当于打开了两个浏览器，是两个完全不相关的会话，能成功获取个人信息吗？那当然不能。

其实解决这个问题的主要方法就是维持同一个会话，也就是相当于打开一个新的浏览器选项卡而不是新开一个浏览器。但是我又不想每次设置Cookies，那该怎么办？这时候就有了新的利器Session对象。

####  代理设置

对于某些网站，在测试的时候请求几次，能正常获取内容。但是一旦开始大规模爬取，对于大规模且频繁的请求，网站可能会直接登录验证，验证码，甚至直接把IP给封禁掉。那么为了防止这种情况的发生，我们就需要设置代理来解决这个问题，在 Requests 中需要用到 proxies 这个参数。

```Python
import requests
proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
requests.get('https://www.taobao.com', proxies=proxies)
```


### 3 正则表达式

### 4 Example: 抓取猫眼电影排行



