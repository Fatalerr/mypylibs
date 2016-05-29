# -*- coding: utf-8 -*-
"""This class wrap the system logging module for easy used.


from logger import MessageLogger

logger = MessageLogger(logname)
logger.

"""

__author__ = 'Liu Jun'
__date__   = '2013/x/x'
__version__ = '1.0'

import logging
from logging.handlers import RotatingFileHandler

LOG_FORMATTER = "%(asctime)s %(levelname)s %(name)s: %(message)s"
logging.addLevelName(100,'DISABLE')

def setBasicConfig(format=None,datefmt=None,level=None):
    format = format or LOG_FORMATTER
    datefmt = datefmt or "%Y-%m-%d %H:%M:%S"
    level = level or logging.INFO
    
    logging.basicConfig(
        format=format,
        datefmt=datefmt,
        level=level,
        )

class MessageLogger(object):
    """A customize and easy to used logging tools, only support stream(console) and file handler
    
    logger = MessageLogger('myname',logfile='myname.log',fmt='%(asctime)s,..')
    logger.formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    logger.debug('debug message')
    logger.info('info message')
    logger.critical('critical message')
    
    """
    root = logging.getLogger()
    
    def __init__(self,name=None,logfile="",maxbytes=1024*1024,backupcount=5,fmt=LOG_FORMATTER):       
        self.maxbytes = maxbytes
        self.backupcount = backupcount
        self.formatter = logging.Formatter(fmt,"%Y-%m-%d %H:%M:%S")
        self.handlers = {}
        
        self.logger = logging.getLogger(name)        
        #self.logger.setLevel(logging.INFO)

        if not name:
            setBasicConfig()
            
        # ch = logging.StreamHandler()                                             
        # ch.setFormatter(self.formatter)
        # logger.addHandler(ch)
        #self.handlers['console'] = ch
        
        if logfile:
            self.addFileHandler(logfile)
            
    def setLevel(self,level):
        self.logger.setLevel(logging._levelNames.get(level,logging.DEBUG))
        #self.logger.setLevel(level)
    
    def getLevel(self):
        return self.logger.getEffectiveLevel()
    
    def addFileHandler(self,filename,root=False):
        handler = RotatingFileHandler(
                  filename, maxBytes=self.maxbytes,backupCount=self.backupcount)
        handler.setFormatter(self.formatter)
        if root:
            self.root.addHandler(handler)
        else:
            self.logger.addHandler(handler)
            self.handlers['file'] = handler
        
    def setHandlerLevel(self,handlertype,level,root=False):
        """handlertype: 'console' or 'file' 
        level: 'DISABLE', 'DEBUG','INFO'...
        """
        if root:
            self.root.setLevel(logging._levelNames.get(level,logging.DEBUG))
        else:
            self.handlers[handlertype].setLevel(logging._levelNames.get(level,logging.DEBUG))
        
    def debug(self,msg):
        self.logger.debug(msg)
    def info(self,msg):
        self.logger.info(msg)
    def error(self,msg):
        self.logger.error(msg)
    def critical(self,msg):
        self.logger.critical(msg)
        