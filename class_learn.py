"""
python类
"""
from human import Human

class Student(Human):
    name = 'zdd'        # 类变量
    age = 30
    english_score = 100

    # 构造函数,前后__是内置函数
    def __init__(self,name,age,sex):
        self.name = name  # 赋值给实例变量
        self.age = age
        self.no = '220900328'
        self.__english_score=0  #私有变量,被翻译成 _Student__english_score
        super(Student, self).__init__(sex) #调用父类
        print('init'+str(age))

    # 前__是私有方法
    def __marking(self,score):
        if score<0:
            score=0
        self.english_score=score
        print(self.english_score)

    def do_homework(self): #类中函数第一个参数必须有self
        print('homework')

    @classmethod  #类方法，与静态方法相似，只是入参强制要求传入cls参数
    def score_exchange(cls):
        if cls.english_score<60:
            print('不及格')
        elif cls.english_score>60:
            print('及格')

    @staticmethod  #静态方法
    def score_print():
        print(Student.english_score)

student1=Student('小东',18,'man')
student2=Student('小红',17,'woman')

Student.score_exchange()
student1.__english_score=10  #与self.__english_score不是同一个变量，而是python动态新增了一个变量，伪私有机制（翻译）只有在类内部才会触发
print(student1.__english_score)
print(student2.sex)
print(student1.__dict__)
student1._Student__marking(10)
Student.score_print()
print(student1.name)
print(Student.name)
student1.do_homework()