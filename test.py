# -*- coding: utf-8 -*-

#!/usr/bin/python

import smtplib

sender = 'xingjunbj@qq.com'
receivers = ['xingjun@hfvast.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP_SSL('smtp.qq.com',465)
   smtpObj.login('xingjun','xyjp2008')
   smtpObj.sendmail(sender, receivers, message)
   print "Successfully sent email"
except Exception,e:
   print e
   print "Error: unable to send email"


'''
import smtplib
import string
HOST = "smtp.uinx.com.cn"
SUBJECT = "Test email from Python"
#TO = "yafeng.jin@archermind.com"
#TO = "desheng.shi@archermind.com"
TO = "xingjunbj@qq.com"
FROM = "sh331902@126.com"
text = "Pyhon rules them all!"
BODY = string.join((
    "From:  %s" % FROM,
    "To:   %s" % TO,
    "Subject:    %s" % SUBJECT,
    " ",
    text
), "\r\n")
server = smtplib.SMTP()
server.connect(HOST, "25")
# server.starttls()
server.login("sh331902@126.com", "xyjp2008")
server.sendmail(FROM, [TO], BODY)
server.quit
'''