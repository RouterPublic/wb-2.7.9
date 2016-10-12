# -*- coding:utf-8 -*-

import os
import time
import win32api  
import win32con  
import win32gui
import random
import ImageGrab, Image, ImageChops

class Keyboard(object):
    
    def input_char(self,character):

        shift_char = ['~','!','@','#','$','%','^','&','*','(',')','_',
                      '+','{','}','|',':','"','<','>','?','A','B','C',
                      'D','E','F','G','H','I','J','K','L','M','N','O',
                      'P','Q','R','S','T','U','V','W','X','Y','Z']
         
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
        
    def input_str(self,string): 
        for char in string:
            self.input_char(char)
        
    def click_enter(self):
        win32api.keybd_event(win32con.VK_RETURN,0,0,0)
        win32api.keybd_event(win32con.VK_RETURN,0,win32con.KEYEVENTF_KEYUP,0)
        
    def click_tab(self):
        win32api.keybd_event(win32con.VK_TAB,0,0,0)
        win32api.keybd_event(win32con.VK_TAB,0,win32con.KEYEVENTF_KEYUP,0)

    def click_backspace(self):
        win32api.keybd_event(win32con.VK_BACK,0,0,0)
        win32api.keybd_event(win32con.VK_BACK,0,win32con.KEYEVENTF_KEYUP,0)    

class Mouse(object):
    
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 2
    
    def move(self,x,y):
        win32api.SetCursorPos((x,y))
        
    def click(self,butten):
        if butten == self.LEFT_BUTTON:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
            curpos = win32api.GetCursorPos()
            win32api.SetCursorPos(curpos)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        if butten == self.RIGHT_BUTTON:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)
    
keybd = Keyboard()
mouse = Mouse()

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
    for i in xrange(100):
        try:
            time.sleep(0.01)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        else:
            break
    time.sleep(0.1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, w, h, flag)
    

def find_bmp_in_bmp(small,big,accuracy=1):
    '''
    '''

    if not isinstance(small,Image.Image):
        msg = 'The "small" is not a PIL "Image" object'
        raise TypeError,msg
    if not isinstance(big,Image.Image):
        msg = 'The "big" is not a PIL "Image" object'
        raise TypeError,msg

    bw,bh = big.size
    sw,sh = small.size
    if (sw*sh) > (bw*bh):
        msg = 'The big bmp is er than the small bmp'
        raise ValueError,msg
    
    bdata = big.getdata()
    sdata = small.getdata()
#     bcoo = [(x, y) for x in xrange(bw) for y in xrange(bh)]
    scoo = [(x, y) for x in xrange(sw) for y in xrange(sh)]
    if sw*sh >= 2500:
        scoo = random.sample(scoo,2500)
    else:
        random.shuffle(scoo)
        
    rscoo = random.sample(scoo,1)   # try three times
    for (sx,sy) in rscoo:
        sid = sy*sw + sx
        scolor = sdata[sid]
        for bid in xrange(bw*bh):
            bcolor = bdata[bid]
            if (abs(scolor[0]-bcolor[0])>5) or \
               (abs(scolor[1]-bcolor[1])>5) or \
               (abs(scolor[2]-bcolor[2])>5):
                pass
            else: 
                by = bid//bw
                bx = bid%bw
                sy0 = by - sy
                sx0 = bx - sx
                sym = sy0 + sh
                sxm = sx0 + sw
                f_num = 0
                p_num = 0
                if sy0<0 or sx0<0 or sym>bh or sxm>bw:
                    continue
                else:
                    for (sx_,sy_) in scoo:
                        sid_ = sy_*sw + sx_
                        bid_ = (sy0+sy_)*bw+(sx0+sx_)
                        scolor_ = sdata[sid_]
                        bcolor_ = bdata[bid_]
                        if (abs(bcolor_[0]-scolor_[0])>5) or \
                           (abs(bcolor_[1]-scolor_[1])>5) or \
                           (abs(bcolor_[2]-scolor_[2])>5):
                            f_num += 1
                        else:
                            p_num += 1
                        f_rate = float(f_num)/len(scoo)
                        p_rate = float(p_num)/len(scoo)
                        if f_rate > (1-accuracy):
                            break
                        elif p_rate >= accuracy:
                            return sx0,sy0  
    
def grab_screen_bmp(mode='ps'):
    '''
    grab screen to save as a bmp
    mode : 'ps'  --- press down 'print screen' button
           'pil' --- pil grab function
    '''
    if mode == 'ps':
        for i in xrange(3):
            win32api.keybd_event(win32con.VK_SNAPSHOT,0,0,0)
            win32api.keybd_event(win32con.VK_SNAPSHOT,0,win32con.KEYEVENTF_KEYUP,0)
            time.sleep(0.1)
            pic = ImageGrab.grabclipboard()
            if isinstance(pic, Image.Image):
                break
        return pic
    elif mode == 'pil':
        pic = ImageGrab.grab()
        return pic
    else:
        raise TypeError,'the mode is incorrect'
    
def find_bmp_in_screen(bmp,timeout=30,mode='ps'):
    ''' 
    Find the bmp from the screen in timeout and return the bmp's coordinate. If not found, return None.
    1.bmp must be a autopy Bitmap object
    
    For example:
    import autopy
    inbmp =  autopy.bitmap.Bitmap.open(pic_pth)
    coordinate = find_bmp_in_window(hwnd,inbmp,30)
    '''
    
    t = 0
    t1 = time.time()
    while t <= timeout:
        screen = grab_screen_bmp(mode=mode)
        coordinate = find_bmp_in_bmp(bmp,screen)
        if coordinate:
            break
        else:
            time.sleep(1)
            t = time.time() - t1
    return coordinate

def grab_window_bmp(hwnd=None):
    '''
    grab the window to save as a bmp
    '''
    
    # try 3 times, if failed, raise error "pic object has no attribute 'save'" 
    for i in xrange(3):
        set_window_top(hwnd)
        time.sleep(0.5)
        
        # Alt + PrtScn
        win32api.keybd_event(win32con.VK_MENU,0,0,0)
        win32api.keybd_event(win32con.VK_SNAPSHOT,0,0,0)
        win32api.keybd_event(win32con.VK_SNAPSHOT,0,win32con.KEYEVENTF_KEYUP,0)
        win32api.keybd_event(win32con.VK_MENU,0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(0.1)
        
        pic = ImageGrab.grabclipboard()
        if isinstance(pic, Image.Image):
            break
 
    return pic
    
def find_bmp_in_window(hwnd,bmp,timeout=30):
    '''
    Find the bmp from the window in timeout and return the bmp's coordinate. If not found, return None.
    1.hwnd is the handle to the window
    2.bmp must be a autopy Bitmap object
    3.timeout is a integer in seconds, if timeout = 0, only do one times
    
    For example:
    import autopy
    inbmp =  autopy.bitmap.Bitmap.open(pic_pth)
    coordinate = find_bmp_in_window(hwnd,inbmp,30)
    
    '''
    
    t = 0
    t1 = time.time()
    while t <= timeout:
        window = grab_window_bmp(hwnd)
        coordinate = find_bmp_in_bmp(bmp,window)
        if coordinate:
            break
        else:
            time.sleep(1)
            t = time.time() - t1
    return coordinate

def click_pic_in_screen(pic_pth,timeout=30,mode='ps',errflg=True):
    '''
    If you want to click a picture in the screen, use this function. You must give the picture's path.
    
    For example:
    pic_pth = r'f:\pic.bmp'
    click_pic_in_screen(hwdl,pic_pth)
    
    '''
    try:
        bt_bmp = Image.open(pic_pth)
    except Exception,e:
        err_msg = '%s  ---pic_pth: %s'%(e,pic_pth)
        raise Exception,err_msg
        
    coordinate = find_bmp_in_screen(bmp=bt_bmp,timeout=timeout,mode=mode)
    if not coordinate:
        error_msg = u'Can not find button in screen, please check or reload bmp. Path: %s'%pic_pth
        if errflg:
            raise Exception,error_msg
        else:
            pass
    else:
        x,y = coordinate
        bwidth,bheight = bt_bmp.size
        x = x + int(bwidth/2)
        y = y + int(bheight/2)
        mouse.move(x,y)
        mouse.click(mouse.LEFT_BUTTON)
    
def click_pic_in_window(hwdl,pic_pth,timeout=30,errflg=True):
    '''
    If you want to click a picture in a window, use this function. You must give the picture's path.
    
    For example:
    pic_pth = r'f:\pic.bmp'
    click_pic_in_window(hwdl,pic_pth)
    
    '''
    try:
        bt_bmp = Image.open(pic_pth)
    except Exception,e:
        err_msg = '%s  ---pic_pth: %s'%(e,pic_pth)
        raise Exception,err_msg
        
    coordinate = find_bmp_in_window(hwdl, bt_bmp, timeout)
    if not coordinate:
        error_msg = u'Can not find button in window, please check or reload bmp. Path: %s'%pic_pth
        if errflg:
            raise Exception,error_msg
        else:
            pass
    else:
        x,y = coordinate
        bwidth,bheight = bt_bmp.size
        x = x + int(bwidth/2)
        y = y + int(bheight/2)
        mouse.move(x,y)
        set_window_top(hwdl,(0,0))
        mouse.click(mouse.LEFT_BUTTON)

if __name__ == '__main__':
    t = time.time()
    try:
        LOL_BMP_DIR = "../bmp/cf/"
        QUERXZ = LOL_BMP_DIR + "beifdq.bmp" #确认选择
        #QUERXZ2 = LOL_BMP_DIR + "jiand1.bmp"
#        screen = LOL_BMP_DIR+"07.bmp"
#        handle = get_window_handle('PPLiveGUI','PPTV')
#        bt_bmp = Image.open(QUERXZ)
        #bt_bmp2 = Image.open(QUERXZ2)
#        screen = Image.open(screen)
#        print find_bmp_in_bmp(bt_bmp,screen)
#        im3 = ImageChops.invert(bt_bmp2)
#        im = Image.blend(bt_bmp,im3,0.5)
#        print im.getcolors()
#        im.save('../bmp/xxx.bmp')
#        u,i,w,h = im.getbbox()
#        for y in range(h) :
#            for x in range(w):
#                print (x,y),im.getpixel((x,y))

#        bt_bmp = bitmap.Bitmap.open(QUERXZ2)
#        screen = bitmap.Bitmap.open(screen)
#        coordinate = screen.find_bitmap(bt_bmp)
#        print coordinate
#        print find_bmp_in_window(handle,bt_bmp,0)
#        print hex(handle)
#        grab_window_bmp(handle)
#         set_window_top(handle,(131,25),(1000,700))
#        time.sleep(5)
#        keybd.input_str('wwwssdfdaf')
        
        print win32api.GetCursorPos()
        
    except Exception,e:
        print e
    finally:
        print time.time()-t
#     raw_input()
