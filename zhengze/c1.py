import re

a='C|C++|Python|Java|Javascript'

# findall返回匹配的列表
r=re.findall('Python',a)
print(r)