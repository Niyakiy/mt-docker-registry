#!/usr/bin/env python

import jinja2

root_path = "/var/mt-docker-registry"

tenants = [
  {'name': 'cisco', 'port': 5001},
  {'name': 'databricks', 'port': 5002}
]

tmpl = jinja2.Template(open('../templates/tenant-proxy-config.conf.j2').read())
open("{path}/config/tenant-proxy-config.conf".format(path=root_path), "w").write(tmpl.render({'tenants': tenants, 'root_path': root_path}))

tmpl = jinja2.Template(open('../templates/docker-compose.yml.j2').read())
open("{path}/docker-compose.yml".format(path=root_path), "w").write(tmpl.render({'tenants': tenants, 'root_path': root_path}))
