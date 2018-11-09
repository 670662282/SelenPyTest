import os
from time import strftime, localtime, time, sleep
from selenium.common.exceptions import NoSuchElementException,
                                        WebDriverException
from SelenPyTest.pyselenium.configs.config import IMAGE_PATH, Config
import functools
try:
    import keyring
except (NameError, ImportError, RuntimeError):
    pass

MAX_TIME = Config().get('TIME_OUT')

def get_png(driver, file_name):
    pngname = 'screenshot_' + strftime("%Y%m%d-%H%M%S", localtime()) + file_name
    print('出错截图：', pngname)
    driver.get_screenshot_as_file(os.path.join(IMAGE_PATH, pngname))


def get_passwd(usr=None, pwd=None, type='email'):
    """ get password for keyring """
    if pwd is None:
        try:
            pwd = keyring.get_password(type, usr)
            print("keyring get password for ", usr)
        except NameError as e:
            print("keyring加载失败 尝试命令‘pip install keyring’安装，或者离开")
            raise e
        if pwd is None:
            import getpass
            pwd = getpass.getpass('请输入用户名{}的密码:'.format(usr))
            answer = ''
            while answer != 'y' and answer != 'n':
                answer = input("用户名和密码是否存入钥匙环? [y/n]: ").strip().lower()
            if answer == 'y':
                register(type, usr, pwd)

    return pwd

def register(type, usr, pwd):
    """save username password in keyring"""
    keyring.set_password(type, usr, pwd)

def unregister(type, usr):
    try:
        keyring.delete_password(type, usr)
    except PasswordDeleteError:
        print(usr, ' 删除一个不存在的密码')


def changewait(time):
    def _changewait(func):
        @functools.wraps(func)
        def waits(self, *args, **kw):
            self.set_wait(time)
            result = func(self, *args, **kw)
            self.set_wait(MAX_TIME)
            return result
        return waits
    return _changewait

def wait(timeout)
    def _wait(fn):
        @functools.wraps(fn)
        def modfied_fn(self, *args, **kwargs):
            start_time = time()
            while True:
                try:
                    return fn(self, *args, **kwargs)
                except (WebDriverException, NoSuchElementException, AssertionError) as e:
                    if time() - start_time > timeout:
                        print('wait Timeout 30s!')
                        raise e
                    sleep(0.5)
        return modfied_fn
    return _wait

def capture_except(fun):
    def capture(self, *args, **kw):
        try:
            return fun(self, *args, **kw)
        except BaseException as e:
            self.except_parse(po.capture_error_closed, e)
    return capture
