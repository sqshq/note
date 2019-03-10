# -*- coding: utf-8 -*-

import subprocess
import os
from urllib.parse import quote

"""
快速重建MarkDown建成的网站，并在浏览器中打开或者刷新页面
用途：修改完MarkDown文件后，立即查看效果
"""



LOCALHOST = 'http://localhost/'
WIKI_SITE = os.getcwd()


def getWebURL(path):
	"""
	根据给定的markdown文件路径计算出URL
	:param path: markdown文件路径
	:return:
	"""
	doc_path = os.path.join(WIKI_SITE, 'docs/') 
	urlpath = quote(path)# 处理中文以及特殊字符
	return urlpath.replace(doc_path, LOCALHOST).replace('.md', '/')

def getMostRecentModifiedFile(path):
	"""
	获得最新修改的Markdown文件
	"""
	mostRecentModifiedFile = []
	_getMostRecentModifiedFile(mostRecentModifiedFile, path)
	return max(mostRecentModifiedFile)[1]


def _getMostRecentModifiedFile(mostRecentModifiedFile, path):
	"""
	获得最新修改的Markdown文件
	"""
	# 否则找出最小值
	for file in os.listdir(path):
		filename = os.path.join(path, file)
		if file.startswith('.'): # 隐藏文件
			continue
		if os.path.isdir(filename): # 文件夹
			_getMostRecentModifiedFile(mostRecentModifiedFile, filename)
		elif filename.endswith('.md'):   # md文件
			modifiedTime = os.path.getmtime(filename)
			mostRecentModifiedFile.append((modifiedTime, filename))

def openTab(url):
	"""
	打开网页，利用的是AppleScript
	find existing tab with URL, or open a new one.
	https://gist.github.com/stevenschobert/ba6845feb5b0db7cdf04d04362720424
	"""
	script = '''
	tell application "Safari"
	set topWindows to every window whose name is not ""
	set numWindows to the number of topWindows
	set didFind to false
	set targetUrl to "%s"
	log targetUrl
	repeat with x from 1 to numWindows
		set numTabs to the number of tabs in window x
		repeat with y from 1 to numTabs
			set tabUrl to the URL of tab y of window x
			log tabUrl
			if tabUrl contains targetUrl then
				set didFind to true
				tell window x to set current tab to tab y
				set docUrl to URL of document y
				set URL of document y to docUrl
				set index of window x to 1
			end if
		end repeat
	end repeat
	if didFind is false then
	tell window 1 to set current tab to (make new tab with properties {URL:targetURL})
	end if
	log didFind
	end tell
	''' % url
	# Open pipe to AppleScript through osascript command
	osapipe = os.popen("osascript", "w")
	# Write script to osascript's stdin
	osapipe.write(script)
	rc = osapipe.close()


def updateWiki():
	"""
	利用bash命令快速重建网站
	"""
	command = r"mkdocs build --dirty --site-dir=/Users/larry/techlarry.github.io"
	subprocess.Popen(command.split(), cwd='/Users/larry/techlarry/wiki')


if __name__ == "__main__":
	#updateWiki()
	file = getMostRecentModifiedFile(WIKI_SITE)
	url = getWebURL(file)
	openTab(url)

