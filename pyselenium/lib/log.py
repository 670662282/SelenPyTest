#!/usr/bin/env python3
import logging
from logging.handlers import TimedRotatingFileHandler
from colorama import Fore, init
from colorlog import LevelFormatter

log_colors = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
}
init(autoreset=True)


def get_logger(level=logging.DEBUG, logfile='test.log', log_backup=3):

    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    handler_list = []

    formatter = LevelFormatter(fmt={
        'DEBUG': '%(log_color)sDEBUG: %(asctime)s %(name)s(%(module)s:%(lineno)d line) %(msg)s',
        'INFO': '%(log_color)sINFO: %(asctime)s %(name)s(%(module)s:%(lineno)d line) %(msg)s',
        'WARNING': '%(log_color)sWARN: %(asctime)s %(name)s(%(module)s:%(lineno)d line)  %(msg)s ',
        'ERROR': '%(log_color)sERROR: %(asctime)s %(name)s(%(module)s:%(lineno)d line)  %(msg)s ',
        'CRITICAL': '%(log_color)sCRIT: %(asctime)s %(name)s(%(module)s:%(lineno)d line)  %(msg)s ',
         },
        datefmt=None,
        reset=True,
        log_colors=log_colors
    )
    con_handle = logging.StreamHandler()
    con_handle.setLevel(level)
    con_handle.setFormatter(formatter)
    handler_list.append(con_handle)

    """create file handle for write logs"""
    if logfile:
        file_handle = TimedRotatingFileHandler(
            filename=logfile,
            when='D',
            interval=1,
            backupCount=log_backup,
            delay=True,
            encoding='utf-8'
        )
        file_handle.setLevel(level)
        file_handle.setFormatter(formatter)
        handler_list.append(file_handle)

    logger.handlers = handler_list

    return logger


def coloring(text='', color='WHITE'):
    if hasattr(Fore, color.upper()):
        return getattr(Fore, color.upper()) + text
    else:
        print("no %s color!" % color)
        return text


def print_color(text, color='green'):
    print('\n' + coloring(text, color) + '\n')


def disable_logger(log):
    if isinstance(log, logging.Logger):
        log.disabled = True
    else:
        print_color(str(type(log)) + 'is not logging.Logger Type.')


def enable_logger(log):
    if isinstance(log, logging.Logger):
        log.disabled = False
    else:
        print_color(str(type(log)) + 'is not logging.Logger Type.')


if __name__ == "__main__":
    logger = get_logger()
    logger.info('232323')
    logger.debug('2323')
    disable_logger(logger)
    logger.info('disable_logger')
    logger.debug('disable_logger')
    enable_logger(logger)
    logger.info('enable_logger')
    logger.debug('enable_logger')
