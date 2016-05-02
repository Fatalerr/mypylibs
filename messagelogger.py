# -*- coding: utf-8 -*-
"""This class wrap the system logging module for easy used.


from logger import MessageLogger

logger = MessageLogger()

"""

__author__ = 'Liu Jun'
__date__   = '2013/x/x'
__version__ = '1.0'

import logging
from logging.handlers import RotatingFileHandler

LOG_FORMATTER = "%(asctime)s %(levelname)s %(name)s: %(message)s"
logging.addLevelName(100,'DISABLE')

class MessageLogger(object):
    """A customize and easy to used logging tools, only support stream(console) and file handler
    
    logger = MessageLogger('myname',logfile='myname.log',fmt='%(asctime)s,..')
    logger.formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    logger.debug('debug message')
    logger.info('info message')
    logger.critical('critical message')
    
    """
    def __init__(self,name,logfile="",maxbytes=1024*1024,backupcount=5,fmt=LOG_FORMATTER):
        logger = logging.getLogger(name)
        self.maxbytes = maxbytes
        self.backupcount = backupcount
        self.formatter = logging.Formatter(fmt,"%Y-%m-%d %H:%M:%S")
        self.handlers = {}
        
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()                                             
        ch.setFormatter(self.formatter)
        logger.addHandler(ch)
        self.logger = logger
        self.handlers['console'] = ch
        
        if logfile:
            self.setFileHandler(logfile)
            
    def setLevel(self,level):
        self.logger.setLevel(logging._levelNames.get(level,logging.DEBUG))
        #self.logger.setLevel(level)
    def getLevel(self):
        return self.logger.getEffectiveLevel()
    def addFileHandler(self,filename):
        handler = RotatingFileHandler(
                  filename, maxBytes=self.maxbytes,backupCount=self.backupcount)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        self.handlers['file'] = handler
        
    def setHandlerLevel(self,handlertype,level):
        """handlertype: 'console' or 'file' 
        level: 'DISABLE', 'DEBUG','INFO'...
        """
        self.handlers[handlertype].setLevel(logging._levelNames.get(level,logging.DEBUG))
        
    def debug(self,msg):
        self.logger.debug(msg)
    def info(self,msg):
        self.logger.info(msg)
    def error(self,msg):
        self.logger.error(msg)
    def critical(self,msg):
        self.logger.critical(msg)
        