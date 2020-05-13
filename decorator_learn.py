"""
装饰器,在不改变函数内部实现的基础上动态增加新功能，aosp切面思想#java中的注解
"""
import time

def decorator(func):
    #key word
    def wrapper(*args,**kw):  #*args可变参数列表,**kw关键参数列表
        print(time.time())
        func(*args,**kw)
    return wrapper


#第一种调用
def f1():
    print("this is a function")

f=decorator(f1)
f()

#第二种调用
@decorator
def f2(arg1):
    print("this is a function"+arg1)

@decorator
def f3(arg1,arg2):
    print("this is a function"+arg1)
    print("this is a function"+arg2)

@decorator
def f4(arg1,arg2,**kw):
    print("this is a function"+arg1)
    print("this is a function"+arg2)
    print(kw)

f2('test f2')
f3('test f3','test f3')
f4('test f4','test f4',a=1,b=2,c='123')
