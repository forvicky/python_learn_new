# 数量词
# * 匹配0次或者无限多次
# + 匹配1次或者无限多次
# ? 1.匹配0次或者1次;2.前面是一个范围的话，表示的是非贪婪
import re

a = 'python 1111java678php'

# {3} 3个
r = re.findall('[a-z]{3}', a)
print(r)

# {3,6} 3~6个
# python默认是贪婪模式
r = re.findall('[a-z]{3,6}', a)
print(r)


# {3,6} 3~6个
# python默认是贪婪模式,?切换到非贪婪模式
r = re.findall('[a-z]{3,6}?', a)
print(r)

a = 'pytho0python1pythonn2'

r = re.findall('python*', a)
print(r)

r = re.findall('python?', a)
print(r)