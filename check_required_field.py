# -*- coding:utf-8 -*-
import requests
import hashlib
session = requests.session()
session.get(u'http://221.226.253.51:5065/onlineGovQl/starshine/login.jsp')
md5 = hashlib.md5()
md5.update(u'123456')
password = md5.hexdigest()
print password
data = {u'jsu':u'RR1040_LR', u'jsp':password, u'jOrgNo':u''}
response = session.post(u'http://221.226.253.51:5065/onlineGovQl/j_spring_security_check', data=data)
print response

