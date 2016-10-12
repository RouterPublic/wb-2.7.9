# -*- coding:utf-8 -*-

import os
import time
import logging
from selenium import webdriver

def mail_auth(username, password, timeout=60, browse='ie'):
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
        except:
            pass
        
        for ia in range(30):
            time.sleep(1)
            try:
                
                driver.find_element_by_name("USER_NAME").clear()
                driver.find_element_by_name("USER_NAME").send_keys(username)
                driver.find_element_by_name("USER_PWD").clear()
                driver.find_element_by_name("USER_PWD").send_keys(password)
                driver.find_element_by_name("ONLINE_BTN").click()
            except:
                if ia == 29:
                    driver.quit()
                    clean()
                    return 'Can not open the page of web authentication.'
            else:
                break
        
#        for i in range(30):
#            time.sleep(1)
#            try: 
#                driver.find_element_by_name("GOON_BTN").click()
#            except:
#                if ia == 29:
#                    driver.quit()
#                    clean()
#                    return 'Web authentica failed!'
#            else:
#                break
        for i in range(3):
            try:
                time.sleep(2)
                bd = 'www.baidu.com'
                logging.info('open the url: %s'%bd)
                driver.get(bd)
            except Exception:
                pass
            
            for i in range(30):
                if driver.title == u"百度一下，你就知道" :
                    logging.info('close the browse')
                    driver.quit() 
                    return 'Mail authentication OK!'    
                else:
                    time.sleep(1)
        
        logging.info('close the browse')
        driver.quit() 
        clean()
        return 'Can not open baidu!'
        
    except Exception,e:
        err_msg = 'browse web error: %s'%e
        logging.error(err_msg)
        clean()
        return err_msg

def clean():
    logging.info('clean test...')
    os.popen('taskkill /f /im iexplore.exe')
#     os.popen('taskkill /f /im firefox.exe')
#     os.popen('taskkill /f /im chrome.exe')
#     os.popen('taskkill /f /im chromedriver.exe')
    os.popen('taskkill /f /im IEDriverServer.exe')
    
if __name__ == '__main__':
    print mail_auth("1","1")
    clean()
