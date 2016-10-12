import sys
import time
import logging
import rpyc
import traceback 
import config

def log_out():
    
#    cur_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())

    logging.getLogger().setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logging.getLogger().addHandler(sh)

def check_connection():
    iplist = config.IPLIST
    for ip in iplist:
        try:
            con = rpyc.classic.connect(ip)
            logging.info("Build %s remote control success!"%ip)
            con.close()
        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(ip,e))

def remote_mail_authen():
    client = {} 
    rfunc = {} 
    rresult = {}
    start_time = time.time()

    all_user = config.USERLIST
    all_ip = config.IPLIST
    num = raw_input('How many PCs are you choice? (total %s): '%len(all_ip))
    while 1:
        try: 
            assert int(num) <= len(all_ip)
            break
        except Exception:
            num = raw_input('Input a right number (total %s): '%len(all_ip))
    iplist = all_ip[0:int(num)]
    interval = raw_input('Input the interval between twice authentication: ')
    user_flag = raw_input('Whether to use a single mail? (y/n)(default:n): ')
    
    logging.info("Build remote connection for web authentication...")
    for ip in iplist:
        try:
            client[ip] = rpyc.classic.connect(ip)
            try:
                if not client[ip].modules.os.path.exists('./plugin/'):
                    client[ip].modules.os.mkdir('./plugin/')
                rpyc.classic.upload(client[ip], './__init__.py', './plugin/__init__.py')
                if not client[ip].modules.os.path.exists('./plugin/web_authen/'):
                    client[ip].modules.os.mkdir('./plugin/web_authen/')
                rpyc.classic.upload(client[ip], './__init__.py', './plugin/web_authen/__init__.py')
                rpyc.classic.upload(client[ip], './rFunction.py', './plugin/web_authen/rFunction.py')
                
            except:
                raise Exception("Upload the files failed!")
            
            client[ip].modules["plugin.web_authen.rFunction"]
            client[ip].modules.imp.reload(client[ip].modules["plugin.web_authen.rFunction"])
            rfunc[ip] = rpyc.async(client[ip].modules["plugin.web_authen.rFunction"].mail_auth) 
            
            #logging.info("Build %s remote control succeed!"%ip)
        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(ip,e))
    
    ipl = sorted(rfunc.keys())
    try:
        intvl = float(interval)
    except:
        intvl = 0
        
    # start the remote task, return a dictionary of remote function running object
    if user_flag == 'y':
        username,password = all_user[0]
        for ipf in ipl: 
            rresult[ipf] = rfunc[ipf](username,password)
            logging.info("Build %s remote control succeed!"%ipf)
            time.sleep(intvl)
    else:
        for i in range(len(ipl)):
            ipf = ipl[i]
            username,password = all_user[i]
            rresult[ipf] = rfunc[ipf](username,password)
            logging.info("Build %s remote control succeed!"%ipf)
            time.sleep(intvl)
        
    while rresult:
        for ipr in rresult.keys():
            if rresult[ipr].ready:
                logging.info('Web Authentication %s result: %s'%(ipr,rresult[ipr].value))
                rresult.pop(ipr)
        time.sleep(1)
        
    for ipc in client.keys():
        client[ipc].close()
        
def main():
    
    operations = '''Operations:
c    check connection
r    run one test
q    quit
?    for help
'''
    log_out()
    while True:
        operation = raw_input('>>> ')
        try:
            if operation == 'c': 
                check_connection()
                    
            elif operation == 'r':
                remote_mail_authen()
                
            elif operation == 'q':
                break
                
            elif operation == '?':
                print(operations) 
                
            else:
                print('Please input current operation! "?" for help!')
        except:
            logging.error(traceback.format_exc())

if __name__ == '__main__':
    main()
#     print remote_mail_authen("liht@192.168.0.3","volans123")
    
