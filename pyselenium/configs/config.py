import os
from .cfread import YamlReader

BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
PYSELENIUM = os.path.join(BASE_PATH, 'pyselenium')
CONFIG_FILE = os.path.join(PYSELENIUM, 'configs', 'config.yaml')
LOG_PATH = os.path.join(BASE_PATH, 'demo')
REPORT_PATH = os.path.join(LOG_PATH, 'reports')
IMAGE_PATH = REPORT_PATH


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data
    #框架配置默认在0节点上
    def get(self, element, index=0):
        return self.config[index].get(element)
