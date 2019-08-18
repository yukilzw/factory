import os
"""
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d['Bobs'] = '呵呵哒'
print('Bob' in d)

math = hex(582)
print(math)

def my_abs(x):
    if x >= 0:
        return 'asd'+'哦'
    else:
        return math
print(my_abs(8))

list_1 = [24,3]
def calc(*args,**kw):
    return args[0]+kw['c']
res = calc(*list_1,**{'c':5})
print(res)
"""

def age1(n):
    if n==1:
        return 1
    return n * age1(n - 1)
print(age1(10))

#tspath = os.path.abspath('./code/ts/dev.ts')
with open('../../README.md',  mode='r', encoding='UTF-8') as f:
    print(f.read()) 
