# -*- coding:utf-8 -*-

import os
import time
import logging
from selenium import webdriver

    
def wx_web_authen(url,timeout=60,browse='ie'):
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
            logging.info('open the url: %s'%url)
            driver.get(url)
        except Exception:
            pass
        time.sleep(1)
        
        for i in range(30):
            try:
                driver.find_element_by_css_selector("body")
            except Exception:
                pass
            else:
                if driver.find_element_by_css_selector("body").text == 'Login Succeed!':
                    break
            time.sleep(1)
        
        try:
            logging.info('open the baidu')
            driver.get('www.baidu.com')
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
    logging.getLogger().setLevel(logging.INFO)
    print wx_web_authen('12345.com')
#     t = time.time()
#     clean()
#     print time.time() - t
