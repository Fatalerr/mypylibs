#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Uncompress the archive files to the <detdir>

supported archive format:
  - zip
  - rar
  
Usage:
    logarchiver  <logfile|logdir> <dest_dir>
"""
import os,re
import sys,logging
import shutil
from zipfile import is_zipfile,ZipFile
from rarfile import is_rarfile,RarFile

archive_pat = re.compile("\.(rar|zip|gz|txt|log)")
logfile_pat = re.compile("\.(txt|log)")

keyword_pat = re.compile("(\w+(?:CUC|MCC))")

is_logfile = lambda fname: logfile_pat.search(fname)
is_archive = lambda fname: archive_pat.search(fname)

logger = logging.getLogger('logarchiver')

def get_keyword_from_filename(kwpattern,filename):
    kwnames = re.findall(filename)
    if kwnames:
        return kwnames[0]
    else:
        return ''

def get_archive_files(logdir):
    return [f for f in os.listdir(logdir) if is_archive(f)]
    
def decompress(zfilename,targetpath):
    zfile = ArchivedFile(zfilename)
    zfile.extractall(targetpath)      

def compress_to_zipfile(targetdir, savename):
    zipcmd = "/usr/bin/zip -r -D %(zipfilename)s %(target)s/*"
    result = os.system(zipcmd % dict(zipfilename=savename,target=os.path.abspath(targetdir)))

    if result == 0:
        return "Success"
    else:
        return "Failed"

class ArchivedFile(object):
    def __init__(self,filename):
        if is_zipfile(filename):
            self._zfile = ZipFile(filename)
        elif is_rarfile(filename):
            self._zfile = RarFile(filename)
        
    def filelist(self):
        return self._zfile.namelist()
        
    def extract(self,srcfile,targetpath):
        "extract srcfile in archive to targetpath"
        for fullfilename in self.filelist():
            if srcfile in fullfilename:
                fpath,fname = os.path.split(fullfilename)
                self._zfile.extract(fname.encode('gbk'),targetpath+fname)
                return True

        return None
    def extractall(self,targetpath):
        self._zfile.extractall(targetpath)

def get_text_from_file(filename):
    with open(filename) as fp:
        logtxt = "".join(fp.readlines())
    return logtxt
    
def decompress_archived_files(logdir, tmpdir):
    """decompress the archived files or move log files to temporal directory.
    """
    for dfile in get_archive_files(logdir):
        project_name = get_keyword_from_filename(keyword_pat,dfile)
        srcfile = os.path.join(logdir,dfile)
        dstdir = os.path.join(tmpdir,project_name)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        if is_logfile(dfile):
            logger.info("Move logfile: %s --> %s" % (dfile,dstdir))
            shutil.move(srcfile,dstdir)
            continue
        else:
            logger.info("extract compress file:%s --> %s" % (dfile,os.path.join(tmpdir,project_name)))
            decompress(srcfile,dstdir)

if __name__ == "__main__":
   if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    
   logdir,destdir = sys.argv[1:]
    
   decompress_archived_files(logdir,destdir)            