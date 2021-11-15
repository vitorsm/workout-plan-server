import gzip
import os
import shutil
import sys
from os.path import exists, splitext, basename, join, dirname

import logging

from logging.handlers import TimedRotatingFileHandler

from workout_plan_server import configs

FORMATTER = logging.Formatter('%(asctime)s %(levelname)s --- %(module)s:%(lineno)d @@@ %(message)s')
LOG_FILE = f"{configs.LOG_REPOSITORY}/workout-plan.log"

if not os.path.exists(configs.LOG_REPOSITORY):
    os.mkdir(configs.LOG_REPOSITORY)


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename="", when="midnight", interval=1, backup_count=14):
        super(GzipTimedRotatingFileHandler, self).__init__(filename=filename, when=when, interval=interval,
                                                           backupCount=backup_count)

    def doRollover(self):
        super(GzipTimedRotatingFileHandler, self).doRollover()
        log_dir = dirname(self.baseFilename)
        to_compress = [
            join(log_dir, f) for f in os.listdir(log_dir) if f.startswith(
                basename(splitext(self.baseFilename)[0])
            ) and not f.endswith((".gz", ".log"))
        ]
        for f in to_compress:
            if exists(f):
                with open(f, "rb") as _old, gzip.open(f + ".gz", "wb") as _new:
                    shutil.copyfileobj(_old, _new)
                os.remove(f)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = GzipTimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(configs.LOG_LEVEL)

    logger.setLevel(configs.LOG_LEVEL)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
