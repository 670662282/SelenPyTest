import os
from .cfread import ReaderFactory

BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
PYSELENIUM = os.path.join(BASE_PATH, 'pyselenium')
CONFIG_FILE = os.path.join(PYSELENIUM, 'configs', 'config.yaml')
LOG_PATH = os.path.join(BASE_PATH, 'demo')
REPORT_PATH = os.path.join(LOG_PATH, 'report')
IMAGE_PATH = os.path.join(REPORT_PATH, 'images')

if not os.path.isdir(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)


class YamlConfig:
    def __init__(self, config=CONFIG_FILE):
        self.reader = ReaderFactory.reader(config)
        self.config = self.reader.data

    # 框架配置默认在0节点上
    def get(self, element, index=0):
        return self.config[index].get(element)
