import requests
from bs4 import BeautifulSoup #引入bs库, 解析HTML,

"""
	bs4库的解析是针对成对出现标签的文本
"""

r = requests.get("http://www.baidu.com")
r.encoding = r.apparent_encoding

demo = r.text

"""
	解析方式:
			1. html.parser 安装bs4即可
			2. lxml  安装lxml
			3. xml	安装lxml
			4. html5lib	安装html5lib
			上述都可以解析HTML内容
	基本元素:
			Tag: 标签,是最基本的组织单元, 分别用<>和</>标明开头和结尾
			Name: 标签的名字例如, <p>...</p>的名字是'p', 格式: <tag>.name
			Attributes: 标签的属性, 字典形式组织,格式: <tag>.attrs
			NavigableString: 标签内非属性字符串, <>...</>中的字符串,格式<tag>.string
			Comment: 标签内字符串的注释部分,一种特殊的Comment类型

"""

soup = BeautifulSoup(demo,"html.parser") #html.parser是html的解析器
#soup = BeautifulSoup(open("D://1.html"),"html.parser") #也可以采用打开文件的方式解析

print(soup.title) 
#存在多个a标签, 只能获得第一个标签的内容
print(soup.a)
print(soup.a.name,soup.a.parent.name)
#若不存在当前标签, 则返回一个空字典
print(soup.a.attrs,soup.a.attrs["href"])
print(soup.a.string)
