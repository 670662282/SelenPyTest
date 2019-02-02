#!/usr/bin/env python3
import logging
import os
import threading
from pyselenium.configs.config import YamlConfig, LOG_PATH
from logging.handlers import TimedRotatingFileHandler
from colorama import Fore, init
from colorlog import LevelFormatter

log_colors_config = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
}


class Log(object):

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Log, "_instance"):
            with Log._instance_lock:
                if not hasattr(Log, "_instance"):
                    Log._instance = object.__new__(cls)
        return Log._instance

    def __init__(self):
        init(autoreset=True)
        self.logs = YamlConfig().get('log')
        if self.logs is None:
            raise KeyError
        self.backup = self.logs.get('backup', 5)
        self.level = self.logs.get('level', 'INFO')
        self.pattern = self.logs.get('pattern',
                                     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.output = self.logs.get('output', 0)
        self.logger = logging.getLogger('SelePyTest')

        """
        重复打印日志原因是在自定义中，每初始化会添加一个handler
        判断没有handler才去添加
        """
        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not self.logger.handlers:
            # set log level main on-off
            self.logger.setLevel(self.level)
            self.formatter = LevelFormatter(
                self.pattern,
                datefmt="%d %b %Y %H:%M:%S",
                reset=True,
                log_colors=log_colors_config[self.level])
            self.set_output_mode(self.output)

        self.debug = self.log_with_color("DEBUG")
        self.info = self.log_with_color("INFO")
        self.warning = self.log_with_color("WARNING")
        self.error = self.log_with_color("ERROR")
        self.critical = self.log_with_color("CRITICAL")


    def coloring(self, text='', color='WHITE'):
        if hasattr(Fore, color):
            return getattr(Fore, color.upper()) + text
        else:
            print("no %s color!" % color)
            return text

    def print_color(self, text, color='green'):
        print(self.coloring(text, color))

    def _file_output(self):
        """create file handle for write logs"""
        log_file = os.path.join(LOG_PATH, 'test.log')
        file_handle = TimedRotatingFileHandler(filename=log_file,
                                               when='D',
                                               interval=1,
                                               backupCount=self.backup,
                                               delay=True,
                                               encoding='utf-8')

        # log_file level
        file_handle.setLevel(self.level)
        file_handle.setFormatter(self.formatter)
        self.logger.addHandler(file_handle)

    def _console_output(self):
        # get  console handle
        con_handle = logging.StreamHandler()
        # console print level
        con_handle.setLevel(self.level)
        # set log format
        con_handle.setFormatter(self.formatter)
        self.logger.addHandler(con_handle)

    def set_output_mode(self, output=0):

        if output == 0:
            self._console_output()
        elif output == 1:
            self._file_output()
        else:
            self._console_output()
            self._file_output()

    def log_with_color(self, level):
        def log_level(text):
            getattr(self.logger, level.lower())(self.coloring(text, log_colors_config[level.upper()]))
        return log_level


if __name__ == "__main__":
    l = Log()
   # if hasattr(l.logger, 'info'):
        #l.log_info('23323')
    #l.log_with_color("DEBUG")('dsdsd')
