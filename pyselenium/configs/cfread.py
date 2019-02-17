try:
    import yaml
except (ModuleNotFoundError, NameError, ImportError, RuntimeError) as e:
    print('yaml加载失败 尝试命令‘pip install pyyaml’安装，或者离开')
    raise e

import json
import xml.etree.ElementTree as xml
import os
from xlrd import open_workbook
from common.error import SheetTypeError
from collections import OrderedDict


class ReaderFactory:
    # TODO yaml json csv互相转换
    @classmethod
    def reader(cls, file_path):
        if file_path.endswith('.xml'):
            reader = cls.XmlReader
        elif file_path.endswith('.json'):
            reader = cls.JsonReader
        elif file_path.endswith(('.yml', '.yaml')):
            reader = cls.YamlReader
        elif file_path.endswith('.csv'):
            reader = cls.ExcelReader
        else:
            raise ValueError("can't not open to {}, please use yaml xml json".format(file_path))
        return reader(file_path)

    class JsonReader:
        def __init__(self, file):
            self.data_ = dict()
            with open(file, 'rb', encoding='utf-8') as f:
                self.data_ = json.load(f)

        @property
        def data(self):
            return self.data_

    class XmlReader:
        def __init__(self, file):
            self.tree = xml.parse(file)

        @property
        def data(self):
            return self.tree

    class ExcelReader:
        """
        读取excel文件中的内容。返回list。
        如：
        excel中内容为：
        | A  | B  | C  |
        | A1 | B1 | C1 |
        | A2 | B2 | C2 |

        如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
        [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

        如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
        [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

        可以指定sheet，通过index或者name：
        ExcelReader(excel, sheet=2)
        ExcelReader(excel, sheet='BaiDuTest')
        """
        def __init__(self, excel, sheet=0, title_line=False):
            self.excel = excel
            self.sheet = sheet
            self.title_line = title_line
            self._data = list()

        @property
        def data(self):
            sheet = None
            if not self._data:
                workbook = open_workbook(self.excel)
                if type(self.sheet) == str:
                    sheet = workbook.sheet_by_name(self.sheet)
                elif type(self.sheet) == int:
                    sheet = workbook.sheet_by_index(self.sheet)
                else:
                    raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))

            if self.title_line:
                title = sheet.row_values(0)
                for col in range(1, sheet.nrows):
                    self._data.append(dict(zip(title, sheet.row_values(col))))
            else:
                for col in range(0, sheet.nrows):
                    self._data.append(sheet.row_values(col))

            return self._data

    class YamlReader:
        def __init__(self, file, write_mode='w'):
            self.yaml = file
            self._data = None
            self._write_mode = write_mode

        @property
        def data(self):
            if not self._data:
                with open(self.yaml, 'r', encoding='utf-8') as f:
                    self._data = list(yaml.safe_load_all(f))
            return self._data

        @data.setter
        def data(self, data):
            with open(self.yaml, self._write_mode, encoding='utf-8') as f:
                self.ordered_yaml_dump(data, f, default_flow_style=False, allow_unicode=True, indent=4)

        @staticmethod
        def ordered_yaml_dump(data, stream=None, **kwargs):

            def _dict_representer(dumper, data):
                return dumper.represent_mapping(
                    yaml.loader.BaseResolver.DEFAULT_MAPPING_TAG,
                    data.items())

            yaml.SafeDumper.add_representer(OrderedDict, _dict_representer)
            return yaml.dump(data, stream, yaml.SafeDumper, **kwargs)

        """
        def ordered_yaml_load(self, stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
            class OrderedLoader(Loader):
                pass

            def construct_mapping(loader, node):
                loader.flatten_mapping(node)
                return object_pairs_hook(loader.construct_pairs(node))

            OrderedLoader.add_constructor(
                yaml.loader.BaseResolver.DEFAULT_MAPPING_TAG,
                construct_mapping)
            return yaml.load(stream, OrderedLoader)
        """


if __name__ == '__main__':
    file_path = 'test.yaml'
    ya = ReaderFactory.reader(file_path)
    info = OrderedDict({
        'URL': "http://10.10.120.3",
        'log': {
            'backup': 3,
            'level': "DEBUG",
            "output": 2
        },
        'RESERVE_REPORTS_NUM': 3,
        "EMAIL_SERVER": "smtp.163.com",
        "EMAIL_USR": '',
        "EMAIL_RECEIVE": '',
        "MAIL_TITLE": 'UI自动化测试报告',
        "IMP_TIME": 20,
        "TIME_OUT": 30,
    })
    ya.data = info
    print(ya.data)
    if os.path.isfile(file_path):
        os.remove(file_path)







