import pprint

try:
    import yaml
except (ModuleNotFoundError, NameError, ImportError, RuntimeError) as e:
    print('yaml加载失败 尝试命令‘pip install pyyaml’安装，或者离开')
    raise e

import json
import os
from xlrd import open_workbook
from common.error import SheetTypeError
from collections import OrderedDict


class ReaderFactory:
    # TODO yaml json csv互相转换
    @classmethod
    def reader(cls, file_path):
        if file_path.endswith('.json'):
            reader = cls.JsonReader
        elif file_path.endswith(('.yml', '.yaml')):
            reader = cls.YamlReader
        elif file_path.endswith(('.csv', '.xlsx')):
            reader = cls.ExcelReader
        else:
            raise ValueError("can't not open to {}, please use type <yaml xml json csv>".format(file_path))
        return reader(file_path)

    class JsonReader:
        def __init__(self, file, encoding='utf-8'):
            self.data_ = OrderedDict()
            self.json = file
            self.encoding = encoding

        @property
        def data(self):
            if not self.data_:
                with open(self.json, 'rb', encoding=self.encoding) as fp:
                    self.data_ = json.load(fp)
            return self.data_

        @data.setter
        def data(self, data):
            with open(self.json, 'a', encoding=self.encoding) as fp:
                json.dump(data, fp, indent=2)

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
        def __init__(self, excel_path, sheet=0, title_line=False):
            self.excel_path = excel_path
            self.sheet = sheet
            self.title_line = title_line
            self._data = list()
            self.start_col = 1 if title_line else 0

        @property
        def data(self):
            sheet = None
            if not self._data:
                workbook = open_workbook(self.excel_path)
                if isinstance(self.sheet, str):
                    sheet = workbook.sheet_by_name(self.sheet)
                elif isinstance(self.sheet, int):
                    sheet = workbook.sheet_by_index(self.sheet)
                else:
                    raise SheetTypeError('Please pass in `int` or `str`, not {0}'.format(type(self.sheet)))
            self._data = [self._parse_data_for_col(sheet, col) for col in range(self.start_col, sheet.nrows)]
            return self._data

        def _parse_data_for_col(self, sheet, col):
            """
            :param sheet:
            :param col:
            :return: if title_line return [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]
                    else return [[A,B,C], [A1,B1,C1], [A2,B2,C2]]
            """
            titles = sheet.row_values(0)
            return dict(zip(titles, sheet.row_values(col))) \
                if self.title_line else sheet.row_values(col)

    class YamlReader:
        def __init__(self, file, write_mode='a'):
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
        'URL': "http://www.baidu.com",
        'log': {
            'backup': 3,
            'level': "DEBUG",
            "output": 2
        },
        'RESERVE_REPORTS_NUM': 3,
        "EMAIL_SERVER": "smtp.163.com",
        "EMAIL_USR": '',
        "EMAIL_RECEIVE": '',
        "MAIL_TITLE": '自动化测试报告',
        "IMP_TIME": 20,
        "TIME_OUT": 30,
    })
    ya.data = info
    pprint.pprint(ya.data)
    if os.path.isfile(file_path):
        os.remove(file_path)







