# -*- coding:utf-8 -*-

import os
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

LOL_PATH    = u"X:\网络游戏\英雄联盟\GameCheck.exe"
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
NIUQSL_D = LOL_BMP_DIR + "niuqsl_d.bmp"     #扭曲森林（被选择）
NIUQSL_U = LOL_BMP_DIR + "niuqsl_u.bmp"     #扭曲森林（未选择）
AIONY_D  = LOL_BMP_DIR + "aiony_d.bmp"      #艾欧尼亚（被选择）
AIONY_U  = LOL_BMP_DIR + "aiony_u.bmp"      #艾欧尼亚（未选择）
TIANFFOU = LOL_BMP_DIR + "tianffou.bmp"     #新季度新天赋“否”按钮

QQ_PATH    = u"X:\聊天工具\QQ\Bin\QQ.exe"
QQ_BMP_DIR = "./bmp/qq/"
DENGLQQ  = QQ_BMP_DIR + "denglqq.bmp"       #登陆QQ
QHZKSDL  = QQ_BMP_DIR + "qiehzksdl.bmp"     #切换至快速登录
KSDLQD   = QQ_BMP_DIR + "ksdlqued.bmp"      #快速登录确定
QQZXH    = QQ_BMP_DIR + "qqzxh.bmp"         #qq最小化

def login_qq(username, password):
    
    try:
        logging.info("Step1: start qq and login")
        os.startfile(QQ_PATH)
        logging.info("Step1: start qq and login 1")
        hlogin = get_window_handle(None,u'QQ')
        bmp_dlqq = Image.open(DENGLQQ)
        logging.info("Step1: start qq and login 2")
        coordinate = find_bmp_in_window(hlogin,bmp_dlqq)
            
        if not coordinate:
            error_msg = u'Can not find “enter the qq” button, please check.\
                You can reload the “enter the qq” button bmp.'
            raise Exception,error_msg
        logging.info("Step1: start qq and login 3")
        
        mouse.move(752, 432)
        mouse.click(mouse.LEFT_BUTTON)

        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.click_backspace()
        keybd.input_str(username)
        time.sleep(1)
        #清除QQ登陆账号信息
        
        logging.info("Step1: start qq and login 4")
        keybd.click_tab()
        time.sleep(2)
            
        keybd.input_str(password)
        time.sleep(2)  

        logging.info("Step1: start qq and login 5")    
        keybd.click_enter()
        time.sleep(5)
        logging.info("Step1: start qq and login 6")
        #time.sleep(20)
        #click_pic_in_window(hlogin,QQZXH)
        time.sleep(20)
        mouse.move(1145,42)#QQ最小化
        mouse.click(mouse.LEFT_BUTTON)
        logging.info("Step1: start qq and login 7") 
        time.sleep(15)
        logging.info("Sleep time over!")
        
    except Exception:
        err_msg = u'logging qq error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg
        logging.info("Step1: try it again.")
        
def start_lol():
    try:
        cwd = os.getcwd()
        os.chdir(LOL_PATH1.encode('gbk'))
        os.popen('GameCheck.exe')
        os.chdir(cwd)
    except:
        raise Exception,'Can not find GameCheck.exe'
    
def login_game():
    
    try:
        logging.info("Step1: start game and login,please waiting.")
        start_lol()
        hlogin = get_window_handle(None,u'英雄联盟登录程序')
        set_window_top(hlogin,(0,0))
        logging.info("Step1: start game and login 1")
        #bmp_jryx = Image.open(JINRYX)
        #coordinate = find_bmp_in_window(hlogin,bmp_jryx)
            
        #if not coordinate:
        #    error_msg = u'Can not find "enter the game" button, please check.\
        #        You can reload the "enter the game" button bmp.'
        #    raise Exception,error_msg

        logging.info("Step1: start game and login 2")
        time.sleep(5)
        mouse.move(1010,525)#切换至快速登录
        mouse.click(mouse.LEFT_BUTTON)
        #click_pic_in_window(hlogin,QHZKSDL)
        logging.info("Step1: start game and login 3")
        time.sleep(5)
        #click_pic_in_window(hlogin,KSDLQD)
        mouse.move(1000,480)#快速登录确定
        mouse.click(mouse.LEFT_BUTTON)
        logging.info("Step1: start game and login 5")
        time.sleep(5)
       
    except Exception:
        err_msg = u'logging game error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg

def server_choise(serverid):
    
    try:
        logging.info("Step2: choice server")
        #hlogin = get_window_handle(None,u'英雄联盟登录程序')
        #click_pic_in_window(hlogin,FUWQLB)
        mouse.move(1190,700)#服务器列表
        mouse.click(mouse.LEFT_BUTTON)
        time.sleep(5)
        logging.info("Step1: start game and login 6")
        if serverid == 1:
            #click_pic_in_window(hlogin,AIONY_U,10,errflg=False)
            mouse.move(500,425)#进电信服务器
            mouse.click(mouse.LEFT_BUTTON)
            logging.info("Step1: start game and login 7")
        if serverid == 2:
            #click_pic_in_window(hlogin,NIUQSL_U,10,errflg=False)
            mouse.move(240,555)#进联通服务器
            mouse.click(mouse.LEFT_BUTTON)
            logging.info("Step1: start game and login 8")

        #click_pic_in_window(hlogin,QUERXZ)
        time.sleep(5)
        mouse.move(950,700)#确认选择
        mouse.click(mouse.LEFT_BUTTON)
        logging.info("Step1: start game and login 9")
        
    except Exception:
        err_msg = u'server choise error, error message: %s'%(traceback.format_exc()[34:])
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
    
    except Exception:
        err_msg = u'new player error, error message: %s'%(traceback.format_exc()[34:])
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

        # 关闭“！”（查看游戏状态）的弹出信息
        click_pic_in_window(hpvp,T_GUANB,0,errflg=False)
        
        # 点击“Play”
        click_pic_in_window(hpvp,PLAY)
        
        # 建房
        click_pic_in_window(hpvp,RENJDZ,0,errflg=False)
        click_pic_in_window(hpvp,JINDDZ,0,errflg=False)
        click_pic_in_window(hpvp,ZHAOHSXG,0,errflg=False)
        click_pic_in_window(hpvp,JIAND,0,errflg=False)
        #mouse.move(1145,42)#QQ最小化
        #mouse.click(mouse.LEFT_BUTTON)
        #logging.info("Step1: start qq and login 7") 
        #time.sleep(15)
        
        # 点击“系统匹配队友”
        click_pic_in_window(hpvp,XITPPDY)
        
        # 点击“现在开始”
        click_pic_in_window(hpvp,XIANZKS,120)
    
        # 点击“随机选择”
        click_pic_in_window(hpvp,SUIJXZ)
    
        # 点击“确定”
        click_pic_in_window(hpvp,QUED)
    
        # 判断游戏是否开始，没有等待重新建立游戏，等待时长10分钟
        starttime = time.time()
        bmp_xzks = Image.open(XIANZKS)
        while not win32gui.FindWindow('RiotWindowClass',u'League of Legends (TM) Client'):
            # 使用在屏幕上寻找“现在开始”，而不是窗口上寻找，主要是窗口在启动中同时被设置为
            # 顶层时，会导致窗口分辨率改变（lol bug）
            if find_bmp_in_screen(bmp_xzks, 0):
    
                # 点击“现在开始”
                click_pic_in_window(hpvp,XIANZKS,120)
    
                # 点击“随机选择”
                click_pic_in_window(hpvp,SUIJXZ)
    
                # 点击“确定”
                click_pic_in_window(hpvp,QUED)
            t = time.time() - starttime
            if t > 600:
                err_msg = 'cannot load a game in timeout 10 minutes'
                raise Exception,err_msg
      
    except Exception:
        err_msg = u'load game error, error message: %s'%(traceback.format_exc()[34:])
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
                elif t > 3600:
                    err_msg = 'the time of playing game out of 1 hour'
                    raise Exception,err_msg
                else:
                    random_click()
                    
                    # 点击“继续游戏”按钮所在的区域
                    box = (600,500,770,590)#(min_x,min_y,max_x,max_y)
                    ystep = int((box[3]-box[1])/10)
                    for i in range(10):
                        y = box[1]+i*ystep
                        mouse.move(680, y)
                        mouse.click(mouse.LEFT_BUTTON)
                    t = time.time() - t1
    
        
            
    except Exception:
        err_msg = u'play game error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg
    
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
        
    except Exception:
        err_msg = u'again game error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg

def random_click():
    
    try:
        
        key_list = ['q','w','e','r']
        for i in range(100):
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
        
    except Exception:
        err_msg = u'random click error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg
  
def clean():
    os.system('taskkill /f /im LolClient.exe')
    os.system('taskkill /f /im Client.exe') 
    os.system('taskkill /f /im "League of Legends.exe"')
    os.system('taskkill /f /im "lol.launcher_tencent.exe"')
    os.system('taskkill /f /im BsSndRpt.exe')
    os.system('taskkill /f /im #bugreport.exe')
    logging.info("Clean LOL task over")
    os.system('taskkill /f /im TXPlatform.exe')
    os.system('taskkill /f /im QQ.exe')
    os.system('taskkill /f /im QQApp.exe')
    logging.info("Clean QQ task over")
      
def play_lol(username,password,serverid):
    
    try:
        login_qq(username,password)
        login_game()
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
    
if __name__ == '__main__':
    try:
        username = '2768180191'
        password = 'volans'
        print play_lol(username,password,1)
        
    except Exception,e:
        print traceback.format_exc()
    finally:
        raw_input()
        
