import os
from collections import OrderedDict
from time import strftime, localtime, time, sleep
from keyring.errors import PasswordDeleteError
from selenium.common.exceptions import NoSuchElementException, WebDriverException


import functools
from pyselenium.lib.log import get_logger, print_color
from pyselenium.lib.ssh import SSH

logger = get_logger()

try:
    import keyring
except (NameError, ImportError, RuntimeError):
    pass


def get_png(driver, image_path, img_name):
    image_name = 'screenshot_' + strftime("%Y%m%d-%H_%M_%S_", localtime()) + str(img_name) + '.png'
    path = os.path.join(image_path, image_name)
    driver.get_screenshot_as_file(path)
    return path


def find_alias(arg, compare):
    # TODO Refactor this function
    if not arg or not compare:
        return None
    arg = str(arg)
    max_char_alias_len = 0
    alias_char = None
    if isinstance(compare, str):
        compare = [compare]
    elif isinstance(compare, dict):
        compare = compare.keys()
    elif isinstance(compare, (list, set)):
        pass
    else:
        compare = str(compare)

    for key in compare:
        if key == arg:
            return key
        key = str(key)
        # str conversion List of characters
        key_char_list = ' '.join(key).split(' ')
        count = 0
        for i in arg:
            if i in key_char_list:
                count += 1
        max_len = len(key) if len(key) > len(arg) else len(arg)
        if count > max_len / 2 + 1 and count > max_char_alias_len:
            alias_char = key
            max_char_alias_len = count
            logger.debug("alias_char:{}, max_char_alias_len: {}".format(alias_char, max_char_alias_len))

    return alias_char


def get_password(usr=None, pwd=None, type='email'):
    """ get password for keyring """
    if pwd is None:
        try:
            pwd = keyring.get_password(type, usr)
            print_color("keyring get password for {}".format(usr), color='red')
        except NameError as e:
            print_color("keyring加载失败 尝试命令‘pip install keyring’安装，或者离开", color='red')
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
                        print_color('wait Timeout 30s!')
                        raise e
                    sleep(0.5)
        return modfied_fn
    return _wait


def capture_except(png_path=None, retry=0):
    def _capture_except(fn):
        @functools.wraps(fn)
        def capture(self, *args, **kw):
            try:
                fn(self, *args, **kw)
            except (WebDriverException, AssertionError) as e:
                png = png_path if png_path else self.png_path if self.png_path else '.'
                print_color('出错截图：{}'.format(get_png(self.driver, png, fn.__name__)))
                if retry:
                    self.except_parse(e, retry, fn, *args, **kw)
        return capture
    return _capture_except


def get_file_by_sftp(ip, pwd, service_file=None, local_path='./download_dir'):
    """sftp get remote host file
    :param ip: remote host ip
    :param pwd: remote host pasword
    :param service_file: remote host file path
    :param local_path: local file store path
    :return: local_file
    """
    ssh = SSH(ip, pwd)
    ssh.connect()
    ssh.set_transport()

    if local_path and os.path.isdir(local_path):
        logger.info("Folder {} exists".format(local_path))
    else:
        os.makedirs(local_path)

    file_name = os.path.basename(service_file)
    local_file = os.path.join(local_path, file_name)

    try:
        ssh.down(service_file, local_file)
    except FileNotFoundError:
        print_color('sorry, no find {}'.format(local_file), 'red')
        return None
    finally:
        ssh.close()

    return local_file


def create_project_scaffold(project_name):

    if project_name and os.path.isdir(project_name):
        logger.warning("Folder {} exists, please specify a new folder name".format(project_name))
        return

    logger.print_color("Start to create new project: {}".format(project_name), "YELLOW")

    dir_list = {
        os.path.join(project_name, 'reports/images'),
        os.path.join(project_name, 'testcases'),
        os.path.join(project_name, 'config'),
        os.path.join(project_name, 'logs'),
        os.path.join(project_name, 'runner'),
    }
    [os.makedirs(path) and logger.print_color("success crete dir {}".format(path), "YELLOW") for path in dir_list]

    from pyselenium.configs.cfread import ReaderFactory

    config = ReaderFactory.reader(os.path.join(project_name, 'config', 'config.yaml'))
    config.data = OrderedDict({
        'Api': {
            'is_listen': True
        },
        'log': {
            'backup': 3,
            'level': "DEBUG",
            "is_store": True
        },
        'email': {
            "EMAIL_SERVER": 'smtp.163.com',
            "EMAIL_USR": '',
            "EMAIL_RECEIVE": ''
        },
        'export': {
            'BACKUP_DAY': 3,
            'BACKUP_COUNT': 3,
            "MAIL_TITLE": 'UI自动化测试报告'
        },
        'wait_time': {
            "IMP_TIME": 20,
            "MAX_TIME_OUT": 30
        }

    })
