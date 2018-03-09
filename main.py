#!/usr/bin/env python
#coding=utf-8

from record import record

config_file = 'domain.json'

task = record.Update(config_file)
task.all()
