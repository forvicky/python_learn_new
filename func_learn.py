"""
函数
"""
def student_info(name,age=18,address='人民路小学'): # 默认参数
    return name,age,address                        #返回多参序列

#序列拆包，最好用多个变量来接受多参返回值，这样每个变量含义比较明确
name,age,address=student_info('zww')
print(name,age,address)
name,age,address=student_info('zdd',address='柳园小学')  #指定参数
print(name,age,address)

"""
匿名函数
"""
def add(x,y):
    return x+y

print(add(1,2))

f= lambda x,y:x+y

print(f(1,2))

#条件为真时返回的结果 if 条件判断 else 条件为假时返回的结果
a = 2
b = 1
r = a if a > b else b
print(r)


list_x= [1,0,1,0,1,0]
r=filter(lambda x:True if x ==1 else False,list_x)
print(list(r))