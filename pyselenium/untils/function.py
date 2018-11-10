import os
from time import strftime, localtime, time, sleep
from keyring.errors import PasswordDeleteError
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from SelenPyTest.pyselenium.configs.config import IMAGE_PATH, Config
from SelenPyTest.pyselenium.models.ssh import Tl_ssh
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

def register(type='email', usr=None, pwd=None):
    """save username password in keyring"""
    keyring.set_password(type, usr, pwd)

def unregister(type='email', usr=None):
    try:
        keyring.delete_password(type, usr)
    except PasswordDeleteError:
        return False
    else:
        return True


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

def wait(timeout):
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


#获取测试页面的web日志 通过sftp下载
def get_weblog(ip, pwd, service_file=None, local_path=None):
    ssh = Tl_ssh(ip, pwd)
    ssh.connect()
    ssh.set_transport()
    if not os.path.isfile(service_file):
        raise TypeError(service_file, '不是一个合法文件')
    file_name = os.path.basename(service_file)
    local_file = None
    if local_path is None or os.path.isdir(local_path):
        if local_path is None:
            local_path = './log'
            os.mkdir(local_path)
        local_file = os.path.join(local_path, file_name)
    else:
        local_file = local_path
    try:
        ssh.down(service_file, local_file)
    except FileNotFoundError:
        print('soory no find {}'.format(log_name))
        return None
    finally:
        ssh.close()

    return local_file
