#coding:utf-8
try:
    import yaml
except (ModuleNotFoundError, NameError, ImportError, RuntimeError) as e:
    print('yaml加载失败 尝试命令‘pip install pyyaml’安装，或者离开')
    raise e

import json
import xml.etree.ElementTree as xml
import os
#需要改动
from xlrd import open_workbook


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
        elif filepath.endswith('.excel'):
            reader = cls.ExcelReader
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


    class ExcelConfig:
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
            if not self._data:
                wb = open_workbook(self.excel)
                if type(self.sheet) == str:
                    s = workbook.sheet_by_name(self.sheet)
                elif type(self.sheet) == int:
                    s = workbook.sheet_by_index(self.sheet)
                else:
                    raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))

            if self.title_line:
                title = s.row_values(0)
                for col in range(1, s.nrows):
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    self._data.append(s.row_values(col))

            return self._data

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
