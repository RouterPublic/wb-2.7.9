# -*- coding:utf-8 -*-

import os
import time
import ImageGrab
import win32gui
import win32api
import win32con
from selenium import webdriver
from threading import Thread

def get_window_handle(className,windowName,timeout=60):
    '''
    Get window handle from class name or window name in timeout. If not find, raise a error.
    1.className is a string 
    2.windowName is a string
    3.timeout is a integer in seconds
    
    For example:
    handle = get_window_handle('xunleiobjeck',u'PVP.net 客户端',30)
    '''
    
    t = 0
    t1 = time.time()
    while t < timeout:
        login_hdl = win32gui.FindWindow(className,windowName)
        if login_hdl:
            break
        else:
            time.sleep(1)
            t = time.time() - t1
            
    if login_hdl:
        return login_hdl
    else:
        error_msg = u'Can not find window in %ss! className = %s ; windowName = %s'%(timeout,className,windowName)
        raise Exception,error_msg

def set_window_top(hwnd,pos=None,size=None):
    '''
    Set the window to the topmost window, and move it to specified position in specified size. 
    1. hwnd is the handle to the window
    2. pos is a tuple, (x,y), if it is None, do not move the window
    3. size is a tuple, (width,height), if it is None, do not change the size for the window
    
    For example:
    set_window_top(hwnd,(131,25),(1000,700))
    
    '''
    
    flag = win32con.SWP_SHOWWINDOW
    
    if pos:
        x,y = pos
    else:
        x,y = (0,0)
        flag = win32con.SWP_NOMOVE | flag
        
    if size:
        w,h = size
    else:
        w,h = (0,0)
        flag = win32con.SWP_NOSIZE | flag
        
    win32gui.ShowWindow(hwnd,win32con.SW_RESTORE)
    for i in range(100):
        try:
            time.sleep(0.01)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        else:
            break
    time.sleep(0.1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, w, h, flag)

def get_page_boxx(hwnd):
    
    chwnd1 = win32gui.FindWindowEx(hwnd,None,'Frame Tab',None)
    chwnd2 = win32gui.FindWindowEx(chwnd1,None,'TabWindowClass',None)
    chwnd3 = win32gui.FindWindowEx(chwnd2,None,'Shell DocObject View',None)
    cchwnd = win32gui.FindWindowEx(chwnd3,None,'Internet Explorer_Server',None)
    boxx = win32gui.GetWindowRect(cchwnd)
    return boxx
    
def open_url(browser,url):
    
    try:
        browser.get(url)
    except  Exception:
        pass

def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def clean():
    os.popen('taskkill /f /im iexplore.exe')
    os.popen('taskkill /f /im IEDriverServer.exe')

def run(url,timeout=30):
    try:
        
        os.popen('RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 4351')
        browser = webdriver.Ie()
        
        hwnd = get_window_handle('IEFrame',None,timeout=20)
        set_window_top(hwnd,(0,0),(800,600))
        
        browser.set_page_load_timeout(timeout)
        bbox = get_page_boxx(hwnd)
        initial_his = ImageGrab.grab(bbox).histogram()
        
        web_thread = Thread(target=open_url,args=(browser,url))
        start_time = time.time()
        web_thread.start()
    
        while 1:
            now_his = ImageGrab.grab(bbox).histogram()
            t =  time.time() - start_time
            if  hist_similar(now_his,initial_his) < 0.5:
                break
            elif t > timeout:
                break
        pic = ImageGrab.grab(bbox)
        pic.save(url.split('.')[1]+'.png')
        
        web_thread.join()
        browser.close()
    except Exception,e:
        print e
        clean()
        return 'n/a'
    else:
        clean()
        return round(t,3)
 
if __name__ == "__main__":
    url = 'http://www.qq.com'
#     for i in range(10):
    #print run(url)
#     hwnd = get_window_handle('IEFrame',None,timeout=20)
#     print get_page_boxx(hwnd)
    print run(url,10)
    

    
    
