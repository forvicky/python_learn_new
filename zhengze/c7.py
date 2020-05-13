# findall第三个参数
import re

lanuage = 'PythonC#\nJavaPHP'

r = re.findall('c#', lanuage)
print(r)

# re.I忽略大小写
r = re.findall('c#', lanuage, re.I)
print(r)

# re.I忽略大小写;re.S表示.也可以匹配\n
r = re.findall('c#.{1}', lanuage, re.I|re.S)
print(r)