# -*- coding: utf-8 -*-
"""This module handling the login info for the network elements

A typical Account will include a `username` and a `password`. both can be saved in a file with YAML format.
and the `password` will be encrypted.

Usage Examples:

- read the account information from YAML file.

   from loginfo import AccountFile
   
   accfile = AccountFile('hosts.yml')
   acc1 = accfile.account('user1')
   print "Account:",acc1
   print acc1.decrypt_password()
   
- encrypt/decrypt the password in a console:

    R:\git\mypylibs>python account.py encrypt
    Input the user name:root
    Input the password(max length 20):
    ==I5dmRISnZiM1J5YjI5MGNtOXZLMkZpWTJjbQUn

    R:\git\mypylibs>python account.py decrypt
    Input the username:root
    Input the encrypt password string:==I5dmRISnZiM1J5YjI5MGNtOXZLMkZpWTJjbQUn
      
"""
__author__ = 'Liu Jun'
__date__   = '2016/4/15'
__version__ = '1.0'

import yaml
import base64

userinfo_template = """
Username : %(username)s
Password : %(password)s
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
    try:
        p1 = base64.b64decode(_change_seq(ep))
        p2 = _change_seq(p1)
        p3 = base64.b64decode(p2)
    except Exception, err:
        #print "\nThe password might not be encrypted. return the original password."
        return ep
        
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

class Account(object):
    """A abstract class for all account.

    """
    fields = []
    _reprstr = "%(classname)s(%(username)s)"
    
    def __init__(self,**kwargs):       
        for field in self.fields:
            self.__dict__[field] = None
            
        for key,value in kwargs.items():
            self.__dict__[key] = value
            
    def encrypt_password(self,password=None):
        "encrypt the password of the user"
        if not password:
            password = self.password
        
        self.password = encrypt(self.username,password)
        
        return self.password
    
    def decrypt_password(self,password=None):
        "decrypt the password"
        if not password:
            password = self.password
        
        return decrypt(self.username,password)
        
    def load(self,acc_name):
        """Load the account(acc_name) data from the file(filename).
        """
        with file(filename) as fp:
            alldata = yaml.load(fp)
        
        data = alldata.get(acc_name,None)
        if not data:
            print "No such account:",acc_name
            return None
            
        for key in self.fields:
            self.__dict__[key] = data.get(key)
        
        return data
        
    def save(self,filename):
        """Save the fields data to a file.
        """
        data = {key:self.__dict__[key] for key in self.fields}
        with open(filename,'w') as fp:
            yaml.safe_dump(data,fp)
            
    def __repr__(self):
        _data = {'classname': self.__class__.__name__}
        _data.update((k,self.__dict__[k]) for k in self.fields)
        return self._reprstr % _data

class UserAccount(Account):
    fields = ['username','password']
    _reprstr = "%(classname)s(%(username)s,password=<%(password)s>)"
        
class HostAccount(UserAccount):
    fields = ['hostname','ipaddr','username','password']
    _reprstr="%(classname)s(%(hostname)s,user=%(username)s)"

class MailAccount(UserAccount):
    fields = ['description','smtp','pop3','username','password']
    _reprstr="%(classname)s(%(description)s)"
    
class AccountFile(object):
    """Read the account info from the YAML file.
    """
    def __init__(self,filename):
        with file(filename) as fp:
            self.data = yaml.load(fp)
        
    def get(self,account_name):
        """Get the account data of account_name.
        """
        return self.data.get(account_name)
    
    def add(self,account_data):
        """Add a account data to AccountFile.
        """
        self.data.update(account_data)
    
    def account(self,account_name):
        """Return the account instance of account_name.
        """
        data = self.get(account_name)
        if not data:
            return Account()
               
        account_type = data.get('_type')
        if account_type not in globals():
            fields = data.keys()
            account_class = type(data['_type'],(Account,),{'fields':fields})
        else:
            account_class = globals().get(account_type)
        
        return account_class(**data)
        
    def save(self):
        """Save the accounts to the file.
        """
        pass


if __name__ == "__main__":
    accfile = AccountFile("hostaccount.yml")
    
    acc1 = accfile.account('smartchecker')
    print acc1,acc1.decrypt_password(),acc1.smtp,acc1.pop3
    print 
    
    
    acc2=accfile.account('tester')
    print "account2:", acc2
    print acc2.password, acc2.decrypt_password()
    #acc2.save('hostaccount.yml')
    

