#coding:utf-8
try:
    import yaml
except (ModuleNotFoundError, NameError, ImportError, RuntimeError) as e:
    print('yaml加载失败 尝试命令‘pip install pyyaml’安装，或者离开')
    raise e

import json
import xml.etree.ElementTree as xml
import os



class Reader_Factory:

    @classmethod
    def reader(cls, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError('{}配置文件不存在！'.format(filepath))
        if filepath.endswith('.xml'):
            reader = cls.XmlReader
        elif filepath.endswith('.json'):
            reader = cls.JsonReader
        elif filepath.endswith('.yaml'):
            reader = cls.YamlReader
        else:
            raise ValueError("can't not open to {}, please use yaml xml json".format(filepath))
        return reader(filepath)

    class JsonReader:
        def __init__(self, file):
            self.data_ = dict()
            with open(file, 'rb', 'utf-8') as f:
                self.data_ = josn.load(f)

        @property
        def data(self):
            return self.data_

    class XmlReader:
        def __init__(self, file):
            self.tree = xml.parse(file)
        @property
        def data(self):
            return self.tree

    class YamlReader:
        def __init__(self, yaml):
            self.yaml = yaml
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
