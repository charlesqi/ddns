import os
import json
from error import Error
from time import time
from shutil import rmtree

class Cache:

    db_prefix = '.cache'

    def __init__(self, key_prefix='', key_suffix=''):
        self.key_prefix = key_prefix
        self.key_suffix = key_suffix
        self.select()

    def __check_dir(self):
        if not(os.path.exists(self.__dir)):
            os.mkdir(self.__dir)

    def __prepare(self, key):
        return self.__dir + '/' + self.key_prefix + key + self.key_suffix

    def select(self, db=0):
        self.db = db
        self.__dir = WORKING_DIRECTORY + self.db_prefix + str(self.db)
        self.__check_dir()

    def set(self, key, value):
        key = self.__prepare(key)
        try:
            file_name = open(key, "w")
        except Error('IOError') as e:
            print(e.message)
            return False
        else:
            file_name.write(value)
            file_name.close()
            return True

    def get(self, key):
        value = ''
        key = self.__prepare(key)
        if os.path.exists(key):
            try:
                file_name = open(key, "r")
            except:
                raise Error('IOError')
            else:
                value = file_name.read()
                file_name.close()
        return value

    def remove(self, key):
        key = self.__prepare(key)
        try:
            os.remove(key)
        except:
            raise Error('IOError')
        else:
            return True

    def flush(self):
        try:
            rmtree(self.__dir)
        except:
            raise Error('IOError')
        else:
            return True
