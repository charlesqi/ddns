#!/usr/bin/env python
# coding= utf-8

import os
import json
from urllib2 import urlopen
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest 
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest

class DnsHandler:
    # 从阿里云开发者后台获取区域ID、Access_Key_Id和Access_Key_Secret
    region_id = "cn-qingdao"
    access_key_id = "LTAIa62kuR1fqwRL"
    access_key_secret = "63CsfaXsjQE2TXMDhlWtuHl4v4onXq"

    # 填入自己的域名
    domain_name = "qdjiehun.cn"
    # 填入二级域名的RR值
    rr_keyword = "miyu"

    # version为阿里云SDK的版本，此处为"2015-01-09"
    version = "2015-01-09"

    # 解析记录类型，一般为A记录
    record_type = "A"

    # 用于储存解析记录的文件名
    file_name = ".ip_addr"

    client = None
    record = None
    current_ip  = ''

    def __init__(self):
        self.client = AcsClient(
            self.access_key_id,
            self.access_key_secret,
            self.region_id
        )
        self.record = self.get_record()
        self.current_ip = self.get_current_ip()

    def reset(self):
        if self.current_ip <> self.get_record_value():
            print self.update_record(self.current_ip)
            self.get_record()

    def get_record(self):
        if os.path.isfile(self.file_name) :
            file_handler = open(self.file_name, 'r')
            r = file_handler.read()
            file_handler.close()
        else :
            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_PageSize(10)
            request.set_version(self.version)
            request.set_action_name("DescribeDomainRecords")
            request.set_DomainName(self.domain_name)
            request.set_RRKeyWord(self.rr_keyword)
            request.set_TypeKeyWord(self.record_type)
            r = self.client.do_action_with_exception(request)
            file_handler = open(self.file_name, 'w')
            file_handler.write(r)
            file_handler.close()
        return json.loads(r)
    
    def get_record_id(self) :
        return self.record["DomainRecords"]["Record"][0]["RecordId"]

    def get_record_value(self) :
        return self.record["DomainRecords"]["Record"][0]["Value"]

    def update_record(self, value):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_version(self.version)
        request.set_action_name("UpdateDomainRecord")
        request.set_RecordId(self.get_record_id())
        request.set_Type(self.record_type)
        request.set_RR(self.rr_keyword)
        request.set_Value(value)
        return self.client.do_action_with_exception(request)

    def get_current_ip(self):
        return json.load(urlopen('http://jsonip.com'))['ip']
        
dns = DnsHandler()
dns.reset()
