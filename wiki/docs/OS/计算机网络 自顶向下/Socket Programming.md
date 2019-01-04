---
title: Socket Programming
---

一共5个套接字编程作业。

### 1 Web服务器

在本实验中，您将学习Python中TCP连接的套接字编程的基础知识：如何创建套接字，将其绑定到特定的地址和端口，以及发送和接收HTTP数据包。您还将学习一些HTTP头部格式的基础知识。

您将开发一个处理一个HTTP请求的Web服务器。您的Web服务器应该接受并解析HTTP请求，然后从服务器的文件系统获取所请求的文件，创建一个由响应文件组成的HTTP响应消息，前面是头部行，然后将响应直接发送给客户端。如果请求的文件不存在于服务器中，则服务器应该向客户端发送“404 Not Found”差错报文。

#### 代码

在文件下面你会找到Web服务器的代码框架。您需要填写这个代码。而且需要在标有#Fill in start 和 # Fill in end的地方填写代码。另外，每个地方都可能需要不止一行代码。

#### 运行服务器

将HTML文件(例如HelloWorld.html)放在服务器所在的目录中。运行服务器程序。确认运行服务器的主机的IP地址（例如128.238.251.26）。从另一个主机，打开浏览器并提供相应的URL。例如：

http://128.238.251.26:6789/HelloWorld.html

"HelloWorld.html"是您放在服务器目录中的文件。还要注意使用冒号后的端口号。您需要使用服务器代码中使用的端口号来替换此端口号。在上面的例子中，我们使用了端口号6789. 浏览器应该显示HelloWorld.html的内容。如果省略“:6789”，浏览器将使用默认端口80，只有当您的服务器正在端口80监听时，才会从服务器获取网页。

然后用客户端尝试获取服务器上不存在的文件。你应该会得到一个“404 Not Found”消息。

#### Web服务器的Python代码框架

```python
#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket 
#Fill in start 
#Fill in end 
while True:     
#Establish the connection    
print 'Ready to serve...'     
connectionSocket, addr =   #Fill in start  #Fill in end
try:         
    message =   #Fill in start  #Fill in end
    filename = message.split()[1]                          
    f = open(filename[1:])
    outputdata = #Fill in start  #Fill in end
    #Send one HTTP header line into socket         
    #Fill in start         
    #Fill in end    

    #Send the content of the requested file to the client
    for i in range(0, len(outputdata)):
        connectionSocket.send(outputdata[i])
    connectionSocket.close()
except IOError:
    #Send response message for file not found
    #Fill in start
    #Fill in end

    #Close client socket
    #Fill in start
    #Fill in end             
serverSocket.close()
```

#### 可选练习

1. 目前，这个Web服务器一次只处理一个HTTP请求。请实现一个能够同时处理多个请求的多线程服务器。使用线程，首先创建一个主线程，在固定端口监听客户端请求。当从客户端收到TCP连接请求时，它将通过另一个端口建立TCP连接，并在另外的单独线程中为客户端请求提供服务。这样在每个请求/响应对的独立线程中将有一个独立的TCP连接。
2. 不使用浏览器，编写自己的HTTP客户端来测试你的服务器。您的客户端将使用一个TCP连接用于连接到服务器，向服务器发送HTTP请求，并将服务器响应显示出来。您可以假定发送的HTTP请求将使用GET方法。客户端应使用命令行参数指定服务器IP地址或主机名，服务器正在监听的端口，以及被请求对象在服务器上的路径。以下是运行客户端的输入命令格式。 
   ```
   > client.py server_host server_port filename
   ```

#### 解答

使用Python3的服务器：

```Python
#import socket module
import socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#Prepare a sever socket 
serverName = socket.gethostname()
serverPort = 4556
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
while True:     
#Establish the connection    
    print('Ready to serve...')     
    connectionSocket, addr = serverSocket.accept()
    try:         
        message =  connectionSocket.recvfrom(2048)
        filename = message[0].split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket         
        header = 'HTTP/1.1 200 OK\r\n' +\
            'Connection: close\r\n' + \
            'Content-Type: text/html\r\n' + \
            'Content-Length: %d\r\n\r\n' % (len(outputdata))
        connectionSocket.send(header.encode())
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
        connectionSocket.send(header.encode())
        #Close client socket
        connectionSocket.close()
serverSocket.close()
```

### 2 UDP Ping 程序

在本实验中，您将学习使用Python进行UDP套接字编程的基础知识。您将学习如何使用UDP套接字发送和接收数据报，以及如何设置适当的套接字超时。在实验中，您将熟悉Ping应用程序及其在计算统计信息(如丢包率)中的作用。

您首先需要研究一个用Python编写的简单的ping服务器程序，并实现对应的客户端程序。这些程序提供的功能类似于现代操作系统中可用的标准ping程序功能。然而，我们的程序使用更简单的UDP协议，而不是标准互联网控制消息协议(ICMP)来进行通信。 ping协议允许客户端机器发送一个数据包到远程机器，并使远程机器将数据包返回到客户(称为回显)的操作。另外，ping协议允许主机计算它到其他机器的往返时间。

以下是Ping服务器程序的完整代码。你的任务是写出Ping客户端程序。

#### 服务器代码

以下代码完整实现了一个ping服务器。您需要在运行客户端程序之前编译并运行此代码。*而且您不需要修改此代码。*

在这个服务器代码中，30％的客户端的数据包会被模拟丢失。你应该仔细研究这个代码，它将帮助你编写ping客户端。

``` python
# UDPPingerServer.py 
# We will need the following module to generate randomized lost packets import random 
import socket
import random

# Create a UDP socket  
# Notice the use of SOCK_DGRAM for UDP packets 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
# Assign IP address and port number to socket 
serverSocket.bind((socket.gethostname(), 12000)) 

while True:     
	# Generate random number in the range of 0 to 10 
	rand = random.randint(0, 10)     
	# Receive the client packet along with the address it is coming from  
	message, address = serverSocket.recvfrom(1024) 
	# Capitalize the message from the client     
	message = message.upper() 
	# If rand is less is than 4, we consider the packet lost and do not respond     
	if rand < 4:         
		continue     
	# Otherwise, the server responds         
	serverSocket.sendto(message, address) 
```

服务器程序在一个无限循环中监听到来的UDP数据包。当数据包到达时，如果生成一个随机整数大于或等于4，则服务器将数字转为大写并将其发送回客户端。

#### 数据包丢失

UDP为应用程序提供了不可靠的传输服务。消息可能因为路由器队列溢出，硬件错误或其他原因，而在网络中丢失。但由于在内网中很丢包甚至不丢包，所以在本实验室的服务器程序添加人为损失来模拟网络丢包的影响。服务器创建一个随机整数，由它确定传入的数据包是否丢失。

#### 客户端代码

您需要实现以下客户端程序。

客户端向服务器发送10次ping。因为UDP是不可靠的协议，所以从客户端发送到服务器的数据包可能在网络中丢失。因此，客户端不能无限期地等待ping消息的回复。客户等待服务器回答的时间至多为一秒，如果在一秒内没有收到回复，您的客户端程序应该假定数据包在网络传输期间丢失。您需要查找Python文档，以了解如何在数据报套接字上设置超时值。

具体来说，您的客户端程序应该

1. 使用UDP发送ping消息（注意：不同于TCP，您不需要首先建立连接，因为UDP是无连接协议。）
2. 从服务器输出响应消息，如果有的话
3. 如果从服务器受到响应，则计算并输出每个数据包的往返时延(RTT)（以秒为单位），
4. 否则输出“Request time out”

在开发过程中，您应该先在计算机上运行`UDPPingerServer.py`，并通过向`localhost`（或127.0.0.1）发送数据包来测试客户端。调试完成代码后，您应该能看到ping服务器和ping客户端在不同机器上通过网络进行通信。

#### 消息格式

本实验中的ping消息格式使用最简单的方式。客户端消息只有一行，由以下格式的ASCII字符组成：

> Ping *sequence_number time*

其中*sequence_number*从1开始，一直到10，共10条消息，而*time*则是客户端发送消息时的时间。

#### 可选练习

1. 目前，程序计算每个数据包的往返时间(RTT)，并单独打印出来。请按照标准ping程序的模式修改。您需要在客户端每次ping后显示最小，最大和平均RTT。另外，还需计算丢包率（百分比）。
2. UDP Ping的另一个类似的应用是UDP Heartbeat。心跳可用于检查应用程序是否已启动并运行，并报告单向丢包。客户端在UDP数据包中将一个序列号和当前时间戳发送给正在监听客户端心跳的服务器。服务器收到数据包后，计算时差，报告丢包（若发生）。如果心跳数据包在指定的一段时间内丢失，我们可以假设客户端应用程序已经停止。实现UDP Heartbeat（客户端和服务器端）。您需要修改给定的UDPPingerServer.py和您自己的UDP ping客户端。


#### 解答

```Python
import socket
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverName = socket.gethostname()
serverPort = 12000
clientSocket.settimeout(1.0) # 设置套接字超时值1秒
for i in range(10):
    send_time_ns = time.process_time_ns()
    message = "Ping {0}, {1}".format(i+1, send_time_ns)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage = False
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        receive_time_ns = time.process_time_ns()
        print(modifiedMessage)
        print("RTT: {0}s\n".format((receive_time_ns - send_time_ns)/1e6))
    except:
        print("Request time out\n")

clientSocket.close()
```


### 4 多线程Web代理服务器

在本实验中，您将了解Web代理服务器的工作原理及其基本功能之一 —— 缓存。

您的任务是开发一个能够缓存网页的小型Web代理服务器。这是一个很简单的代理服务器，它只能理解简单的GET请求，但能够处理各种对象 —— 不仅仅是HTML页面，还包括图片。

通常，当客户端发出一个请求时，请求将被直接发送到Web服务器。然后Web服务器处理该请求并将响应消息发送客户端。为了提高性能，我们在客户端和Web服务器之间建立一个代理服务器。现在，客户端发送的请求消息和Web服务器返回的响应消息都要经过代理服务器。换句话说，客户端通过代理服务器请求对象。代理服务器将客户端的请求转发到Web服务器。然后，Web服务器将生成响应消息并将其传递给代理服务器，代理服务器又将其发送给客户端。

![ProxyServerDemo](figures/ProxyServerDemo.png)

#### 运行代理服务器

使用命令行模式运行您的代理服务器程序，然后从您的浏览器发送一个网页请求，将IP地址和端口号指向代理服务器。 例如：http://localhost:8888/www.google.com。为了在独立的计算机上使用浏览器和代理服务器， 因此，在运行代理服务器时，您需要将“localhost”更换为代理服务器的所在机器的IP地址。您还需要将“8888”替换您在代理服务程序中使用的端口。号。

#### 配置浏览器

您还可以直接配置您的Web浏览器以使用您的代理服务。具体取决于您的浏览器。你首先要毫无问题地在同一台计算机上运行代理服务器和浏览器。这种方式下，使用代理服务器获取网页就只需提供页面的URL。


#### 代理服务器的Python代码框架

```python
import socket
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n'
        + '[server_ip : It is the IP Address Of Proxy Server]')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Fill in start.
# Fill in end.
while True:
	# Start receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	message = # Fill in start. # Fill in end.
	print(message)
	# Extract the filename from the given message
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print(filename)
	fileExist = "false"
	filetouse = "/" + filename
	print(filetouse)
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")
		outputdata = f.readlines()
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n")
		tcpCliSock.send("Content-Type:text/html\r\n")
		# Fill in start.
		# Fill in end.
		print('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			c = # Fill in start. # Fill in end.
			hostn = filename.replace("www.","",1) 
			print(hostn)
			try:
				# Connect to the socket to port 80
				# Fill in start.
				# Fill in end.
				# Create a temporary file on this socket and ask port 80
				for the file requested by the client
				fileobj = c.makefile('r', 0)
				fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
				# Read the response into buffer
				# Fill in start.
				# Fill in end.
				# Create a new file in the cache for the requested file.
				# Also send the response in the buffer to client socket 
				# and the corresponding file in the cache
				tmpFile = open("./" + filename,"wb")
				# Fill in start.
				# Fill in end.
			except:
				print("Illegal request")
		else:
			# HTTP response message for file not found
			# Fill in start.
			# Fill in end.
	# Close the client and the server sockets
	tcpCliSock.close()
# Fill in start.
# Fill in end.
```

#### 可选练习

1. 目前代理服务器不能处理错误。这可能会导致一些问题，当客户端请求一个不可用的对象时，由于“404 Not Found”响应通常没有响应正文，而代理服务器会假设有正文并尝试读取它。
2. 当前代理服务器只支持HTTP GET方法。通过添加请求体来增加对POST的支持。
3. 缓存：每当客户端发出特定请求时，典型的代理服务器会缓存网页。缓存的基本功能如下：当代理获得一个请求时，它将检查请求的对象是否已经在缓存中，如果是，则从缓存返回对象，从而不用联系服务器。如果对象未被缓存，则代理从服务器获取该对象，向客户端返回该对象，并缓存一个拷贝以备将来的请求。在实际环境下，代理服务器必须验证被缓存的响应是否仍然有效，并且它们能对客户端正确响应。您可以在RFC 2068中阅读有关缓存及其在HTTP中实现方式的更多细节。添加上述简单的缓存功能。您不需要实现任何替换或验证策略。然而您需要实现的是，将请求和响应写入磁盘（即缓存）并能从磁盘中获取它们，用于缓存被请求命中时。为此，您需要在代理中实现一些内部数据结构，以便跟踪哪些请求处于缓存中时，以及它们在磁盘上的位置。您也可以将此数据结构保存在内存中，因为没有必要关机之后持续保存这些数据。