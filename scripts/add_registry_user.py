#!/usr/bin/env python

import yaml
import sys 
import os
import random
from optparse import OptionParser

def loadConfigs(conf_file):
  try:
    return yaml.load(open(conf_file, 'r'))
  except:
    return None

try:
    import crypt
except ImportError:
    try:
        import fcrypt as crypt
    except ImportError:
        sys.stderr.write("Cannot find a crypt module.  "
                         "Possibly http://carey.geek.nz/code/python-fcrypt/\n")
        sys.exit(1)


def salt():
    """Returns a string of 2 randome letters"""
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789/.'
    return random.choice(letters) + random.choice(letters)

def prepareHash(password):
  try:
    return crypt.crypt(password, salt())
  except:
    return None

def loadCurrentUsers(auth_file_path):
  try:
    auth_file = open(auth_file_path, 'r')
  except:
    return None
    
  return [line.strip().split(':') for line in auth_file.readlines()]
     
def saveUsers(auth_file_path, user_data):
  try:
    auth_file = open(auth_file_path, 'w')
    auth_file.writelines(
      ["%s:%s" % (user[0], user[1]) for user in user_data]
    )
  except:     
    return False
    
          
if __name__ == '__main__':

  tenant_name = sys.argv[1]
  user_name = sys.argv[2]
  password = sys.argv[3]

  password_hash = prepareHash(password)

  script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
  config_dir = script_dir+'/../config'
  template_path = script_dir+'/../templates'

  CONFIG = loadConfigs("{config_path}/config.yml".format(config_path=config_dir))
  if not CONFIG:
    print "[ERROR] Unable to read config!"
    sys.exit(1)

  tenants = CONFIG['tenants']
  root_path = CONFIG['mtregistry_root_path']
  
  auth_file_path = root_path+'/auth/'+tenant_name+'.htpasswd'
  curr_users = loadCurrentUsers(auth_file_path)
  if not curr_users:
    curr_users = [[user_name, password_hash]]
  else:
    existing_user = False
    for user in curr_users:
      if user[0] == user_name:
        existing_user = True
        user[1] = password_hash
    if not existing_user:
      curr_users.append([user_name, password_hash])
        

  saveUsers(auth_file_path, curr_users)
