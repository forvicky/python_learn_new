"""
python中没有switch..case,使用字典可以更方便实现类似功能
"""
def success():
    print('success')


def debug():
    print('debug')


def error():
    print('error')

def get_default():
    print('default')

numbers={
    0:success,
    1:debug,
    2:error
}

day=3

func=numbers.get(day,get_default)
func()