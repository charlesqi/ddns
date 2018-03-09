import os
from error import Error
from shutil import rmtree

class Cache:

    db_prefix = '.cache'
    key_prefix = ''
    key_suffix = ''

    def __init__(self):
        self.select(0)

    def __check_path(self):
        if not(os.path.exists(self.cache_path)):
            os.mkdir(self.cache_path)

    def __prepare(self, key):
        filename = self.cache_path + '/'
        filename += self.key_prefix
        filename += key
        filename += self.key_suffix
        return filename

    def set_key_prefix(self, key_prefix):
        self.key_prefix = key_prefix

    def set_key_suffix(self, key_suffix):
        self.key_suffix = key_suffix

    def set_cache_path(self, cache_path):
        self.cache_path = cache_path

    def select(self, db):
        self.set_cache_path(self.db_prefix + str(db))

    def set(self, key, value):
        self.__check_path()
        key = self.__prepare(key)
        try:
            file_name = open(key, "w")
        except:
            raise Error('IOError')
        else:
            file_name.write(value)
            file_name.close()
            return True

    def get(self, key):
        value = ''
        key = self.__prepare(key)
        try:
            file_name = open(key, "r")
            value = file_name.read()
            file_name.close()
        except:
            raise Error('IOError')
        finally:
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
            rmtree(self.cache_path)
        except:
            raise Error('IOError')
        else:
            return True
