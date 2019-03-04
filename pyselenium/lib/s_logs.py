#!/usr/bin/env python3
import logging
import os
from pyselenium.configs.yaml_config import YamlConfig, LOG_PATH
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

    def __init__(self, backup=3, level='DEBUG', output=0):
        init(autoreset=True)
        self.backup = backup
        self.level = level
        self.output = output
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
            self.set_output_mode(2)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical

    def coloring(self, text='', color='WHITE'):
        if hasattr(Fore, color.upper()):
            return getattr(Fore, color.upper()) + text
        else:
            print("no %s color!" % color)
            return text

    @classmethod
    def print_color(cls, text, color='green'):
        print(cls.coloring(text, color))

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


if __name__ == "__main__":
    logger = Log()
    logger.info('232323')
    logger.warning('2323')
    logger.error('2323')
    logger.debug('hahahaha')


