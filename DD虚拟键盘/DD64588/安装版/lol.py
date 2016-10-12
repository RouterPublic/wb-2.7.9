# -*- coding:utf-8 -*-

import ctypes
import os
import re
import time
import win32api  
import win32con  
import win32gui
import random
import logging
import traceback
from wbpublic import * 
import ImageGrab, Image, ImageChops
from autopy import bitmap, mouse

LOL_PATH1    = u"X:/网络游戏/英雄联盟/"
LOL_BMP_DIR = "./bmp/lol/"
JINRYX   = LOL_BMP_DIR + "jinryx.bmp"       #进入游戏
FUWQLB   = LOL_BMP_DIR + "fuwqlb.bmp"       #服务器列表
PLAY     = LOL_BMP_DIR + "play.bmp"         #play
XITPPDY  = LOL_BMP_DIR + "xitppdy.bmp"      #系统匹配队友
XIANZKS  = LOL_BMP_DIR + "xianzks.bmp"      #现在开始
SUIJXZ   = LOL_BMP_DIR + "suijxz.bmp"       #随机选择（英雄）
QUED     = LOL_BMP_DIR + "qued.bmp"         #确定（选择英雄）
FENGHQR  = LOL_BMP_DIR + "fenghaoqr.bmp"    #封号确认（登录游戏后）
CHENGFQR = LOL_BMP_DIR + "chengfaqr.bmp"    #惩罚确认（登录游戏后）
ZAILYJ   = LOL_BMP_DIR + "zailyj.bmp"       #再来一局
JIXYXSL  = LOL_BMP_DIR + "jixyx_shengl.bmp" #胜利后继续游戏
JIXYXSB  = LOL_BMP_DIR + "jixyx_shib.bmp"   #失败后继续游戏
HUIDDT   = LOL_BMP_DIR + "huiddt.bmp"       #回到大厅
QUERXZ   = LOL_BMP_DIR + "querxz.bmp"       #确认选择（选择服务器后）
MINGM    = LOL_BMP_DIR + "mingm.bmp"        #命名你的召唤师
MINGMBOX = LOL_BMP_DIR + "mingmbox.bmp"     #命名输入框
MINGMJS  = LOL_BMP_DIR + "mingmjs.bmp"      #命名接受      
TOUXQR   = LOL_BMP_DIR + "touxqr.bmp"       #头像确认
DASNDM   = LOL_BMP_DIR + "dasndm.bmp"       #大师你懂吗水平
SHUIPQR  = LOL_BMP_DIR + "shuipqr.bmp"      #水平确认
SHIZF    = LOL_BMP_DIR + "shizf.bmp"        #实战训练“否”按钮
FENGHGB  = LOL_BMP_DIR + "fenghgb.bmp"      #封号关闭（一局游戏完成后）
T_GUANB  = LOL_BMP_DIR + "!_guanb.bmp"      #“！”（查看游戏状态）消息关闭按钮
RENJDZ   = LOL_BMP_DIR + "renjdz.bmp"       #人机对战
JINDDZ   = LOL_BMP_DIR + "jingddz.bmp"      #经典对战
ZHAOHSXG = LOL_BMP_DIR + "zhaohsxg.bmp"     #召唤师峡谷
JIAND    = LOL_BMP_DIR + "jiand.bmp"        #简单（游戏难度）
ZIDYYX   = LOL_BMP_DIR + "zidyyx.bmp"       #自定义游戏
CHUANGJYX = LOL_BMP_DIR + "chuangjyx.bmp"   #创建游戏
MENU_5   = LOL_BMP_DIR + "5_menu.bmp"       #队伍规模5
MENU_1   = LOL_BMP_DIR + "1_menu.bmp"       #队伍规模1
TUZHSXG  = LOL_BMP_DIR + "tuzhsxg.bmp"      #图片召唤师峡谷
FANGJMM  = LOL_BMP_DIR + "fangjmm.bmp"      #房间密码框
CHUANGJFJ = LOL_BMP_DIR + "chuangjfj.bmp"   #创建房间
TIANJJQR = LOL_BMP_DIR + "tianjjqr.bmp"     #添加机器人
KAISYX   = LOL_BMP_DIR + "kaisyx.bmp"       #开始游戏
SHI_WUJL = LOL_BMP_DIR + "shi_wujl.bmp"     #“是”按钮（无奖励）
SHI_WUJL2 = LOL_BMP_DIR + "shi_wujl2.bmp"   #“是”按钮2（无奖励）
NIUQSL_D = LOL_BMP_DIR + "niuqsl_d.bmp"     #扭曲森林（被选择）
NIUQSL_U = LOL_BMP_DIR + "niuqsl_u.bmp"     #扭曲森林（未选择）
AIONY_D  = LOL_BMP_DIR + "aiony_d.bmp"      #艾欧尼亚（被选择）
AIONY_U  = LOL_BMP_DIR + "aiony_u.bmp"      #艾欧尼亚（未选择）
TIANFFOU = LOL_BMP_DIR + "tianffou.bmp"     #新季度新天赋“否”按钮
SHIPGB   = LOL_BMP_DIR + "shipgb.bmp"       #视频关闭按钮
DIANSTX  = LOL_BMP_DIR + "dianstX.bmp"      #电视台关闭按钮
XINSLBX  = LOL_BMP_DIR + "xinslbX.bmp"      #新手礼包关闭按钮
LINGQXRWX = LOL_BMP_DIR + "lingqxrwX.bmp"   #领取新任务关闭按钮
YINGXSKX = LOL_BMP_DIR + "yingxskX.bmp"     #英雄时刻关闭按钮
XUNLKTX  = LOL_BMP_DIR + "xunlktX.bmp"      #训练课堂关闭按钮
JIASQX   = LOL_BMP_DIR + "jiasqX.bmp"       #游戏圈-迅游加速器关闭按钮
SHOP     = LOL_BMP_DIR + "shop.bmp"         #进入商店
BUY      = LOL_BMP_DIR + "buy.bmp"          #买红
    
def start_lol():
    try:
        cwd = os.getcwd()
        os.chdir(LOL_PATH1.encode('gbk'))
        os.popen('GameCheck.exe')
        os.chdir(cwd)
    except:
        raise Exception,'Can not find GameCheck.exe'
    
def login_game(username,password):
    
    try:
        logging.info("Step1: start game and login")
        start_lol()
       #time.sleep(600)
        hlogin = get_window_handle(None,u'英雄联盟登录程序')
        set_window_top(hlogin,(0,0))
        bmp_jryx = Image.open(JINRYX)
        coordinate = find_bmp_in_window(hlogin,bmp_jryx)
            
        if not coordinate:
            error_msg = u'Can not find "enter the game" button, please check.\
                You can reload the "enter the game" button bmp.'
            raise Exception,error_msg
    
        mouse.move(1090, 245)
        mouse.click(mouse.LEFT_BUTTON)

        logging.info("Step1: username is %s"%(username))  
        keybd.input_str(username)
        time.sleep(0.5)
        
        keybd.click_tab()
        time.sleep(30)

#          logging.info("Step1: password is %s"%(password))   
#          keybd.input_str(password)
#          time.sleep(0.5)
          logging.info("Step1: password is %s"%(password))
          dd = ctypes.WinDLL("DD32.dll")
          dd.DD_str("volans")
          time.sleep(0.5)
            
        keybd.click_enter()
        
    except Exception,e:
        err_msg = u'logging game error, error message: %s'%e
        raise Exception,err_msg

def server_choise(serverid):
    
    try:
        logging.info("Step2: choice server")
        hlogin = get_window_handle(None,u'英雄联盟登录程序')
        click_pic_in_window(hlogin,FUWQLB)
        if serverid == 1:
            click_pic_in_window(hlogin,AIONY_U,10,errflg=False)
        if serverid == 2:
            click_pic_in_window(hlogin,NIUQSL_U,10,errflg=False)

        click_pic_in_window(hlogin,QUERXZ)
        
    except Exception,e:
        err_msg = u'server choise error, error message: %s'%e
        raise Exception,err_msg
    
def new_player():
    
    try:
        logging.info("Build a new player.")
        hpvp = get_window_handle(None,u'PVP.net 客户端')
        
        # 点击命名输入框
        click_pic_in_window(hpvp,MINGMBOX)
        name = 'T'
        for i in xrange(12):
            name = name + str(random.randint(0,9)) 
        keybd.input_str(name)
        
        # 点击命名接受
        click_pic_in_window(hpvp,MINGMJS)
        
        # 点击头像确认
        click_pic_in_window(hpvp,TOUXQR)
        
        # 点击大师你懂吗水平
        click_pic_in_window(hpvp,DASNDM)
        
        # 点击水平确认
        click_pic_in_window(hpvp,SHUIPQR)
        
        # 点击实战训练否按钮
        click_pic_in_window(hpvp,SHIZF)
    
    except Exception,e:
        err_msg = u'new player error, error message: %s'%e
        raise Exception,err_msg
    
def load_game():
    try:

        logging.info("Step3: build a room and select the hero")
        hpvp = get_window_handle(None,u'PVP.net 客户端')
        
        # 是否封号，封号则触发异常
        bmp_fhqr = Image.open(FENGHQR)
        coordinate = find_bmp_in_window(hpvp, bmp_fhqr)
        if coordinate:
            
            #kill process
            msg = 'This usename has been frozen!'
            raise Exception,msg
        
        # 新天赋“否”
        click_pic_in_window(hpvp,TIANFFOU,0,errflg=False)
        
        # 检查是否有惩罚提示，点击确定，没有不触发异常
        click_pic_in_window(hpvp,CHENGFQR,0,errflg=False)
        
        # 新天赋“否”,不确定先后
        click_pic_in_window(hpvp,TIANFFOU,0,errflg=False)
        
        # 检查是否需要新建召唤师
        bmp_mingm = Image.open(MINGM)
        coordinate = find_bmp_in_window(hpvp, bmp_mingm, 0)
        if coordinate:
            new_player()

        # 关闭新任务领取提示
        click_pic_in_screen(LINGQXRWX,5,errflg=False)

        # 关闭电视台
        click_pic_in_screen(DIANSTX,5,errflg=False)

        # 关闭训练课堂
        click_pic_in_screen(XUNLKTX,5,errflg=False)

        # 关闭“！”（查看游戏状态）的弹出信息
        click_pic_in_window(hpvp,T_GUANB,0,errflg=False)
        
        # 点击“Play”
        click_pic_in_window(hpvp,PLAY)

        # 关闭弹出视频
        click_pic_in_window(hpvp,SHIPGB,5,errflg=False)

        # 关闭领取新手礼包
        click_pic_in_window(hpvp,XINSLBX,5,errflg=False)

        # 关闭英雄时刻
        click_pic_in_window(hpvp,YINGXSKX,5,errflg=False)

        # 关闭加速器
        click_pic_in_window(hpvp,JIASQX,5,errflg=False)
        
        # 建房
        click_pic_in_window(hpvp,ZIDYYX,5,errflg=False)

        # 创建游戏
        click_pic_in_window(hpvp,CHUANGJYX,5,errflg=False)

        # 选择地图和输入密码
        click_pic_in_window(hpvp,TUZHSXG,5,errflg=False)
        click_pic_in_window(hpvp,FANGJMM,5,errflg=False)
        keybd.input_str('4830253')

        # 创建房间和添加机器人
        click_pic_in_window(hpvp,CHUANGJFJ,5,errflg=False)
        for i in range(5):
            click_pic_in_window(hpvp,TIANJJQR,5,errflg=False)

        # 开始游戏和点击按钮
        click_pic_in_window(hpvp,KAISYX,5,errflg=False)
        click_pic_in_window(hpvp,SHI_WUJL,5,errflg=False)
        click_pic_in_window(hpvp,SHI_WUJL2,5,errflg=False)
        
        # 点击“系统匹配队友”
        #click_pic_in_window(hpvp,XITPPDY)
        
        # 点击“现在开始”
        #click_pic_in_window(hpvp,XIANZKS,120)
    
        # 点击“随机选择”
        click_pic_in_window(hpvp,SUIJXZ)
    
        # 点击“确定”
        click_pic_in_window(hpvp,QUED)
    
        # 判断游戏是否开始，没有等待重新建立游戏，等待时长10分钟
        starttime = time.time()
        bmp_xzks = Image.open(XIANZKS)
        while not win32gui.FindWindow('RiotWindowClass',u'League of Legends (TM) Client'):
            time.sleep(10)
            t = time.time() - starttime
            if t > 600:
                err_msg = 'cannot load a game in timeout 10 minutes'
                raise Exception,err_msg
      
    except Exception,e:
        err_msg = u'load game error, error message: %s'%e
        raise Exception,err_msg
      
def play_game():
    
    try:
        logging.info("Step4: walk hero in the game")
        hclient = get_window_handle('RiotWindowClass',u'League of Legends (TM) Client',5)
        
        # 玩游戏，如果1小时后仍检测不到“继续游戏按钮”，可能发生异常或者游戏时长超过1小时
        t1 = time.time()
        t = 0
        bmp_jxyxsl = Image.open(JIXYXSL)
        bmp_jxyxsb = Image.open(JIXYXSB)
        while True:
            time.sleep(10)
            if not win32gui.FindWindow('RiotWindowClass',u'League of Legends (TM) Client'):
                break
            else:
                if find_bmp_in_window(hclient, bmp_jxyxsl, 0):
                    click_pic_in_window(hclient,JIXYXSL)
                    break
                elif find_bmp_in_window(hclient, bmp_jxyxsb, 0):
                    click_pic_in_window(hclient,JIXYXSB)
                    break
                elif t > 5400:
                    err_msg = 'the time of playing game out of 1 hour'
                    raise Exception,err_msg
                else:
                    
                    #buy()
                    #for i in range(5):
                    kill_body()
                    t = time.time() - t1
            
    except Exception,e:
        err_msg = u'play game error, error message: %s'%e
        raise Exception,err_msg

def kill_body():
    # 前往地图中心位置
    time.sleep(60)
    mouse.move(1296, 676)
    mouse.click(mouse.LEFT_BUTTON)
    random_click()
                    
    # 点击“继续游戏”按钮所在的区域
    box = (600,300,770,600)#(min_x,min_y,max_x,max_y)
    ystep = int((box[3]-box[1])/40)
    for i in range(40):
        y = box[1]+i*ystep
        mouse.move(680, y)
        mouse.click(mouse.LEFT_BUTTON)
        time.sleep(0.1)

                        
def again_game():
    
    try:
        logging.info("Step5: again another game")
        hpvp = get_window_handle(None,u'PVP.net 客户端')
        
        # 检测到有封号关闭按钮
        bmp_fhgb = Image.open(FENGHGB)
        coordinate = find_bmp_in_window(hpvp, bmp_fhgb)
        if coordinate:
            msg = "We get a 'close' button and the game must be closed."
            click_pic_in_window(hpvp,FENGHGB)
            raise Exception,msg
        
        click_pic_in_window(hpvp,HUIDDT)
        
    except Exception,e:
        err_msg = u'again game error, error message: %s'%e
        raise Exception,err_msg

def buy():

    try:
        # 前往商店所在位置
        mouse.move(1181, 760)
        mouse.click(mouse.LEFT_BUTTON)
        mouse.move(747,369)
        mouse.click(mouse.RIGHT_BUTTON)
        
        click_pic_in_screen(SHOP,1,errflg=False)
        click_pic_in_screen(BUY,1,errflg=False)
        mouse.click(mouse.LEFT_BUTTON)
        # 缺少关闭商店
    except:
        pass

def random_click():
    
    try:
        
        key_list = ['q','w','e','r']
        for i in range(10):
            wait_time = random.uniform(0,0.2)
            action = random.randint(0,1)
            if action == 0:
                key = random.choice(key_list)
                keybd.input_char(key)
            elif action == 1:
                x = random.randint(600,700)
                y = random.randint(300,400)
                mouse.move(x,y)
                mouse.click(mouse.RIGHT_BUTTON)
            time.sleep(wait_time)
        #mouse.move(1350,590)
        #mouse.click(mouse.RIGHT_BUTTON)
        
    except Exception,e:
        err_msg = u'random click error, error message: %s'%e
        raise Exception,err_msg
  
def clean():
    os.popen('taskkill /f /im LolClient.exe')
    os.popen('taskkill /f /im Client.exe') 
    os.popen('taskkill /f /im "League of Legends.exe"')
    os.popen('taskkill /f /im "lol.launcher_tencent.exe"')
    os.popen('taskkill /f /im BsSndRpt.exe')
    os.popen('taskkill /f /im #bugreport.exe')

def state():
    tasklist = os.popen('tasklist').read()
    if "League of Legends.exe" in tasklist:
        return True
    else:
        return False
    
def play_lol(username,password,serverid):
    
    try:
        login_game(username,password)
        server_choise(serverid)
        load_game()
        play_game()
        again_game()
            
    except Exception,e:
        err_msg = u'%s'%e
        logging.error(err_msg)
#         cur_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())
#         path = './log/error_screen/%s.bmp'%cur_time
#         grab_screen_bmp(path)
        clean()
        return err_msg
    
    else:
        clean()
        return None
    
def read_ping(log_path):

    return_list = []
    log = open(log_path)
    for log_line in log:
        match = re.search("(.*):.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*",log_line)
        if match:
            start_time = match.groups()[0]
            stime_list = re.split('[T-]',start_time)
            for i in range(len(stime_list)):
                stime_list[i] = int(stime_list[i])
 
        match2 = re.search("(\d*),\d*\..*,\d*,\d*,\d*,\d*,\d*,\d*,(\d*),\d*,\d*,\d*,\d*,\d*",log_line)
        if match2:
            time_msec,ping = match2.groups()
            
            sec = stime_list[5] + int(time_msec)//1000
            
            if sec >= 60:
                minu = stime_list[4] + (sec//60)
                sec = sec % 60 
            else:
                minu = stime_list[4]
                
            if minu >= 60:
                hour = stime_list[3] + (minu//60)
                minu = minu % 60
            else:
                hour = stime_list[3]

            if hour >= 24:
                day = stime_list[2] + (hour//24)
                hour = hour % 24
            else:
                day = stime_list[2]

            month = stime_list[1]
            year = stime_list[0]
                
            return_list.append(((year,month,day,hour,minu,sec),int(ping)))
    return return_list

def get_all_ping():
    
    path = u'X:/网络游戏/英雄联盟/Game/Logs/Network Logs/'
    is_exists = os.path.exists(path)
    if is_exists:
        
        ping_list = []
        
        wk = os.walk(path)
        for root,dirs,files in wk:
            for fil in files:
                if len(fil) > 10:
                    if fil[-10:] == "netlog.txt":
                        log_path = root + fil
                        ping_list = ping_list + read_ping(log_path)
                        
        return sorted(ping_list)

    else:
        return None
    
if __name__ == '__main__':
#     print get_all_ping()
#    serverid = 1
#    server_path_list = []
#     if serverid == 1:
#    LOL_BMP_DIR = "../bmp/lol/"
#    servers_path = LOL_BMP_DIR  + 'Servers1/'
#    for root,dir,files in os.walk(servers_path):
#        for file in files:
#            if 'server_' in file:
#                server_path_list.append((root+file))
                
#    print random.choice(server_path_list)
     try:
         #username = '1819686283'
         #password = 'volans'
         #print play_lol(username,password,1)
         pass
     except Exception,e:
         print traceback.format_exc()
#     finally:
#         raw_input()
        
