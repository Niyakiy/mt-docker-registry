#!/usr/bin/env python

import jinja2
import yaml
import sys 
import os
import random

def ckeckAndCreateDirLayout(root_path):
  for dir in ['auth', 'config', 'registries']:
    path = root_path + '/' + dir
    if not os.path.exists(path):
      os.makedirs(path)

def loadConfigs(conf_file):
  try:
    return yaml.load(open(conf_file, 'r'))
  except:
    return None
           

if __name__ == '__main__':

  script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
  config_dir = script_dir+'/../config'
  template_path = script_dir+'/../templates'

  CONFIG = loadConfigs("{config_path}/config.yml".format(config_path=config_dir))
  if not CONFIG:
    print "[ERROR] Unable to read config!"
    sys.exit(1)


  tenants = CONFIG['tenants']
  root_path = CONFIG['mtregistry_root_path']

  # Checking if nessesary directories are present
  ckeckAndCreateDirLayout(root_path)

  try:
    tmpl = jinja2.Template(open('{template_path}/tenant-proxy-config.conf.j2'.format(template_path=template_path)).read())
    open("{path}/config/tenant-proxy-config.conf".format(path=root_path), "w").write(tmpl.render({'tenants': tenants, 'root_path': root_path}))
  except:
    print "[ERROR] Unable to render tenant proxy template!"

  try:
    tmpl = jinja2.Template(open('{template_path}/docker-compose.yml.j2'.format(template_path=template_path)).read())
    open("{path}/docker-compose.yml".format(path=root_path), "w").write(tmpl.render({'tenants': tenants, 'root_path': root_path}))
  except:
    print "[ERROR] Unable to render tenant proxy template!"
