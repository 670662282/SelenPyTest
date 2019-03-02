import os
from pyselenium.configs.cfread import ReaderFactory

BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
PYSELENIUM = os.path.join(BASE_PATH, 'pyselenium')


class YamlConfig:
    def __init__(self, config):
        self.reader = ReaderFactory.reader(config)
        self.config = self.reader.data

    # 默认在0节点上
    def get(self, element, index=0):
        return self.config[index].get(element)
