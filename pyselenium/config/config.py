import os
from .cfread import YamlReader

BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
CASE_PATH = os.path.join(BASE_PATH, 'case')
CONFIG_FILE = os.path.join(BASE_PATH, 'data', 'config.yaml')
LOG_PATH = os.path.join(BASE_PATH, 'Logs')
REPORT_PATH = os.path.join(BASE_PATH, 'reports')
IMAGE_PATH = os.path.join(REPORT_PATH, 'images')


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data
    #框架配置默认在0节点上
    def get(self, element, index=0):
        return self.config[index].get(element)
