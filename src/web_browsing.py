# -*- coding:utf-8 -*-

import os
import time
import logging
from selenium import webdriver

    
def web_browsing(url_list=None,timeout=20,browse='ie'):
    '''
    1. url_list is a list, define a url list to browse
    2. timeout is a integer, define a timeout(seconds) when loading a web 
    3. browse is a string, define the browse which you choose
    '''
    logging.info('start browse web...')
    if not url_list:
        url_list = ["http://www.hao123.com/",
                    "http://www.baidu.com/",
                    "http://www.qq.com/",
                    "http://www.163.com/",
                    "http://www.renren.com/"]
    try:
        browse = browse.lower()
        if browse == 'chrome':
            logging.info('open chrome')
            driver = webdriver.Chrome()
        elif browse == 'ie':
            logging.info('open ie')
            driver = webdriver.Ie()
        elif browse == 'firefox':
            logging.info('open firefox')
            driver = webdriver.Firefox()
        else:
            raise ValueError,'Your browse is not support!'
        
        driver.set_page_load_timeout(timeout)
        for url in url_list:
            try:
                logging.info('open the url: %s'%url)
                driver.get(url)
                time.sleep(10)
            except Exception:
                pass
    
        logging.info('close the browse')
        driver.quit()
        
    except Exception,e:
        err_msg = 'browse web error: %s'%e
        logging.error(err_msg)
        return err_msg
    
    else:
        return None

def clean():
    logging.info('clean the web_browsing')
    os.system('taskkill /f /im iexplore.exe')
    os.system('taskkill /f /im firefox.exe')
    os.system('taskkill /f /im chrome.exe')
    os.system('taskkill /f /im chromedriver.exe')
    os.system('taskkill /f /im IEDriverServer.exe')

if __name__ == "__main__":
    url_list = 'urllist_1'
    print web_browsing(browse = 'chrome')
#     t = time.time()
#     clean()
#     print time.time() - t
