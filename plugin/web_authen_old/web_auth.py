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


# build remote connection for browsing web, return a dictionary of remote function object
def get_all_ip():
    all_ip = []
    fp = open('ip.txt','r')
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
        time.sleep(interval)
        
    while rresult:
        for ip in rresult.keys():
            if rresult[ip].ready:
                logging.info('Web Authentication %s result: %s'%(ip,rresult[ip].value))
                rresult.pop(ip)
        time.sleep(1)
        
    for ip in client.keys():
        client[ip].close()
    
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
        time.sleep(interval)
    
    # start the remote task, return a dictionary of remote function running object
    while rresult:
        for ip in rresult.keys():
            if rresult[ip].ready:
                logging.info('Web Authentication %s result: %s'%(ip,rresult[ip].value))
                rresult.pop(ip)
            time.sleep(1)
        
    for ip in client.keys():
        client[ip].close()
            
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
    while True:
        print operations
        operation = raw_input('>>> ')
        if operation == '1': 
            remote_local_web_authen()
        
        elif operation == '2':
            remote_wx_web_authen()
            
        elif operation == '3':
            remote_advert_web_auth()
            
        else:
            
            print('Please input current operation!')
            print(operations)
        
if __name__ == '__main__':

    try:
        main()
    except Exception:
        traceback.print_exc()
