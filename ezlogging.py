# -*- coding: utf-8 -*-
import logging
from logging import getLogger

LOG_LEVEL = logging.DEBUG
LOG_FORMATTER = {'simple' : "%(asctime)s %(levelname)s %(name)s: %(message)s", 
                 'detail' : "%(asctime)s %(filename)s [%(lineno)d] [%(levelname)s] %(message)s",
                }

logging.addLevelName(100,'DISABLE')

def setBasicConfig(format=None,datefmt=None,level=None, detail_format=False):
    default_format = LOG_FORMATTER['detail'] if detail_format else LOG_FORMATTER['simple']
    format = format or default_format
    datefmt = datefmt or "%Y-%m-%d %H:%M:%S"
    level = level or logging.INFO
    
    logging.basicConfig(
        format=format,
        datefmt=datefmt,
        level=level,
        )

