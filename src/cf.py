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

CF_PATH    = u"X:\网络游戏\穿越火线\GameCheck.exe"
CF_BMP_DIR = "./bmp/cf/"
DENGLYX  = CF_BMP_DIR + "denglyx.bmp"       #登录游戏
JINRYX   = CF_BMP_DIR + "jinryx.bmp"        #进入游戏
QQZH     = CF_BMP_DIR + "qqzh.bmp"          #QQ账号输入框  
QQMM     = CF_BMP_DIR + "qqmm.bmp"          #QQ密码输入框
DIANX    = CF_BMP_DIR + "dianx.bmp"         #电信
WANGT    = CF_BMP_DIR + "wangt.bmp"         #网通
SIC2Q    = CF_BMP_DIR + "sic2q.bmp"         #四川2区
BEIJ1Q   = CF_BMP_DIR + "beij1q.bmp"        #北京1区
BEIFDQ   = CF_BMP_DIR + "beifdq.bmp"        #北方大区
NICBOX   = CF_BMP_DIR + "nicbox.bmp"        #昵称输入框
SHURNC   = CF_BMP_DIR + "shurnc.bmp"        #输入昵称
NICQD    = CF_BMP_DIR + "nicqd.bmp"         #昵称确定
QUERNC   = CF_BMP_DIR + "quernc.bmp"        #确认昵称
PLAY     = CF_BMP_DIR + "play.bmp"          #play按钮
JUESQD   = CF_BMP_DIR + "juesqd.bmp"        #角色确定按钮
GOUMJS   = CF_BMP_DIR + "goumjs.bmp"        #角色购买按钮
SHENGHYB = CF_BMP_DIR + "shenghyb.bmp"      #生化佣兵模式
LIJKS    = CF_BMP_DIR + "lijks.bmp"         #立即开始
SIWT     = CF_BMP_DIR + "siwt.bmp"          #斯沃特图标
JIARYX   = CF_BMP_DIR + "jiaryx.bmp"        #加入游戏
ALTDAK   = CF_BMP_DIR + "altdak.bmp"        #“alt打开”标志，用于判断游戏是否开始
QUER     = CF_BMP_DIR + "quer.bmp"          #游戏开始后确认
JIESQD   = CF_BMP_DIR + "jiesqd.bmp"        #游戏结束确定
    
def login_game(username,password):
    
    try:
        logging.info("Step1: start game and login")
        os.startfile(CF_PATH)
        hlogin = get_window_handle(None,u'穿越火线登录程序')
        set_window_top(hlogin,(0,0))
        bmp_jryx = Image.open(DENGLYX)
        coordinate = find_bmp_in_window(hlogin,bmp_jryx)
        
        if not coordinate:
            error_msg = u'Can not find "enter the game" button, please check.\
                You can reload the "enter the game" button bmp.'
            raise Exception,error_msg

        click_pic_in_window(hlogin,QQZH)
        keybd.input_str(username)
        time.sleep(0.5)
        
        click_pic_in_window(hlogin,QQMM)
        keybd.input_str(password)
        time.sleep(0.5)  
            
        keybd.click_enter()
        
    except Exception:
        err_msg = 'logging game error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg

def server_choise(serverid):
    
    try:
        logging.info("Step2: choice server")
        hlogin = get_window_handle(None,u'穿越火线登录程序')
        bmp_jryx = Image.open(JINRYX)
        find_bmp_in_window(hlogin,bmp_jryx)
        if serverid == 1:
            click_pic_in_window(hlogin,DIANX,0,errflg=False)
            click_pic_in_window(hlogin,SIC2Q,0,errflg=False)
        elif serverid == 2:
            click_pic_in_window(hlogin,WANGT,0,errflg=False)
            click_pic_in_window(hlogin,BEIFDQ,0,errflg=False)

        click_pic_in_window(hlogin,JINRYX)
        
    except Exception:
        err_msg = 'server choise error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg
    
def new_player():
    
    try:
        logging.info("Build a new player.")
        hpvp = get_window_handle(None,u'穿越火线')

        mouse.move(0,0)
        name = 'T'
        for i in xrange(11):
            name = name + str(random.randint(0,9)) 
        keybd.input_str(name)
        
        # 点击昵称确定
        click_pic_in_screen(QUERNC,mode='pil')
        click_pic_in_screen(NICQD,mode='pil')
    
    except Exception:
        err_msg = 'new player error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg
    
def load_game():
    try:

        logging.info("Step3: enter a room and start play.")
        hpvp = get_window_handle(None,u'穿越火线')
        
        # 检查是否需要新建昵称
        bmp_shurnc = Image.open(SHURNC)
        coordinate = find_bmp_in_screen(bmp=bmp_shurnc, timeout=30, mode='pil')
        if coordinate:
            new_player()

        # 点击play，如果发现没有角色，购买角色
        click_pic_in_screen(PLAY,mode='pil')
        bmp_juesqd = Image.open(JUESQD)
        crd_juesqd = find_bmp_in_screen(bmp=bmp_juesqd, timeout=10, mode='pil')
        if crd_juesqd:
            # 等待1秒（不等待，下面语句无法执行，原因未知）
            time.sleep(1)
            
            click_pic_in_screen(JUESQD,mode='pil')
            click_pic_in_screen(SIWT,mode='pil')
            click_pic_in_screen(GOUMJS,mode='pil')
            

        # 选择模式，进入游戏
        click_pic_in_screen(SHENGHYB,mode='pil')
        click_pic_in_screen(LIJKS,mode='pil')

        time.sleep(5)
        click_pic_in_screen(JIARYX,mode='pil')
        
    except Exception:
        err_msg = 'load game error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg

def play_game():
    try:
        t1 = time.time()
        t = 0
        bmp_altdak = Image.open(ALTDAK)
        bmp_jiesqd = Image.open(JIESQD)
        coordinate = find_bmp_in_screen(bmp=bmp_altdak, timeout=10, mode='pil')
        if coordinate:
            click_pic_in_screen(QUER,timeout=180,mode='pil')
            while True:
                time.sleep(10)
                if find_bmp_in_screen(bmp=bmp_jiesqd, mode='pil'):
                    break
                elif t > 3600:
                    err_msg = 'the time of playing game out of 1 hour'
                    raise Exception,err_msg
                else:
                    t = time.time() - t1
        else:
            err_msg = "can't enter the game room"
            raise Exception,err_msg
        
    except Exception:
        err_msg = 'play game error, error message: %s'%(traceback.format_exc()[34:])
        raise Exception,err_msg

def clean():
    os.system('taskkill /f /im CFStarter.exe')
    os.system('taskkill /f /im Client.exe') 
    os.system('taskkill /f /im crossfire.exe')
    os.system('taskkill /f /im CrossProxy.exe')
      
def play_cf(username,password,serverid):
    
    try:
        login_game(username,password)
        server_choise(serverid)
        load_game()
        play_game()
            
    except Exception,e:
        err_msg = '%s'%e
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
        logging.getLogger().setLevel(logging.INFO)
        username = '2768180191'
        password = 'volans'

        print play_cf(username,password,1)
        
    except Exception,e:
        print traceback.format_exc()
    finally:
        raw_input()
        
