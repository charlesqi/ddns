#!/usr/bin/env python
#coding=utf-8

from record import record

WORKING_DIRECTORY = '/root/ddns/'
MODULE_DIRECTORY = WORKING_DIRECTORY + 'module/'

config_file = WORKING_DIRECTORY + 'domain.json'

task = record.Update(config_file)
task.all()
