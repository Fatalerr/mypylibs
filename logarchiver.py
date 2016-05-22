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
import os
import re
import sys
import shutil
from zipfile import is_zipfile,ZipFile
from rarfile import is_rarfile,RarFile

project_pat = re.compile("(\w+(?:CUC|MCC))")
archive_pat = re.compile("\.(rar|zip|gz|txt|log)")
logfile_pat = re.compile("\.(txt|log)")

is_logfile = lambda fname: logfile_pat.search(fname)
is_archive = lambda fname: archive_pat.search(fname)

def get_project_name_from_filename(filename):
    prjnames = project_pat.findall(filename)
    if prjnames:
        return prjnames[0]
    else:
        return ''

def get_archive_files(logdir):
    return [f for f in os.listdir(logdir) if is_archive(f)]
    
def decompress(zfilename,targetpath):
    zfile = ArchivedFile(zfilename)
    zfile.extractall(targetpath)      

def compress_to_zipfile(targetdir, savename):
    zipcmd = "/usr/bin/zip -r -D %(zipfilename)s %(target)s/*"
    result = os.system(zipcmd % dict(zipfilename=savename,target=targetdir))

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
        project_name = get_project_name_from_filename(dfile)
        srcfile = os.path.join(logdir,dfile)
        dstdir = os.path.join(tmpdir,project_name)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        if is_logfile(dfile):
            print "Move logfile: %s --> %s" % (dfile,dstdir)
            shutil.move(srcfile,dstdir)
            continue
        else:
            print "extract compress file:%s --> %s" % (dfile,os.path.join(tmpdir,project_name))
            decompress(srcfile,dstdir)

if __name__ == "__main__":
   if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    
   logdir,destdir = sys.argv[1:]
    
   decompress_archived_files(logdir,destdir)            