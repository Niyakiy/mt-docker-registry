#!/usr/bin/env python

import jinja2
import yaml
import sys 
import os
import random

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
config_dir = script_dir+'/../config'
template_path = script_dir+'/../templates'

try:
  CONFIG = yaml.load(open("{config_path}/config.yml".format(config_path=config_dir), 'r'))
except:
  print "[ERROR] Unable to read config!"


tenants = CONFIG['tenants']
root_path = CONFIG['mtregistry_root_path']

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
