#coding=utf-8

import re
import urllib2
from error import Error

class CurrentIP:

    def __init__(self, detectors):
        self.set_timeout(3)
        self.set_detectors(detectors)

    def set_timeout(self, timeout):
        self.__timeout = timeout

    def set_detectors(self, proxy_pool):
        self.__detectors = proxy_pool

    def get_ip(self):
        ip = ''
        i = 0
        while len(ip) == 0 or i == len(self.__detectors):
            ip = self.__get_from_proxy(self.__detectors[i])
            i = i + 1
        if len(ip) == 0:
            raise Error('IPRequestError', '', '', 'CRITICAL')
        else:
            return ip

    def __get_from_proxy(self, url):
        ip = ''
        if re.match('^http', url) == None:
            url = 'http://' + url
        try:
            doc = urllib2.urlopen(url, timeout = self.__timeout).read()
        except:
            raise Error("TimeoutError", '', url)
        else:
            pattern = '(?!(((0)|(10)|(127)|(192\.168)|(172\.(1[6-9])|(2[0-9])|(3[01])))|(2[4,5][0-5])))'
            pattern += '((1[0-9][0-9]\.)|(2[0-4][0-9]\.)|(25[0-5]\.)|([1-9][0-9]\.)|([0-9]\.)){3}'
            pattern += '((1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])|([1-9][0-9])|([0-9]))'
            pattern = re.compile(pattern)
            result = pattern.search(doc)
            if result == None:
                raise Error('ReturnValueError', '', url)
            else:
                ip = result.group(0)
        finally:
            return ip
