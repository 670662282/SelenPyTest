#!/usr/bin/env python3
class locker:
    def __init__(self):
        print("locker.__init__() should be not called.")

    @staticmethod
    def acquire():
        print("locker.acquire() called.（这是静态方法）")

    @staticmethod
    def release():
        print("  locker.release() called.（不需要对象实例）")

def deco(cls):
    '''''cls 必须实现acquire和release静态方法'''
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, cls))
            cls.acquire()
            try:
                return func()
            finally:
                cls.release()
        return __deco
    return _deco

@deco(locker)
def myfunc():
    print(" myfunc() called.")
#myfunc()

def _get_locs(*args, **kwargs):
    if len(args) == 1 or len(kwargs) == 1:
        if args and not kwargs:
            if args[0] and isinstance(args[0], str):
                print(1)

            return
        if kwargs and not args:
            print(2)
            return

    raise ValueError("locator error, only one")
#x(d='dsd', j='dsd')
#x()
#x()
_get_locs('ds')
