# coding=utf-8

"""

    record.app
    ~~~~~~~~~~~~~~~~~~~
    Scan the current internet IP address allocated by your ISP and update the
    DNS records on Aliyun Cloud service according to your domain config file
    in order to bind the domain to your intranet server.

    :author: Charles Qi
    :license: BSD

"""

import os
import json
from error import Error
from cache import Cache
from ip import CurrentIP
from aliyunsdkcore.client import AcsClient
#from aliyunsdkcore.acs_exception.exceptions import ClientException
#from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest

class Record:

    """
        Record object is used to operate the Aliyun cloud service with the SDK
        provided by itself.

        :param client: This is an instance of Aliyun core SDK AcsClient class.

        :param domain: This is an dict object containing domain infomation
                       under the name of one Aliyun client.

    """

    def __init__(self, client, domain):
        self.client = client
        self.domain = domain
        self.cache = self.__get_cache('', '.' + domain['DomainName'])

    def get(self, rr, flush=False):
        record = ''

        if not flush:
            record = self.cache.get(rr)

        if len(record) == 0:

            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_action_name("DescribeDomainRecords")
            request.set_DomainName(self.domain['DomainName'])
            request.set_RRKeyWord(rr)
            request.set_TypeKeyWord('A')
            r = json.loads(self.client.do_action_with_exception(request))

            if 'DomainRecords' in r.keys():
                record = r['DomainRecords']['Record'][0]
                if len(record) == 0:
                    ip = CurrentIP()
                    value = ip.get_ip()
                    r = self.add(rr, value)
                    if r == '':
                        value = ''
                    else:
                        self.record_id = r
                else:
                    self.cache.set(rr, json.dumps(record))
                    self.record_id = record['RecordId']
                    value = record['Value']
            else:
                raise Error(r['Code'],r['Message'])

        else:
            record = json.loads(record)
            self.record_id = record['RecordId']
            value = record['Value']

        return value

    def set(self, rr, value):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_action_name("UpdateDomainRecord")
        request.set_RecordId(self.record_id)
        request.set_Type('A')
        request.set_RR(rr)
        request.set_Value(value)
        r = json.loads(self.client.do_action_with_exception(request))
        self.cache.remove(rr)
        try:
            if 'Code' in r.keys():
                raise Error(r['Code'], r['Message'])
        except Error(r['Code'], r['Message']):
            return False
        else:
            self.get(rr)
            return True

    def add(self, rr, value):
        request = AddDomainRecordRequest.AddDomainRecordRequest()
        request.set_action_name("AddDomainRecord")
        request.set_Type('A')
        request.set_RR(rr)
        request.set_Value(value)
        request.set_DomainName(self.domain['DomainName'])
        r = json.loads(self.client.do_action_with_exception(request))
        try:
            if 'Code' in r.keys():
                raise Error(r['Code'], r['Message'])
        except Error(r['Code'], r['Message']):
            return ''
        else:
            return r['RecordId']

    def __get_cache(self, key_prefix='', key_suffix=''):
        cache = Cache()
        cache.set_key_prefix(key_prefix)
        cache.set_key_suffix(key_suffix)
        return cache

class Update:

    """
        Update object is the entrance of the project.

        :property self.config: Converted dict object from the json config file
                               which will automatically generate when you create
                               the class instance.

        :param filename: The argument of string type is the the file name of
                         the domain config file, which should include the path.

    """

    def __init__(self, filename):
        self.__config(filename)

    def __config(self, filename):
        try:
            config = json.load(open(filename, "r"))
        except:
            raise Error('IOError','','','CRITICAL')
        else:
            self.config = config

    def all(self, flush=False):

        """
            :Scan all the clients and domains in the config file
             and update them according to the current public IP address.

        """

        clients = self.config['AliyunClients']
        for client in clients:
            self.client(client, flush)

    def client(self, client, flush=False):
        ali_client = AcsClient(
            client['AccessKeyID'],
            client['AccessKeySecret']
        )

        new_ip = self.__get_new_ip()

        for domain in client['Domains']:
            record = Record(ali_client, domain)
            for rr in domain['RRKeywords']:
                if rr == '':
                    rr == '@'
                if record.get(rr, flush) != new_ip:
                    record.set(rr, new_ip)

    def __get_new_ip(self):
        ip = CurrentIP()
        return ip.get_ip()
