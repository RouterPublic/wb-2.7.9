# -*- coding:utf-8 -*-
 
import os
import time
import win32api  
import win32con  
import win32gui
import traceback
from wbpublic import * 

PPTV_PATH = ''

def init_pptv_window(pptv_path):
    
    global pptv_handle  
    os.startfile(pptv_path)
    for i in xrange(10):
        time.sleep(2)
        pptv_handle = None
        win32gui.EnumWindows(enumWindows_callback_func,0)
        if pptv_handle:
            break
        
    if pptv_handle:

        win32gui.ShowWindow(pptv_handle,win32con.SW_RESTORE)
        time.sleep(5)
        
        for i in xrange(12):
            fw_handle = win32gui.GetForegroundWindow()
            if fw_handle != pptv_handle:
                win32gui.SetForegroundWindow(pptv_handle)
                time.sleep(5)
            else:
                break
    else:
        error_msg = 'Can not find any pptv window!'
        raise Exception,error_msg
        
def enumWindows_callback_func(hwnd,extra):
    
    global pptv_handle    # for return pptv handle
    windowtext = win32gui.GetWindowText(hwnd)
    classname = win32gui.GetClassName(hwnd)
    if ('PPTV' in windowtext) and (classname == 'PPLiveGUI'):
        pptv_handle = hwnd
        print hex(pptv_handle)
        
def open_url_video(url):
    
    # ctrl + u
    win32api.keybd_event(win32con.VK_CONTROL,0,0,0)
    win32api.keybd_event(85,0,0,0)
    win32api.keybd_event(85,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(win32con.VK_CONTROL,0,win32con.KEYEVENTF_KEYUP,0)
    
    # input url
    keybd.input_str(url)
    
    # click enter
    keybd.click_enter()
    
def clean():
    os.system('taskkill /f /im PPLive.exe')
    os.system('taskkill /f /im PPAP.exe')
    
def pptv(url):
    init_pptv_window(PPTV_PATH)
    open_url_video(url)
    

if __name__ == '__main__':
    
    try:

        pptv_path = r"D:\Program Files\PPLive\PPTV\PPLive.exe"
        url = 'pptv://0a2lmamao6mlj9iioaWdj9mioZbQpqeco6aknq2Z'
        url = 'pptv://0a2lmamao6mlj9iioaWdj9mioZbQpqeco6aknq2Z'
        url = 'pptv://0a2lmamao6mlj9iioaWdj9mioZbQpqeco6aknq2b'
        init_pptv_window(pptv_path)
        open_url_video(url)
    
    except Exception,e:
        print e
#     raw_input()

