import requests
from bs4 import BeautifulSoup


r = requests.get("https://www.json.cn/")
r.encoding = r.apparent_encoding

demo = r.text
sp = BeautifulSoup(demo,"html.parser")

# 遍历HTML的方法
"""
	.contents : 子节点的列表, 将<tag>的所有儿子节点存入列表
	.children: 子节点的迭代类型, 循环遍历
	.descendants: 存储某个节点所有节点
"""
#头信息
#print(sp.head)
#print(sp.head.contents[2]) #返回类型为列表


#主体信息
#print(sp.body)
#遍历节点
#for ch in sp.body.children:
#	print(ch)

#for ds in sp.body.descendants:
#	print(ds)


"""
	.parent: 返回父亲节点
	.parents: 返回父辈节点的遍历
"""

#标签书的上行遍历
for par in sp.a.parents:
	print(par)
	if par is None:
		print(par)
	else:
		print(par.name)

