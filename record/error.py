import json
import logging
import logging.config

class Error(Exception):

    def __init__(self, errcode='', errmsg='', special='', level='WARN'):
        Exception.__init__(self)
        self.__errtype_file = 'record/error.json'
        self.set_level(level)
        self.set_message(errcode, errmsg, special)
        self.log()

    def set_message(self, errcode, errmsg, special):
        if errcode == '':
            if not errmsg == '':
                self.message = errmsg
        else:
            if errmsg == '':
                err_file = open(self.__errtype_file, 'r')
                custom_types = json.load(err_file)
                err_file.close()
                if errcode in custom_types.keys():
                    if '%s' in custom_types[errcode]:
                        self.message = custom_types[errcode] % special
                    else:
                        self.message = custom_types[errcode]
                else:
                    self.message = 'Unknown customized error occured.'
            else:
                self.message = errmsg

    def set_level(self, level):
        self.level = level

    def set_logger(self):
        logging.config.dictConfig(json.load(open('record/logging.json', 'r')))
        self.logger = logging.getLogger()

    def log(self):
        if not hasattr(self, 'logger'):
            self.set_logger()
        eval('self.logger.' + self.level.lower() + '("' + self.message +'")')
