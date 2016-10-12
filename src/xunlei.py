# -*- coding:utf-8 -*-

import os
import time
import win32api  
import win32con  
import win32gui
import wbpublic

xunlei_path = r"C:\Program Files\Thunder Network\Thunder\Program\Thunder.exe"

def init_xunlei_window(xunlei_path):
    
    os.startfile(xunlei_path)
    for i in xrange(30):
        time.sleep(2)
        xunlei_handle = win32gui.FindWindow('XLUEFrameHostWnd',u'迅雷7')
        if xunlei_handle:
            break
    
    if xunlei_handle:
        wbpublic.set_window_top(xunlei_handle, 0, 0, 800, 600)
#         win32gui.ShowWindow(xunlei_handle,win32con.SW_RESTORE)
#         print xunlei_handle,'xunlei'
#         time.sleep(5)
#         
#         for i in xrange(12):
#             fw_handle = win32gui.GetForegroundWindow()
#             print fw_handle,'top_1'
#             if fw_handle != xunlei_handle:
#                 win32gui.SetForegroundWindow(xunlei_handle)
#                 time.sleep(5)
#             else:
#                 break
#     else:
#         error_msg = 'Can not find any pptv window!'
#         raise Exception,error_msg
        
def new_a_mission(url):
    
    url = "http://pubnet.sandai.net:8080/20/8ac092c871003a29c8609c596a0a2ba126236d0a/\
fedf65f19e5b9ed71fb87a6742b52d4133f69463/12770320/200000/0/f2b1e/0/0/12770320/0/i\
ndex=0-13636/indexmd5=c626d3c975caafa456beb69a4c0599c1/37fb0706afc40d2e34e9029e4b\
0e2837/e1af1e286f4b042b580a44f6d46ec3da/fedf65f19e5b9ed71fb87a6742b52d4133f69463.\
flv.xv?type=vod&movieid=184342&subid=940877&ext=.xv"
    
    
    win32api.keybd_event(win32con.VK_CONTROL,0,0,0)
    win32api.keybd_event(78,0,0,0)
    win32api.keybd_event(78,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(win32con.VK_CONTROL,0,win32con.KEYEVENTF_KEYUP,0)
    
    time.sleep(2)
    nmw_handle = win32gui.FindWindow('XLUEModalHostWnd',u'新建任务')
    for i in xrange(12):
        fw_handle = win32gui.GetForegroundWindow()
        print fw_handle,'top_2'
        if fw_handle != nmw_handle:
            win32gui.SetForegroundWindow(nmw_handle)
            time.sleep(5)
        else:
            win32gui.MoveWindow(nmw_handle,0,0,0,0,0)
            click_at_pos(40,80)
            for character in url:
                click_keybd(character)
            time.sleep(5)
            click_at_pos(370,450)
            break
    
    print nmw_handle,'mission'
    print win32gui.GetForegroundWindow(),'top_2'
    
def click_at_pos(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

def click_keybd(character):
    shift_char = ['~','!','@','#','$','%','^','&','*','(',')','_','+','{','}','|',':','"','<','>','?'] 
    hkl = win32api.LoadKeyboardLayout("00000409")
    char_code = win32api.VkKeyScanEx(character,hkl)
    if character in shift_char:
        win32api.keybd_event(win32con.VK_LSHIFT,0,0,0)
        win32api.keybd_event(char_code,0,0,0)
        win32api.keybd_event(char_code,0,win32con.KEYEVENTF_KEYUP,0)
        win32api.keybd_event(win32con.VK_LSHIFT,0,win32con.KEYEVENTF_KEYUP,0)
    else:
        win32api.keybd_event(char_code,0,0,0)
        win32api.keybd_event(char_code,0,win32con.KEYEVENTF_KEYUP,0)    
    
    
if __name__ == '__main__':
    try:
        init_xunlei_window(xunlei_path)
        new_a_mission('')
   
    except Exception,e:
        print e
    raw_input()

#     url = '~!@#$%^&*()_+|}{":?><'
#     time.sleep(10)
#     for i in url:
#         click_keybd(i)
#         print i
    
