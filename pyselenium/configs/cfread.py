#coding:utf-8
try:
    import yaml
except (ModuleNotFoundError, NameError, ImportError, RuntimeError) as e:
    print('yaml加载失败 尝试命令‘pip install pyyaml’安装，或者离开')
    raise e

import os

class YamlReader:
    def __init__(self, yaml):
        if os.path.exists(yaml):
            self.yaml = yaml
        else:
            raise FileNotFoundError('yaml配置文件不存在！')
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yaml, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data
    #@dump.setter
    def dump(self, datas):
        with open(self.yaml, 'a', endcoding='utf-8') as f:
            yaml.dump_all(datas, f, default_flow_style=False, indent=4)
