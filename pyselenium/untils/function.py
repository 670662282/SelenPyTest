import os
from time import strftime, localtime, time, sleep
from keyring.errors import PasswordDeleteError
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from pyselenium.configs.config import IMAGE_PATH, YamlConfig
from pyselenium.models.ssh import MySSH
import functools
from pyselenium.models.s_logs import Log

logger = Log()

try:
    import keyring
except (NameError, ImportError, RuntimeError):
    pass

MAX_TIME = YamlConfig().get('TIME_OUT')


def get_png(driver, file_name):
    png_name = 'screenshot_' + strftime("%Y%m%d-%H%M%S", localtime()) + file_name
    driver.get_screenshot_as_file(os.path.join(IMAGE_PATH, png_name))
    print('出错截图：', os.path.join(IMAGE_PATH, png_name))
    return os.path.join(IMAGE_PATH, png_name)


def get_password(usr=None, pwd=None, type='email'):
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


def change_wait(time):
    def _change_wait(func):
        @functools.wraps(func)
        def waits(self, *args, **kw):
            self.set_wait(time)
            result = func(self, *args, **kw)
            self.set_wait(MAX_TIME)
            return result
        return waits
    return _change_wait


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


def capture_except(fn):
    @functools.wraps(fn)
    def capture(self, *args, **kw):
        try:
            fn(self, *args, **kw)
        except (WebDriverException, AssertionError):
            get_png(self.driver, '_error.png')
            self.except_parse(self.driver)
            raise
    return capture


# 获取测试页面的web日志 通过sftp下载
def get_web_log(ip, pwd, service_file=None, local_path=None):
    ssh = MySSH(ip, pwd)
    ssh.connect()
    ssh.set_transport()

    if not os.path.isfile(service_file):
        raise TypeError(service_file, '不是一个合法文件')

    file_name = os.path.basename(service_file)
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
        print('sorry, no find {}'.format(local_file))
        return None
    finally:
        ssh.close()

    return local_file


def create_project_scaffold(project_name):

    if os.path.isdir(project_name):
        logger.warning("Folder {} exists, please specify a new folder name".format(project_name))
        return

    logger.print_color("Start to create new project: {}".format(project_name), "YELLOW")

    dir_list = {
        os.path.join(project_name, 'reports/images'),
        os.path.join(project_name, 'testcases'),
        os.path.join(project_name, 'config'),
    }
    [os.makedirs(path) and logger.print_color("success crete dir {}".format(path), "YELLOW") for path in dir_list]

    from pyselenium.configs.cfread import ReaderFactory

    config = ReaderFactory.reader(os.path.join(project_name, 'config', 'config.yaml'))
    config.data = {
        'URL': "http://10.10.120.3",
        'log': {
            'backup': 3,
            'level': "DEBUG",
            "output": 2
        },
        'RESERVE_REPORTS_NUM': 3,
        "EMAIL_SERVER": 'smtp.163.com',
        "EMAIL_USR": '',
        "EMAIL_RECEIVE": '',
        "MAIL_TITLE": 'UI自动化测试报告',
        "IMP_TIME": 20,
        "TIME_OUT": 30,
    }
