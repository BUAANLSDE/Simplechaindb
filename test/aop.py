__author__ = 'PC-LiNing'

def deco(func):
    def wrapper():
        print('wrapper start...')
        result=func()
        print('wrapper end...')
        return result
    return  wrapper

@deco
def foo():
    print('in foo.')
    return 10

print(foo())