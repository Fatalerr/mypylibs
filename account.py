# -*- coding: utf-8 -*-
"""This module handling the login info for the network elements

A typical Account will include a `username` and a `password`. both can be saved in a file with YAML format.
and the `password` will be encrypted.

Usage Examples:

- encrypt/decrypt the password in a console:

    R:\git\mypylibs>python account.py encrypt
    Input the user name:root
    Input the password(max length 20):
    ==I5dmRISnZiM1J5YjI5MGNtOXZLMkZpWTJjbQUn

    R:\git\mypylibs>python account.py decrypt
    Input the username:root
    Input the encrypt password string:==I5dmRISnZiM1J5YjI5MGNtOXZLMkZpWTJjbQUn
    abcdk
    
-   

"""
__author__ = 'Liu Jun'
__date__   = '2016/4/15'
__version__ = '0.1'

import yaml
import base64

userinfo_template = """
Username : %(username)s
Password : %(password)s
Password : %(_clear)s
"""
### Note: the max password length should not exceed the PASSWD_LENGTH! ###
PASSWD_LENGTH = 20


### core functions for encrypt&decrypt ###
def _change_seq(s):
    #return s[1] + s[0] + s[2:]
    d=2
    return s[-d:] + s[d:-d] + s[:d]

def encrypt(username,passwd):
    """This function encrypt the password for the user and return to the caller.
    
    Notice: the length of passwd should not more than PASSWD_LENGTH!!
    """

    m = (PASSWD_LENGTH-len(passwd))/len(username)
    n = (PASSWD_LENGTH-len(passwd)) % len(username)

    p1 = username*m + username[:n] + '+' + passwd
    #print p1  ##comment this line if debug is not need.
    ep1 = base64.b64encode(p1)
    ep2 = _change_seq(ep1)
    ep3 = base64.b64encode(ep2)

    return _change_seq(ep3)

def decrypt(username,ep):
    """This function decrypt the password for the user and return to the caller.
    
    Notice: the length of passwd should not more than PASSWD_LENGTH!!
    """
    p1 = base64.b64decode(_change_seq(ep))
    p2 = _change_seq(p1)
    p3 = base64.b64decode(p2)

    return p3[p3.find('+')+1:]
### end of core functions ###

def encrypt_password():
    """An convenient way to encrypt the password in interact senerios
    """
    import getpass
    username = raw_input("Input the user name:")
    password = getpass.getpass('Input the password(max length %s): ' % PASSWD_LENGTH)
    if len(password) > PASSWD_LENGTH:
        print "the max length of your password has exceed the %s!" % PASSWD_LENGTH
        return None
    return encrypt(username,password)

def decrypt_password():
    username = raw_input("Input the username:")
    ep = raw_input("Input the encrypt password string:")
    try:
        cp=decrypt(username,ep)
    except TypeError:
        print "the encrypt string is not vaild!"
        sys.exit(1)
    return cp

class AccountInfo(object):
    """User account management.

    """
    def __init__(self,username='',password=''):
        self.username = username
        self.password = password


    def __repr__(self):
        return "AccountInfo(%s)" % self.username

def load_accounts(accfile):
    with file(accfile) as fp:
        data = yaml.load(fp)

    for host,info in data.items():
        print host, info

def _test_read_from_file():
    """

    Returns:
        object: a list of AccountInfo
    """
    accounts = load_accounts('hosts.yml')

    for acc in accounts:
        print userinfo_template % acc.__dict__

if __name__ == "__main__":
    acc1 = AccountInfo('root')
    acc1.password = 'impassword'
    #_test_read_from_file()

    import sys

    if len(sys.argv)<2:
        print "Usage: account encrypt|decrypt"
        exit(1)

    if sys.argv[1] == 'encrypt':
        print encrypt_password()
    if sys.argv[1] == 'decrypt':
        print decrypt_password()


