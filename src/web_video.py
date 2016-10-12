# -*- coding:utf-8 -*-

import os
import time
import logging
from selenium import webdriver

def web_video(url=None,runtime=10,timeout=60,browse='ie'):
    '''
    1. url is a string, define a url to open the video
    2. runtime is a integer, define a period of time(seconds) to watch the video
    3. timeout is a integer, define a timeout(seconds) when loading the web 
    4. browse is a string, define the browse which you choose
    '''
    logging.info('start browse web...')
    if url is None:
        url = "http://www.hao123.com/"
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
        print driver.get_cookies()
        driver.set_page_load_timeout(timeout)
        try:
            logging.info('open the url: %s'%url)
            driver.get(url)
        except Exception,e:
            pass
        print driver.get_cookies()
        logging.info('wait play web video %s minutes...'%runtime)
        runtime_sec = runtime*60
        time.sleep(runtime_sec)
        
        logging.info('close the browse')
        driver.quit()
        
    except Exception,e:
        err_msg = 'watch web video error: %s'%e
        logging.error(err_msg)
        return err_msg
    
    else:
        return None

def clean():
    logging.info('clean the web_video')
    os.system('taskkill /f /im iexplore.exe')
    os.system('taskkill /f /im firefox.exe')
    os.system('taskkill /f /im chrome.exe')
    os.system('taskkill /f /im chromedriver.exe')
    os.system('taskkill /f /im IEDriverServer.exe')

if __name__ == "__main__":
#     web_video('http://v.youku.com/v_show/id_XNDMzNDAzNjQw.html',runtime = 2)
    clean()
