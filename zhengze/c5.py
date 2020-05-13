# 边界匹配
# ^ 1.表示开头;2.在[]中表示取反
# $ 表示结尾
import re

qq = '100000001'

r = re.findall('\d{4,8}', qq)
print(r)


#
r = re.findall('^\d{4,8}$', qq)
print(r)