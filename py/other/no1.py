from collections import Iterable
from module1.no2 import age1 as er

print(er(100))
age = 33
list1 = [1,2]
classmates = ('Michael', 'Bob', 'Tracy',1,2,12)
party = {'早餐':'八宝粥','晚餐':'烤鸭'}
if age >= 18:
    list1[1] = 666
    for key,name in party.items():
        print(key,name)
else:
    print('%.10f %%' % 3.1415926458)
print(isinstance(list1, Iterable))

xs = (x * x for x in range(10))
ns,sa,sb = 80, 'fdg0%%', 1
print(ns)

res1 = list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(res1)

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s()' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
@log('execute')
def now():
    print('2015-3-25')
now()

class Dog(object):
    car2="hehe"
    def __init__(self):
        self.car="skt"
    def run(self):
        print(self.car)
    def eat(self):
        print('Eating meat...')
dog1 = Dog()
dog1.run()
dog1.eat()