# -*- coding:utf-8 -*-

import os
import sys
import rpyc
import time
import logging
import traceback
import gc
import random
import threading
import colorama
from src import colorhandler
from src import configure
from src import ping
    
def check_connection(iplist):

    try:
        ping.ping_ip_list_and_print(iplist)
    except Exception,e:
            logging.error("Check connection failed! Error message: %s"%e)
    
class CheckRemoteControl(threading.Thread):
    '''a multithreading class to check remote control'''
    
    def __init__(self,ip):
        threading.Thread.__init__(self)  
        self.ip = ip 
    
    def run(self):
        try:
            rpyc.classic.connect(self.ip)
            logging.info("Build %s remote control succeed!"%self.ip)

        except Exception,e:
            logging.error("Build %s remote control failed! Error msg: %s"%(self.ip,e))

def check_remote_control(iplist):
    
    client = {}
    iplist = sorted(iplist)
    for ip in iplist:
        try:
            rpyc.classic.connect(ip)
            logging.info("Build %s remote control succeed!"%ip)

        except Exception,e:
            logging.error(u"Build %s remote control failed! Error msg: %s"%(ip,e))  
    gc.collect()
    
class UploadSrc(threading.Thread):
    '''a multithreading class to upload src package '''
    
    def __init__(self,ip):
        threading.Thread.__init__(self)  
        self.ip = ip 

    def run(self):
        try:
            client = rpyc.classic.connect(self.ip)
            rpyc.classic.upload_dir(client, 'src', 'src')
            logging.info("%s finish upload src!"%self.ip)

        except Exception,e:
            logging.error("%s upload src failed! Error message: %s"%(self.ip,e))
    
def upload_src(iplist):
    logging.info("upload the src package to remote pc, wait...")
    client = {}
    iplist = sorted(iplist)
    for ip in iplist:
        client[ip] = UploadSrc(ip)
        
    for ip in iplist:
        client[ip].start()
    
    for ip in iplist:
        client[ip].join()
        
    gc.collect()
    
class UploadBmp(threading.Thread):
    '''a multithreading class to upload bmp package '''
    
    def __init__(self,ip):
        threading.Thread.__init__(self)  
        self.ip = ip 

    def run(self):
        try:
            client = rpyc.classic.connect(self.ip)
            rpyc.classic.upload_dir(client, 'bmp', 'bmp')
            logging.info("%s finish upload bmp!"%self.ip)

        except Exception,e:
            logging.error("%s upload bmp failed! Error message: %s"%(self.ip,e))
        
def upload_bmp(iplist):
    
    logging.info("upload the bmp package to remote pc, wait...")
    client = {}
    iplist = sorted(iplist)
    for ip in iplist:
        client[ip] = UploadBmp(ip)
        
    for ip in iplist:
        client[ip].start()
    
    for ip in iplist:
        client[ip].join()
        
    gc.collect()
        
def upload_all(iplist):
    upload_src(iplist)
    upload_bmp(iplist)
        
class Hotel():
    u'''
    1、Hotel 每层floor可以住多个客户，不够可以新建一层
    2、Hotel 第0层用于表示客户外出，并不代表客户结账离开
    '''
    
    def __init__(self):
        self._hotel = {0:[]} # {layer1:[g1,g2], layer2:[g3,g4]}
    
    def max_layer(self):
        return len(self._hotel.keys())-1
        
    def floor(self,layer):
        return self._hotel[layer]
    
    def new_a_floor(self,guests):
        layer = self.max_layer() + 1
        self._hotel[layer] = guests
    
    def remove_a_guest(self,layer,guest):
        guests = self._hotel[layer]
        if guest in guests:
            guests.remove(guest)
            self._hotel[layer] = guests
    
    def add_a_guest(self,layer,guest):
        guests = self._hotel[layer]
        guests.append(guest)
        self._hotel[layer] = guests
    
    def find_guest(self,guest):
        for layer in xrange(1,self.max_layer()+1):
            if guest in self._hotel[layer]:
                return layer
        
    def move_guest_to_higher_floor(self,guest):
        outlayer = self.find_guest(guest)
        inlayer = outlayer + 1
        self.remove_a_guest(outlayer,guest)
        if inlayer > self.max_layer():
            self.new_a_floor([])
        self.add_a_guest(inlayer,guest)
        
    def move_guest_to_first_floor(self,guest):
        outlayer = self.find_guest(guest)
        self.remove_a_guest(outlayer,guest)
        self.add_a_guest(1,guest)
        
    def go_out(self,guest):
        guests = self._hotel[0]
        guests.append(guest)
        
    def come_back(self,guest):
        self.remove_a_guest(0,guest)
        
    def outlist(self):
        return self._hotel[0]
    
# ************ for test ********************************** 
# 用多线程模拟远程lol执行对象，仅用于测试qq号爬楼机制，可删除
class _TestLol(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.ready = False
        self.value = None
        self.ip = ip
        pass
        
    def run(self):
        u'''
        1、lol远程对象执行时间随机，用time.sleep()
        2、lol远程对象执行结果随机为None或者其他，即self.value属性
        3、lol远程对象是否执行完成，即self.ready属性
                详情可参见rpyc模块中的异步调用，async()方法
        '''
        t = random.randint(5,10)
        time.sleep(t)
        if random.randint(0,1) == 0:
            self.value = 'F'
        else:
            self.value = None
        self.ready = True
# ************ for test ****************************** 

class RemoteTask():
    
    def __init__(self,config_path):
        try:
            config = configure.ConfigureCtrl(config_path)
            self.runtime,self.browse = config.get_global_conf()
            self.web_browsing_conf = config.get_web_browsing_conf()
            self.web_video_conf = config.get_web_video_conf()
            self.lol_conf = config.get_lol_conf()
            self.pptv_conf = config.get_pptv_conf()
            self.cf_conf = config.get_cf_conf()
             
            self.all_urllist = config.get_all_urllist()
            self.qq_dic = config.get_qq_dic()
            
            self._close_flag = False
             
        except Exception,e:
            logging.error("Get configure failed! Error msg: %s"%e)
            raise e
        
    def remote_check_lol_state(self):
        '''For checking all PC's lol running state, return the list of running PC ip
        '''
        client = {}
        rfunc_lol_state = {}
        for ip_l in self.lol_conf.keys():
            try:
                client[ip_l] = rpyc.classic.connect(ip_l)
                client[ip_l].modules["src.lol"]
                client[ip_l].modules.imp.reload(client[ip_l].modules["src.lol"])
                rfunc_lol_state[ip_l] = client[ip_l].modules["src.lol"].state

                #logging.info("Build %s remote control succeed!"%ip_l)
            except Exception,e:
                logging.error("Build %s remote control failed! Error msg: %s"%(ip_l,e))
                
        over_pc = []
        running_pc = []
        
        for ip in rfunc_lol_state.keys():
            lol_run = rfunc_lol_state[ip]()
            if lol_run:
                running_pc.append(ip)
            else:
                over_pc.append(ip)
          
        if running_pc:
            logging.info("%s LOL is finished, %s LOL is still running."%(len(over_pc),len(running_pc)))
            return running_pc
        else:
            return None

    def remote_get_lol_ping(self,start_time=None):
        '''
        Get value of ping in lol.
        1.start_time is a tuple, use the form (year,month,day,hour,minute,second)
        '''
        
        # create remote connection
        client = {}
        rfunc_get_ping = {}
        for ip_l in self.lol_conf.keys():
            try:
                client[ip_l] = rpyc.classic.connect(ip_l)
                client[ip_l].modules["src.lol"]
                client[ip_l].modules.imp.reload(client[ip_l].modules["src.lol"])
                rfunc_get_ping[ip_l] = client[ip_l].modules["src.lol"].get_all_ping

                #logging.info("Build %s remote control succeed!"%ip_l)
            except Exception,e:
                logging.error("Build %s remote control failed! Error msg: %s"%(ip_l,e))
        
        # make dir
        cur_time = time.strftime('%Y_%m_%d__%H_%M_%S',time.localtime())
        save_dir = './result/lolPing/'+cur_time
        now_dir = '.'
        for dirr in save_dir.split('/')[1:]:
            now_dir = now_dir + '/' +  dirr
            is_exists = os.path.exists(now_dir)
            if not is_exists:
                os.mkdir(now_dir)
        
        # get ping and record
        if start_time:
            for ip in rfunc_get_ping.keys():
                save_path = save_dir+'/'+ '_'.join(ip.split('.'))+'.txt'
                lol_pings = rfunc_get_ping[ip]()
                result_file = open(save_path,'a+')
                for t,ping in lol_pings:
                    if t > start_time:
                        record_msg = '%d-%02d-%02d %02d:%02d:%02d'%t + '  %s'%ping
                        result_file.write(record_msg+'\n')
                        if ping >150 :
                            logging.warn('%s ping >150 : %s'%(ip,record_msg))
                result_file.close()
                
        else:
            for ip in client.keys():
                save_path = save_dir+'/'+ '_'.join(ip.split('.'))+'.txt'
                lol_pings = rfunc_get_ping[ip]()
                result_file = open(save_path,'a+')
                for t,ping in lol_pings:
                    record_msg = '%d-%02d-%02d %02d:%02d:%02d'%t + '  %s'%ping
                    result_file.write(record_msg+'\n')
                    if ping >150 :
                        logging.warn('%s ping >150 : %s'%(ip,record_msg))
                result_file.close()

    def remote_play_lol(self):
        u'''
        # 创建一个Hotel对象，并把qq放入其中，采用以下机制：
        # 1、初始层是1，一旦qq被使用，让qq进入外出名单。一旦结束使用，qq回到hotel
        # 2、如果lol运行异常（远程lol返回值不为空），将给出error，并将此qq放入更高的层次
        #    如果lol运行正常，将重置layer为1，qq回到第一层
        # 3、最重要的：我们将先从第一层开始获取qq，如果没有获取到，给出warning，并去第二层获取，以此类推。
        #    也就是说，如果一个qq出错次数越多，表明其被封号的可能性越大；同理我们将越难获得此qq。
        # 
        # 其中的问题：
        # 1、循环查找qq会导致越排序靠前qq越容易上到最高层
        # 2、注意会不会发生死循环！！！！
        '''
        
        client    = {}
        rfunc_lol = {}
        start_time = time.time()
        qqhotel = Hotel()
        
        # a time flag for recording the lol ping 
        start_local_time = tuple(time.localtime())[:6]
        
        # Initialize dictionary lol_qqs : {layer:[qq1,qq2]}
        # layer: 0 --- unusable
        qqhotel.new_a_floor(self.qq_dic.keys())
        
        # build remote connection for play lol, return a dictionary of remote function object
        logging.info("Build remote connection for play lol...")
        for ip_l in self.lol_conf.keys():
            try:
                client[ip_l] = rpyc.classic.connect(ip_l)
                rfunc_lol[ip_l] = rpyc.async(client[ip_l].modules["src.lol"].play_lol)
                client[ip_l].modules.imp.reload(client[ip_l].modules["src.lol"])
                logging.info("Build %s remote control succeed!"%ip_l)
            except Exception:
                logging.error("Build %s remote control failed!"%ip_l)
                #self._close_flag = True
     
        # start the remote task, return a dictionary of remote function running object
        # for play lol
        rresult_lol = {}
        
        # for ip to qq
        ipvqq = {}

        # ************ for test ****************************************
        # if you are test the qqhotel, replace the row of "**replace1**"
        # for ip_l in self.lol_conf: 
        # ************ for test ****************************************
        
        for ip_l in rfunc_lol.keys(): #**replace1**
            try:
                username = None
                password = None

                for qq in qqhotel.floor(1):
                    if qq not in qqhotel.outlist():
                        username = qq
                        password = self.qq_dic[qq]
                        qqhotel.go_out(qq)
                        ipvqq[ip_l] = qq
                        logging.info( '%s got QQ number %s'%(ip_l,qq))
                        break
                if not username:
                    logging.warning('%s could not get QQ number'%ip_l)
                
                else:
                    logging.info('start %s play lol...'%ip_l)
                    
                    # ************ for test ****************************************
                    # if you are test the qqhotel, replace the row of "**replace2**"
                    # rresult_lol[ip_l] = _TestLol(ip_l)
                    # ************ for test ****************************************
                    
                    #**replace2**
                    serverid = self.lol_conf[ip_l]
                    rresult_lol[ip_l] = rfunc_lol[ip_l](username=username,password=password,serverid=serverid) 
                    #**replace2**
            
            except Exception,e:
                logging.error("Start %s play lol failed! Error msg: %s"%(ip_l,e))
                self._close_flag = True
     
        # runtime is used to stop the function, set it to second
        runtime_sec = self.runtime * 60
        new_game_time_sec = (self.runtime - 20) * 60
        logging.info("We will run remote_play_lol in %s minutes."%self.runtime)
        
        # ************ for test ******************************
        # if you are test the qqhotel, add these row
        # for ip in rresult_lol.keys():     
        #     rresult_lol[ip].start()
        # ************ for test ******************************
        
        # Check remote function running object. If stopped, run again. 
        while True:
            
            t = time.time() - start_time
            if t > new_game_time_sec or self._close_flag:
                logging.info("Stop new a remote_play_lol.")
                break
            
            time.sleep(5)
            # for browsing web
            for ip_l in rresult_lol.keys():
                try:
                    # init username and password
                    username = None
                    password = None
                    
                    if rresult_lol[ip_l].ready:
                        # if a remote lol is stopped and ready, the qq of the ip come back to qqhotel 
                        qqhotel.come_back(ipvqq[ip_l])
                        
                        if rresult_lol[ip_l].value:
                            # if we got a exception result, move the qq to a higher floor
                            logging.warning(u'Lol: %s(qq:%s) got some error and '\
                                            u'we will run it again:\n %s'%(ip_l,ipvqq[ip_l],rresult_lol[ip_l].value))
                            qqhotel.move_guest_to_higher_floor(ipvqq[ip_l])
                        else:
                            # if we got nothing, move the qq to the first floor
                            logging.info('Lol: %s(qq:%s) run ok and we will run it again'%(ip_l,ipvqq[ip_l]))
                            qqhotel.move_guest_to_first_floor(ipvqq[ip_l])
                        
                        # the remote lol need a new qq
                        for layer in xrange(1,qqhotel.max_layer()+1):
                            for qq in qqhotel.floor(layer):
                                if qq not in qqhotel.outlist():
                                    username = qq
                                    password = self.qq_dic[qq]
                                    qqhotel.go_out(qq)
                                    ipvqq[ip_l] = qq
                                    break
                                
                            if not username:
                                pass
                                #logging.warning('%s could not get QQ number in the floor %s'%(ip_l,layer))

                            else:
                                logging.info('%s got qq(%s) in the floor %s'%(ip_l,username,layer))
                                break
                            
                        # ************ for test **************************************** 
                        # if you are test the qqhotel, replace the row of "**replace3**"      
                        # rresult_lol[ip_l] = _TestLol(ip_l)
                        # rresult_lol[ip_l].start()
                        # ************ for test **************************************** 
                        
                        #**replace3**
                        serverid = self.lol_conf[ip_l]
                        rresult_lol[ip_l] = rfunc_lol[ip_l](username=username,password=password,serverid=serverid) 
                        #**replace3**
                          
                except Exception,e:
                    logging.error("Check and restart %s remote lol failed! Error msg: %s"%(ip_l,e))
        while True:
            t = time.time() - start_time
            if t > runtime_sec or self._close_flag:
                logging.info("Stop run remote_play_lol.")
                break
            time.sleep(5)
        
        # clean the task
        logging.info('clean the remote lol connection')
        for ip in client.keys():
            client[ip].close()
            
        while 1:
            time.sleep(30)
            running_pc = self.remote_check_lol_state()
            if running_pc:
                logging.info('These LOL is still running: %s'%running_pc)
            else:
                self.remote_get_lol_ping(start_time=start_local_time)
                break
            
#         over_pc = []
#         running_pc = []
#         for ip_l in rresult_lol.keys():
#             if rresult_lol[ip_l].ready:
#                 over_pc.append(ip_l)
#             else:
#                 running_pc.append(ip_l)
#                 
#         logging.warn("%s LOL is finished, %s LOL is still running."%(len(over_pc),len(running_pc)))
#         logging.warn("These LOL is still running:")
#         for pcip in running_pc:
#             logging.warn("%s"%pcip)
            
    def remote_play_cf(self):
        u'''
        # 创建一个Hotel对象，并把qq放入其中，采用以下机制：
        # 1、初始层是1，一旦qq被使用，让qq进入外出名单。一旦结束使用，qq回到hotel
        # 2、如果cf运行异常（远程cf返回值不为空），将给出error，并将此qq放入更高的层次
        #    如果cf运行正常，将重置layer为1，qq回到第一层
        # 3、最重要的：我们将先从第一层开始获取qq，如果没有获取到，给出warning，并去第二层获取，以此类推。
        #    也就是说，如果一个qq出错次数越多，表明其被封号的可能性越大；同理我们将越难获得此qq。
  
        '''
        
        client   = {}
        rfunc_cf = {}
        start_time = time.time()
        qqhotel = Hotel()
        
        # Initialize dictionary cf_qqs : {layer:[qq1,qq2]}
        # layer: 0 --- unusable
        qqhotel.new_a_floor(self.qq_dic.keys())
        
        # build remote connection for play cf, return a dictionary of remote function object
        logging.info("Build remote connection for play cf...")
        for ip_c in self.cf_conf.keys():
            try:
                client[ip_c] = rpyc.classic.connect(ip_c)
                rfunc_cf[ip_c] = rpyc.async(client[ip_c].modules["src.cf"].play_cf)
                client[ip_c].modules.imp.reload(client[ip_c].modules["src.cf"])
                logging.info("Build %s remote control succeed!"%ip_c)
            except Exception,e:
                logging.error("Build %s remote control failed! Error msg: %s"%(ip_c,e))
                self._close_flag = True
     
        # start the remote task, return a dictionary of remote function running object
        # for play cf
        rresult_cf = {}
        
        # for ip to qq
        ipvqq = {}

        # ************ for test ****************************************
        # if you are test the qqhotel, replace the row of "**replace1**"
        # for ip_c in self.cf_conf: 
        # ************ for test ****************************************
        
        for ip_c in rfunc_cf.keys(): #**replace1**
            try:
                username = None
                password = None

                for qq in qqhotel.floor(1):
                    if qq not in qqhotel.outlist():
                        username = qq
                        password = self.qq_dic[qq]
                        qqhotel.go_out(qq)
                        ipvqq[ip_c] = qq
                        logging.info( '%s got QQ number %s'%(ip_c,qq))
                        break
                if not username:
                    logging.warning('%s could not get QQ number'%ip_c)
                
                else:
                    logging.info('start %s play cf...'%ip_c)
                    
                    # ************ for test ****************************************
                    # if you are test the qqhotel, replace the row of "**replace2**"
                    # rresult_cf[ip_c] = _Testcf(ip_c)
                    # ************ for test ****************************************
                    
                    #**replace2**
                    serverid = self.cf_conf[ip_c]
                    rresult_cf[ip_c] = rfunc_cf[ip_c](username=username,password=password,serverid=serverid) 
                    #**replace2**
            
            except Exception,e:
                logging.error("Start %s play cf failed! Error msg: %s"%(ip_c,e))
                self._close_flag = True
     
        # runtime is used to stop the function, set it to second
        runtime_sec = self.runtime * 60
        logging.info("We will run remote_play_cf in %s minutes."%self.runtime)
        
        # ************ for test ******************************
        # if you are test the qqhotel, add these row
        # for ip in rresult_cf.keys():     
        #     rresult_cf[ip].start()
        # ************ for test ******************************
        
        # Check remote function running object. If stopped, run again. 
        while True:
              
            t = time.time() - start_time
            if t > runtime_sec or self._close_flag:
                logging.info("Stop run remote_play_cf.")
                break
            
            time.sleep(5)
            
            # for browsing web
            for ip_c in rresult_cf.keys():
                try:
                    # init username and password
                    username = None
                    password = None
                    
                    if rresult_cf[ip_c].ready:
                        # if a remote cf is stopped and ready, the qq of the ip come back to qqhotel 
                        qqhotel.come_back(ipvqq[ip_c])
                        
                        if rresult_cf[ip_c].value:
                            # if we got a exception result, move the qq to a higher floor
                            logging.warning(u'cf: %s(qq:%s) got some error and '\
                                            u'we will run it again:\n %s'%(ip_c,ipvqq[ip_c],rresult_cf[ip_c].value))
                            qqhotel.move_guest_to_higher_floor(ipvqq[ip_c])
                        else:
                            # if we got nothing, move the qq to the first floor
                            logging.info('cf: %s(qq:%s) run ok and we will run it again'%(ip_c,ipvqq[ip_c]))
                            qqhotel.move_guest_to_first_floor(ipvqq[ip_c])
                        
                        # the remote cf need a new qq
                        for layer in xrange(1,qqhotel.max_layer()+1):
                            for qq in qqhotel.floor(layer):
                                if qq not in qqhotel.outlist():
                                    username = qq
                                    password = self.qq_dic[qq]
                                    qqhotel.go_out(qq)
                                    ipvqq[ip_c] = qq
                                    break
                                
                            if not username:
                                pass

                            else:
                                logging.info('%s got qq(%s) in the floor %s'%(ip_c,username,layer))
                                break
                            
                        # ************ for test **************************************** 
                        # if you are test the qqhotel, replace the row of "**replace3**"      
                        # rresult_cf[ip_c] = _Testcf(ip_c)
                        # rresult_cf[ip_c].start()
                        # ************ for test **************************************** 
                        
                        #**replace3**
                        serverid = self.cf_conf[ip_c]
                        rresult_cf[ip_c] = rfunc_cf[ip_c](username=username,password=password,serverid=serverid) 
                        #**replace3**
                          
                except Exception,e:
                    logging.error("Check and restart %s remote cf failed! Error msg: %s"%(ip_c,e))
        
        # clean the task
        logging.info('clean the remote cf')
        for ip in client.keys():
#             client[ip].close()
            conn = rpyc.classic.connect(ip)
            rclean = rpyc.async(conn.modules["src.cf"].clean)
            rclean()
            time.sleep(0.01)
            conn.close()

    def remote_web_browsing(self):
        '''
        '''
        
        # build remote connection for browsing web, return a dictionary of remote function object
        client = {} 
        rfunc_web_b = {} 
        start_time = time.time()
    
        logging.info("Build remote connection for browsing web...")
        for ip_b in self.web_browsing_conf.keys():
            try:
                client[ip_b] = rpyc.classic.connect(ip_b)
                rfunc_web_b[ip_b] = rpyc.async(client[ip_b].modules["src.web_browsing"].web_browsing) 
                client[ip_b].modules.imp.reload(client[ip_b].modules["src.web_browsing"])
                logging.info("Build %s remote control succeed!"%ip_b)
            except Exception,e:
                logging.error("Build %s remote control failed! Error msg: %s"%(ip_b,e))
                self._close_flag = True
        
        # start the remote task, return a dictionary of remote function running object
        # for browsing web
        rresult_web_b = {}
        for ip_b in rfunc_web_b.keys():
            try:
                logging.info('start %s browsing web...'%ip_b)
                urllist_id = self.web_browsing_conf[ip_b]
                if urllist_id in self.all_urllist.keys():
                    url_list = self.all_urllist[urllist_id]
                else:
                    msg = 'can not find the urllist_id in all urllist, please check the configure'
                    raise ValueError,msg
                rresult_web_b[ip_b] = rfunc_web_b[ip_b](url_list=url_list,browse=self.browse)
                
            except Exception,e:
                logging.error("Start %s browsing web failed! Error msg: %s"%(ip_b,e))
                self._close_flag = True
        
        # runtime is used to stop the function, set it to second
        runtime_sec = self.runtime * 60
        logging.info("We will run remote_web_browsing in %s minutes."%self.runtime)
        
        # Check remote function running object. If stopped, run again.
        # for browsing web 
        while True:
            
            t = time.time() - start_time
            if t > runtime_sec or self._close_flag:
                logging.info("Stop run remote_web_browsing.")
                break
            
            time.sleep(5)
            
            for ip_b in rresult_web_b.keys():
                try:
                    urllist_id = self.web_browsing_conf[ip_b]
                    url_list = self.all_urllist[urllist_id]
                    if rresult_web_b[ip_b].ready:
                        if rresult_web_b[ip_b].value:
                            logging.warning(u'Browse web: %s got some error and '\
                                            u'we will run it again:\n %s'%(ip_b,rresult_web_b[ip_b].value))
                        else:
                            logging.info('Browse web: %s run ok and we will run it again'%ip_b)
                        rresult_web_b[ip_b] = rfunc_web_b[ip_b](url_list=url_list,browse=self.browse)
                        
                except Exception,e:
                    logging.error("Check and restart %s remote web_browsing failed! Error msg: %s"%(ip_b,e))
        
        # clean the task
        logging.info('clean the remote web_browsing')
        for ip in client.keys():
            client[ip].close()
            conn = rpyc.classic.connect(ip)
            rclean = rpyc.async(conn.modules["src.web_browsing"].clean)
            rclean()
            time.sleep(0.01)
            conn.close()
            
    def remote_watch_web_video(self):
        '''
        '''
        
        # build remote connection for watching web video, return a dictionary of remote function object
        client = {}
        rfunc_web_v = {}
        start_time = time.time()
        
        logging.info("Build remote connection for watching web video...")
        for ip_v in self.web_video_conf.keys():
            try:
                client[ip_v] = rpyc.classic.connect(ip_v)
                rfunc_web_v[ip_v] = rpyc.async(client[ip_v].modules["src.web_video"].web_video)
                client[ip_v].modules.imp.reload(client[ip_v].modules["src.web_video"])
                logging.info("Build %s remote control succeed!"%ip_v)
            except Exception,e:
                logging.error("Build %s remote control failed! Error msg: %s"%(ip_v,e))
                self._close_flag = True
        
        # start the remote task, return a dictionary of remote function running object
        # for watch web video
        rresult_web_v = {}
        for ip_v in rfunc_web_v.keys():
            
            try:
                logging.info('start %s watching web video...'%ip_v)
                url = self.web_video_conf[ip_v][0]
                watch_time = self.web_video_conf[ip_v][1]
                rresult_web_v[ip_v] = rfunc_web_v[ip_v](url=url,runtime=watch_time,browse=self.browse)
            except Exception,e:
                logging.error("Start %s watching web video failed! Error msg: %s"%(ip_v,e))
                self._close_flag = True
            
        # runtime is used to stop the function, set it to second
        runtime_sec = self.runtime * 60    
        logging.info("We will run remote_watch_web_video in %s minutes."%self.runtime)
        
        # Check remote function running object. If stopped, run again. 
        # for watching web video
        while True:
            
            t = time.time() - start_time
            if t > runtime_sec or self._close_flag:
                logging.info("Stop run remote_watch_web_video.")
                break
            
            time.sleep(5)
            
            for ip_v in rresult_web_v.keys():
                try:
                    url = self.web_video_conf[ip_v][0]
                    watch_time = self.web_video_conf[ip_v][1]
                    if rresult_web_v[ip_v].ready:
                        if rresult_web_v[ip_v].value:
                            logging.warning(u'Web video: %s got some error and '\
                                            u'we will run it again:\n %s'%(ip_v,rresult_web_v[ip_v].value))
                        else:
                            logging.info('Web video: %s run ok and we will run it again'%ip_v)
                        rresult_web_v[ip_v] = rfunc_web_v[ip_v](url=url,runtime=watch_time,browse=self.browse)
                        
                except Exception,e:
                    logging.error("Check and restart %s remote web_video failed! Error msg: %s"%(ip_v,e))
        
        # clean the task
        logging.info('clean the remote web_video')
        for ip in client.keys():
            client[ip].close()
            conn = rpyc.classic.connect(ip)
            rclean = rpyc.async(conn.modules["src.web_video"].clean)
            rclean()
            time.sleep(0.01)
            conn.close()
            
    def remote_pptv(self):
        '''
        '''
        
        # build remote connection for watching pptv, return a dictionary of remote function object
        client = {}
        rfunc_pptv = {}
        start_time = time.time()
        
        logging.info("Build remote connection for pptv...")
        for ip_p in self.pptv_conf.keys():
            try:
                client[ip_p] = rpyc.classic.connect(ip_p)
                rfunc_pptv[ip_p] = rpyc.async(client[ip_p].modules["src.pptv"].pptv)
                client[ip_p].modules.imp.reload(client[ip_p].modules["src.pptv"])
                logging.info("Build %s remote control succeed!"%ip_p)
            except Exception,e:
                logging.error("Build %s remote control failed! Error msg: %s"%(ip_p,e))
                self._close_flag = True
        
        # start the remote task, return a dictionary of remote function running object
        # for watching pptv
        rresult_pptv = {}
        for ip_p in rfunc_pptv.keys():
            
            try:
                logging.info('start %s pptv...'%ip_p)
                url = self.pptv_conf[ip_p]
                rresult_pptv[ip_p] = rfunc_pptv[ip_p](url=url)
            except Exception,e:
                logging.error("Start %s pptv failed! Error msg: %s"%(ip_p,e))
                self._close_flag = True
            
        # runtime is used to stop the function, set it to second
        runtime_sec = self.runtime * 60    
        logging.info("We will run remote_pptv in %s minutes."%self.runtime)
        
        # Check remote function running object. If stopped, run again. 
        # for watching pptv
        while True:
            
            t = time.time() - start_time
            if t > runtime_sec or self._close_flag:
                logging.info("Stop run remote_pptv.")
                break
            
            time.sleep(5)
            
            for ip_p in rresult_pptv.keys():
                try:
                    url = self.pptv_conf[ip_p]
                    if rresult_pptv[ip_p].ready:
                        if rresult_pptv[ip_p].value:
                            logging.warning(u'PPTV: %s got some error and '\
                                            u'we will run it again:\n %s'%(ip_p,rresult_pptv[ip_p].value))
                        else:
                            logging.info('PPTV: %s run ok and we will run it again'%ip_p)
                        rresult_pptv[ip_p] = rfunc_pptv[ip_p](url=url)
                        
                except Exception,e:
                    logging.error("Check and restart %s remote pptv failed! Error msg: %s"%(ip_p,e))
        
        # clean the task
        logging.info('clean the remote pptv')
        for ip in client.keys():
            client[ip].close()
            conn = rpyc.classic.connect(ip)
            rclean = rpyc.async(conn.modules["src.pptv"].clean)
            rclean()
            time.sleep(0.01)
            conn.close()
       
    def run_all(self):
        
        try:
            
            logging.info("We will run all the task in %s minutes."%self.runtime)
            web_brosewing_thread = threading.Thread(target=self.remote_web_browsing)
            web_video_thread  = threading.Thread(target=self.remote_watch_web_video)
            lol_thread = threading.Thread(target=self.remote_play_lol)
            pptv_thread = threading.Thread(target=self.remote_pptv)
            cf_thread = threading.Thread(target=self.remote_play_cf)
            
            web_brosewing_thread.start()
            web_video_thread.start()
            lol_thread.start()
            pptv_thread.start()
            cf_thread.start()
            
            web_brosewing_thread.join()
            web_video_thread.join()
            lol_thread.join()
            pptv_thread.join()
            cf_thread.join()
            
        except Exception,e:
            self._close_flag = True
            logging.error("Build multithreading failed! Error message: %s"%e)
            return
    
def log_format():
    
    cur_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())

    logging.getLogger().setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    
    co = colorhandler.ColorHandler(sys.stderr)
    co.setFormatter(formatter)
    
    fh = logging.FileHandler('./log/consolePC/%s.log'%cur_time)
    fh.setFormatter(formatter)
    
    logging.getLogger().addHandler(co)
    logging.getLogger().addHandler(fh)
    
def print_cyan(string):
    colorama.init()
    print "\033[40;36;1m%s\033[0m" %string

def raw_input_cyan(string):
    colorama.init()
    value = raw_input('''\033[40;36;1m%s'''%string)
    return value
    
def main():
    
    config_path = './conf/config.db'
    operations = '''Operations:
check        check the remote control
run          start running
lol          scan lol run state
plol         get the lol ping value
quit         quit program
'''
    log_format()
    config = configure.ConfigureCtrl(config_path)
    
    print_cyan(operations)
    while True:
            
        operation = raw_input_cyan('>>> ').lower()
        if operation == 'check': 
            iplist = config.get_all_ip()
            check_remote_control(iplist)
        
        elif operation == 'run':
            iplist = config.get_all_ip()
            upload_all(iplist)
            remotetask = RemoteTask(config_path)
            remotetask.run_all()
            
        elif operation == 'quit':
            break

        elif operation == 'upload':
            iplist = config.get_all_ip()
            upload_all(iplist)
        
        elif operation == 'lol':
            remotetask = RemoteTask(config_path)
            remotetask.remote_check_lol_state()
            
        elif operation == 'plol':
            remotetask = RemoteTask(config_path)
            remotetask.remote_get_lol_ping()
            
        else:
            print_cyan('Please input current operation!')
            print_cyan(operations)
        
if __name__ == '__main__':
#     config_path = './conf/config.db'
#     remotetask = RemoteTask(config_path)
#     remotetask.remote_play_lol()
    try:
        main()
    except Exception:
        traceback.print_exc()
        raw_input_cyan('Some error was happened, input anything to quit.')
#     h = Hotel()
#     print h.max_layer()
#     h.new_a_floor(guests=[1,2,3,4])
#     h.new_a_floor(guests=[6,7,8,9])
#     print h._hotel
#     print h.find_guest(6)
#     h.move_guest_to_higher_floor(6)
#     h.move_guest_to_higher_floor(2)
#     h.move_guest_to_first_floor(8)
#     h.move_guest_to_first_floor(4)
#     h.go_out(9)
#     h.go_out(2)
#     print h._hotel
#     h.come_back(2)
#     print h.outlist()
#     print h._hotel
#     for i in h.floor(1):
#         print i

    
