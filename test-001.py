
class A():
    def __init__(self):
        print('初始化成功')

    # 新增文章
    def a(self, a):
        print(a)

    def b(self, b):
        print(b)

def c(c):
    print(c)


if __name__ == '__main__':
    A = A()
    A.a()
    A.b('aaa')