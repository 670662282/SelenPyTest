import importlib
import sys

if __name__ == '__main__':
    sys.path.insert(0, '/Users/xa0574/PycharmProjects/SelenPyTest/demo/')

    module = importlib.import_module('no_except_window')
    for name, value in vars(module).items():
        print("name:", name)
        print("value:", value)
