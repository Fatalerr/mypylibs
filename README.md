# mypylibs

A python libs include common functions for my projects.

- MessageLogger
  A logging wrapper for simplifying the native logging tool. 
  
- NetAccount
  store and manage the network host login and account information.
  
- logarchiver
  Uncompress the archive(zip or rar) files to the <detdir>

````  
    supported archive format:
      - zip
      - rar
    Usage:
    # in console
        logarchiver  <logfile|logdir> <dest_dir>
        
    # in code
    from logarchiver import decompress_archived_files, compress_to_zipfile
    
    decompress_archived_files(tempdir['attachments'],tempdir['logfiles'])
    
````