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


class Log:

    def __init__(self):
        init(autoreset=True)
        self.logs = YamlConfig().get('log')
        if self.logs is None:
            raise KeyError
        self.backup = self.logs.get('backup', 5)
        self.level = self.logs.get('level', 'INFO')
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
            self.formatter = LevelFormatter(fmt={
                'DEBUG': '%(log_color)sDEBUG: %(asctime)s(%(module)s:%(lineno)d) %(msg)s',
                'INFO': '%(log_color)sINFO: %(asctime)s%(msg)s',
                'WARNING': '%(log_color)sWARN: (%(module)s:%(lineno)d) %(asctime)s %(msg)s ',
                'ERROR': '%(log_color)sERROR: (%(module)s:%(lineno)d) %(asctime)s %(msg)s ',
                'CRITICAL': '%(log_color)sCRIT: (%(module)s:%(lineno)d) %(asctime)s %(msg)s ',
            },
                datefmt=None,
                reset=True,
                log_colors=log_colors_config
            )
            self.set_output_mode()

        self.debug = self.log_with_color("DEBUG")
        self.info = self.log_with_color("INFO")
        self.warning = self.log_with_color("WARNING")
        self.error = self.log_with_color("ERROR")
        self.critical = self.log_with_color("CRITICAL")

    def coloring(self, text='', color='WHITE'):
        if hasattr(Fore, color.upper()):
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
    l.logger.error('232323')
    if hasattr(l.logger, 'info'):
        l.error('23323')

