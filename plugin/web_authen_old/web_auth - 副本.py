# -*- coding:utf-8 -*-

import sys
import rpyc
import time
import logging
import traceback
import gc
import random
import threading
import colorama
import re


class UploadPlugin(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)  
        self.ip = ip 

    def run(self):
        try:
            client = rpyc.classic.connect(self.ip)
            rpyc.classic.upload_dir(client, 'plugin', 'plugin')
            logging.info("%s finish upload plugin!"%self.ip)

        except Exception,e:
            logging.error("%s upload plugin failed! Error message: %s"%(self.ip,e))

def upload_plugin(iplist):
    logging.info("upload the bmp package to remote pc, wait...")
    client = {}
    iplist = sorted(iplist)
    for ip in iplist:
        print ip
        client[ip] = UploadPlugin(ip)
        
    for ip in iplist:
        client[ip].start()
    
    for ip in iplist:
        client[ip].join()
        
    gc.collect()

    
# build remote connection for browsing web, return a dictionary of remote function object
def get_all_ip():
    all_ip = []
    fp = open('./plugin/web_authen/ip.txt','r')
    for line in fp:
        all_ip = all_ip + re.findall('\d+.\d+.\d+.\d+', line)
    return all_ip

def remote_local_web_authen():
    client = {} 
    rfunc = {} 
    rresult = {}
    start_time = time.time()

    all_ip = get_all_ip()
    num = raw_input('How many PCs you choice (total %s): '%len(all_ip))
    while 1:
        try: 
            assert int(num) <= len(all_ip)
            break
        except Exception:
            num = raw_input('Input a right number (total %s): '%len(all_ip))
    iplist = all_ip[0:int(num)]
    interval = raw_input('Please input the interval between twice authentication: ')
    
    logging.info("Build remote connection for web authentication...")
    for ip in iplist:
        try:
            client[ip] = rpyc.classic.connect(ip)
            rfunc[ip] = rpyc.async(client[ip].modules["plugin.web_authen.LocalWebAuthen"].local_web_authen) 
            client[ip].modules.imp.reload(client[ip].modules["plugin.web_authen.LocalWebAuthen"])
            #logging.info("Build %s remote control succeed!"%ip)
        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(ip,e))
    
    # start the remote task, return a dictionary of remote function running object
    ipl = sorted(rfunc.keys())
    for ip in ipl:
        rresult[ip] = rfunc[ip]()
        logging.info("Build %s remote control succeed!"%ip)
        time.sleep(float(interval))

    time.sleep(1)
    iplist2 = all_ip[int(num):int(num)*2]
    client2 = {} 
    rfunc2 = {} 
    rresult2 = {}
    for ip in iplist2:
        try:
            client2[ip] = rpyc.classic.connect(ip)
            rfunc2[ip] = rpyc.async(client2[ip].modules["plugin.web_authen.LocalWebAuthen"].local_web_authen) 
            client2[ip].modules.imp.reload(client2[ip].modules["plugin.web_authen.LocalWebAuthen"])
            #logging.info("Build %s remote control succeed!"%ip)
        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(ip,e))
    
    # start the remote task, return a dictionary of remote function running object
    ipl2 = sorted(rfunc2.keys())
    for ip in ipl2:
        rresult2[ip] = rfunc2[ip]()
        logging.info("Build %s remote control succeed!"%ip)
        time.sleep(float(interval))
        
    while rresult2:
        for ip in rresult2.keys():
            if rresult2[ip].ready:
                logging.info('Web Authentication %s result: %s'%(ip,rresult2[ip].value))
                rresult2.pop(ip)
        time.sleep(1)
        
    for ip in client.keys():
        client[ip].close()
    for ip in client2.keys():
        client2[ip].close()
    
def remote_wx_web_authen():
    
    client = {} 
    rfunc = {} 
    rresult = {}
    start_time = time.time()
    
    
    all_ip = get_all_ip()
    num = raw_input('How many PCs you choice(total %s): '%len(all_ip))
    while 1:
        try: 
            assert int(num) <= len(all_ip)
            break
        except Exception:
            num = raw_input('Input a right number (total %s): '%len(all_ip))
    iplist = all_ip[0:int(num)]
    url = raw_input('Please input the Portal url: ')
    interval = raw_input('Please input the interval between twice authentication: ')

    logging.info("Build remote connection for web authentication...")
    for ip in iplist:
        try:
            client[ip] = rpyc.classic.connect(ip)
            rfunc[ip] = rpyc.async(client[ip].modules["plugin.web_authen.WxWebAuthen"].wx_web_authen) 
            client[ip].modules.imp.reload(client[ip].modules["plugin.web_authen.WxWebAuthen"])

        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(ip,e))

    ipl = sorted(rfunc.keys())
    for ip in ipl:
        rresult[ip] = rfunc[ip](url)
        logging.info("Build %s remote control succeed!"%ip)
        time.sleep(float(interval))
    
    # start the remote task, return a dictionary of remote function running object
    
    time.sleep(3)
    print '**************************************'
    client2 = {} 
    rfunc2 = {} 
    rresult2 = {}
    iplist2 = all_ip[int(num):int(num)*2]
    for ip in iplist2:
        try:
            client2[ip] = rpyc.classic.connect(ip)
            rfunc2[ip] = rpyc.async(client2[ip].modules["plugin.web_authen.WxWebAuthen"].wx_web_authen) 
            client2[ip].modules.imp.reload(client2[ip].modules["plugin.web_authen.WxWebAuthen"])

        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(ip,e))

    ipl2 = sorted(rfunc2.keys())
    for ip in ipl2:
        rresult[ip] = rfunc2[ip](url)
        logging.info("Build %s remote control succeed!"%ip)
        time.sleep(float(interval))
    
    # start the remote task, return a dictionary of remote function running object

    while rresult:
        for ip in rresult.keys():
            if rresult[ip].ready:
                logging.info('Web Authentication %s result: %s'%(ip,rresult[ip].value))
                rresult.pop(ip)
            time.sleep(1)
            
    while rresult2:
        for ip in rresult2.keys():
            if rresult2[ip].ready:
                logging.info('Web Authentication %s result: %s'%(ip,rresult2[ip].value))
                rresult2.pop(ip)
            time.sleep(1)
        
    for ip in client.keys():
        client[ip].close()
    for ip in client2.keys():
        client2[ip].close()
            
def remote_advert_web_auth():
    print 'Not support!'


def log_out():
    
#    cur_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())

    logging.getLogger().setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logging.getLogger().addHandler(sh)
    
#    co = colorhandler.ColorHandler(sys.stderr)
#    co.setFormatter(formatter)
    
#     fh = logging.FileHandler('./log/consolePC/%s.log'%cur_time)
#     fh.setFormatter(formatter)
    
#     logging.getLogger().addHandler(co)
#     logging.getLogger().addHandler(fh)
    
def main():
    
    operations = '''Operations:
1    Local Web Authentication
2    Weixin Web Authentication
3    Advert Web Authentication
'''

    log_out()
    iplist = get_all_ip()
    while True:
        print operations
        operation = raw_input('>>> ')
        if operation == '1': 
            remote_local_web_authen()
        
        elif operation == '2':
            remote_wx_web_authen()
            
        elif operation == '3':
            remote_advert_web_auth()

        elif operation == '4':
            upload_plugin(iplist)
            
        else:
            
            print('Please input current operation!')
            print(operations)
        
if __name__ == '__main__':

    try:
        #print get_all_ip()
        main()
    except Exception:
        traceback.print_exc()
