#!/usr/bin/env python
# coding: utf-8

import os
import sys
from record import record

os.chdir(sys.path[0])
config_file = 'settings.json'

task = record.Update(config_file)
task.all()
