# 列表推导式
# map filter
# set dict 也可以被推导

a = [1,2,3,4,5,6]

b = [i**2 for i in a if i>4]
print(b)

students= {
    '小明':12,
    '小红':16,
    '小东':30
}

b = [key for key,value in students.items()]
print(b)