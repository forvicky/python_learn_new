# group分组,剔除定界字符串
import re

s = 'life is short,i use python,i love python'

r=re.search('life(.*)python(.*)python',s)
print(r.group(0))
print(r.group(1))
print(r.group(2))
print(r.group(0,1,2))
print(r.groups())

r=re.findall('life(.*)python(.*)python',s)
print(r)