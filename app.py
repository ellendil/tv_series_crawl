#!/usr/bin/python

import yaml

with open("config.yaml", 'r') as config_file:
  conf = yaml.load(config_file)
  print(conf)

  for entry in conf['tv_series']:
      print('Entry: ')
      print(entry['name'])
