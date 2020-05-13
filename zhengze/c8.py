# sub 正则替换
import re

lanuage = 'PythonC#JavaPHPC#JavaPHPC#'

# sub 正则替换
r = re.sub('C#','GO', lanuage)
print(r)

# 0表示替换所有匹配的字符串
r = re.sub('C#','GO', lanuage,0)
print(r)

# 1表示替换第一个
r = re.sub('C#','GO', lanuage,1)
print(r)

s = 'A83C035D66E87'

def convert(value):
    print(value)
    matched = value.group()
    if int(matched) >= 6:
        return '9'
    else :
        return '0'

# 函数新增了替换逻辑
r = re.sub('\d',convert, s)
print(r)
