#!/usr/bin/env python
#coding=utf-8

import os
from record import record

path = '/root/ddns/'
if os.path.exists(path):
    os.chdir(path)
config_file = 'settings.json'

task = record.Update(config_file)
task.all()
