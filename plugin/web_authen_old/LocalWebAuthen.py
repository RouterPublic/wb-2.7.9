# -*- coding:utf-8 -*-

import os
import time
import logging
from selenium import webdriver

    
def local_web_authen(timeout=60,browse='ie'):
    '''
    '''

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
        try:
            qq = 'www.qq.com'
            logging.info('open the url: %s'%qq)
            driver.get(qq)
        except Exception:
            pass
        time.sleep(1)

        for i in range(30) :
            try:
                driver.find_element_by_name("ONLINE")
            except Exception,e:
                print e
            else:
                if driver.find_element_by_name("ONLINE").get_attribute("value") == u"点击上网":
                    driver.find_element_by_name("ONLINE").click()
            time.sleep(1)
            
        try:
            bd = 'www.baidu.com'
            logging.info('open the url: %s'%bd)
            driver.get(bd)
        except Exception:
            pass
        
        for i in range(60):
            if driver.title == u"百度一下，你就知道" :
                logging.info('close the browse')
                driver.quit() 
                return 'Web authentication OK!'    
            else:
                time.sleep(1)
        
        logging.info('close the browse')
        driver.quit() 
        return 'Can not open baidu!'
        
    except Exception,e:
        err_msg = 'browse web error: %s'%e
        logging.error(err_msg)
        return err_msg

def clean():
    logging.info('clean the web_browsing')
    os.system('taskkill /f /im iexplore.exe')
    os.system('taskkill /f /im firefox.exe')
    os.system('taskkill /f /im chrome.exe')
    os.system('taskkill /f /im chromedriver.exe')
    os.system('taskkill /f /im IEDriverServer.exe')

if __name__ == "__main__":
    print local_web_authen(browse = 'ie')
#     t = time.time()
#     clean()
#     print time.time() - t
