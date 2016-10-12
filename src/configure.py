# -*- coding:utf-8 -*-

import sqlite3
import logging

class ConfigureCtrl(object):
    
    def __init__(self,config_path):
        self.config_path = config_path
     
    def get_global_conf(self):
        '''
        # return (gl_runtime,gl_browse)
        # gl_runtime is the program run time, default 60 minutes
        # gl_browse is the browse which you choosed, default "chrome"
        '''
        runtime = 60
        browse = 'chrome'
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            runtime_obj = cu.execute("select value from global where item = 'runtime'")
            for item_rt in runtime_obj:
                try:
                    runtime = int(item_rt[0])
                except Exception:
                    err_msg = 'global runtime is not a integer'
                    raise Exception,err_msg
                
            browse_obj = cu.execute("select value from global where item = 'browse'")
            for item_br in browse_obj:
                browse = item_br[0]
                
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get global configure failed, we will set it to default! Error: %s' %e)

        finally:
            return runtime,browse
        
    def get_web_browsing_conf(self):
        '''
        # return {'192.168.1.10':'urllist_1'}
        # 192.168.1.10 host browsing baidu and qq
        '''
        configure = {}
        
        try:
               
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            web_browsing_obj = cu.execute("select * from web_browsing")
            
            for item in web_browsing_obj:
                if item[0]:
                    if item[0] in configure.keys():
                        logging.warning('We got an same ip(%s) when getting veb browsing configure.'%item[0])
                    ip = item[0]
                    if isinstance(item[1],int):
                        urllist = 'urllist_%s'%item[1]
                    else:
                        urllist = None
                    configure[ip] = urllist
            
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get web browsing configure failed! Error: %s' %e)
        
        finally:
            return configure
        
        
    def get_web_video_conf(self):
        '''
        # return {'192.168.1.10':['http://v.youku.com/v_show/id_XNDMzNDAzNjQw.html', 60]}
        # 192.168.1.10 host watch http://... video 60 minutes
        '''
        
        configure = {}
        
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            web_video_obj = cu.execute("select * from web_video")
            
            for item in web_video_obj:
                if item[0]:
                    ip = item[0]
                    if item[0] in configure.keys():
                        logging.warning('We got an same ip(%s) when getting veb video configure.'%item[0])
                    
                    if item[1]:
                        url = item[1]
                    else:
                        url = None
                        
                    if isinstance(item[2],int):
                        watchtime = item[2]
                    else:
                        watchtime = 60
                        logging.error('Web video watchtime is not a integer. We will set it to default 60 minutes')
                    
                    configure[ip] = [url,watchtime]
                    
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get web video configure failed! Error: %s' %e)
        
        finally:
            return configure
        
    def get_all_urllist(self):
        '''
        # return {'urllist_2': [], 'urllist_1': ['http://www.baidu.com/']}
        '''
        all_urllist = {}
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            urllist_obj = cu.execute("select * from urllist")
            
            for item in urllist_obj:
                if item[0]:
                    id = item[0]
                    if item[1]:
                        urllist = item[1].split(';')
                    else:
                        urllist = None
                    all_urllist[id] = urllist
                    
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get all urllist failed! Error: %s' %e)
        
        finally:
            return all_urllist
            
    def get_qq_dic(self):
        '''
        # return {'123456789':'volans','222222222':'volans'}
        # QQ:123456789, PASSWORD:volans
        '''
        qq_list = {}
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            qq_obj = cu.execute("select * from qqlist")
            
            for item in qq_obj:
                if item[0]:
                    qq = item[0]
                    if item[1]:
                        pwd = item[1]
                        qq_list[qq] = pwd
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get QQ list failed! Error: %s' %e)
        
        finally:
            return qq_list
        
    def get_lol_conf(self):
        '''
        # return {'192.168.1.15':'1','192.168.1.16':'2'}
        '''
        lol_conf = {}
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            lol_obj = cu.execute("select * from lol")
            
            for item in lol_obj:
                if item[0]:
                    if item[0] in lol_conf.keys():
                        logging.warning('We got an same ip(%s) when getting lol configure.'%item[0])
                    ip = item[0]
                    serverid = item[1]
                    lol_conf[ip] = int(serverid)    
                        
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get lol configure failed! Error: %s' %e)
        
        finally:
            return lol_conf
    
    def get_cf_conf(self):
        '''
        # return {'192.168.1.15':'1','192.168.1.16':'2'}
        '''
        cf_conf = {}
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            cf_obj = cu.execute("select * from cf")
            
            for item in cf_obj:
                if item[0]:
                    if item[0] in cf_conf.keys():
                        logging.warning('We got an same ip(%s) when getting cf configure.'%item[0])
                    ip = item[0]
                    serverid = item[1]
                    cf_conf[ip] = int(serverid)    
                        
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get cf configure failed! Error: %s' %e)
        
        finally:
            return cf_conf
    
    def get_pptv_conf(self):
        '''
        # return {'192.168.1.15':'pptv://0a2lmamao6mlj9iioaWdj9mioZbQpqeco6aknq2Z'}
        '''
        pptv_conf = {}
        try:
            
            config_db = sqlite3.connect(self.config_path)
            cu = config_db.cursor()
            
            pptv_obj = cu.execute("select * from pptv")
            
            for item in pptv_obj:
                if item[0]:
                    if item[0] in pptv_conf.keys():
                        logging.warning('We got an same ip(%s) when getting pptv configure.'%item[0])
            
                    ip = item[0]
                    url = item[1]
                        
                    pptv_conf[ip] = url    
                        
            cu.close()
            config_db.close()
        
        except Exception,e:
            logging.error('Get lol configure failed! Error: %s' %e)
        
        finally:
            return pptv_conf
    
    def get_all_ip(self):
        
        iplist = []
        try:
            ip1 = self.get_web_browsing_conf().keys()
            ip2 = self.get_web_video_conf().keys()
            ip3 = self.get_lol_conf().keys()
            ip4 = self.get_pptv_conf().keys()
            ip5 = self.get_cf_conf().keys()
            for ip in ip1:
                iplist.append(ip)
            for ip in ip2:
                if ip in iplist:
                    logging.warning('We got an same ip(%s) in web_video configure when getting all ip.'%ip)
                else:
                    iplist.append(ip)
            for ip in ip3:
                if ip in iplist:
                    logging.warning('We got an same ip(%s) in lol configure when getting all ip.'%ip)
                else:
                    iplist.append(ip)
            for ip in ip4:
                if ip in iplist:
                    logging.warning('We got an same ip(%s) in pptv configure when getting all ip.'%ip)
                else:
                    iplist.append(ip)
            for ip in ip5:
                if ip in iplist:
                    logging.warning('We got an same ip(%s) in cf configure when getting all ip.'%ip)
                else:
                    iplist.append(ip)
                
        except Exception,e:
            logging.error('Get all ip failed! Error: %s' %e)
        
        finally:
            return iplist
        
if __name__ == '__main__':
    conf = ConfigureCtrl('../conf/config.db')
    print conf.get_global_conf()
    print conf.get_web_browsing_conf()
    print conf.get_web_video_conf()
    print conf.get_all_urllist()
    print conf.get_qq_dic()
    print conf.get_lol_conf(),'lol'
    print conf.get_pptv_conf()
    print conf.get_cf_conf(),'cf'
    print conf.get_all_ip()
    
