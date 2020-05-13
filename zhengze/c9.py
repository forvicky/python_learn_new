# 用的比较多的还是findall
import re

s = 'A83C035D66E87'

#从字符串首字母开始匹配
r=re.match('\d',s)
print(r)

#搜索字符串，返回匹配的第一个字符串
r1=re.search('\d',s)
print(r1)
print(r1.group())
print(r1.span())


r2=re.findall('\d',s)
print(r2)