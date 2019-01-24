#!/usr/bin/env python3
import logging
import os
import threading
from pyselenium.configs.config import YamlConfig, LOG_PATH
from logging.handlers import TimedRotatingFileHandler


class Log(object):

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Log, "_instance"):
            with Log._instance_lock:
                if not hasattr(Log, "_instance"):
                    Log._instance = object.__new__(cls)
        return Log._instance

    def __init__(self):
        self.logs = YamlConfig().get('log')
        if self.logs is None:
            raise KeyError
        self.backup = self.logs.get('backup', 5)
        self.console_level = self.logs.get('console_level', 'INFO')
        self.file_level = self.logs.get('file_level', 'INFO')
        self.pattern = self.logs.get('pattern',
                                     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.output = self.logs.get('output', 0)
        self.logger = logging.getLogger()

        """
        重复打印日志原因是在自定义中，每初始化会添加一个handler
        判断没有handler才去添加
        """
        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not self.logger.handlers:
            # set log level main on-off
            self.logger.setLevel(logging.INFO)
            self.formatter = logging.Formatter(self.pattern)
            self.set_output_mode(self.output)

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
        file_handle.setLevel(self.file_level)
        file_handle.setFormatter(self.formatter)
        self.logger.addHandler(file_handle)

    def _console_output(self):
        # get  console handle
        con_handle = logging.StreamHandler()
        # console print level
        con_handle.setLevel(self.console_level)
        # set log format
        con_handle.setFormatter(self.formatter)
        self.logger.addHandler(con_handle)

    def set_output_mode(self, output):
        if output == 0:
            self._console_output()
        elif output == 1:
            self._file_output()
        else:
            self._console_output()
            self._file_output()

    def get_logger(self):
        return self.logger
