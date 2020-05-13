# 字符集
# ^ 取反
import re

s = 'abc,acc,adc,ae,afc,ahc'

# 普通字符一般是用来定界的,[]是或关系，一个[]只匹配一个字符
r = re.findall('a[cf]c', s)
print(r)

# c到f
r = re.findall('a[^c-f]c', s)
print(r)
