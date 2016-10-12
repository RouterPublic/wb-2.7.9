# -*- coding:utf-8 -*-

import os
import rpyc
import time
import config
import logging
import thread
import traceback
import win32com.client
from threading import Thread

lock = thread.allocate_lock()## thread lock

all_result = {}
page_white_time_error_flag = False
     
def remote_run(ip,urllist,save_dir):
    
    global page_white_time_error_flag
    
    if urllist is None:
        urllist = ['http://www.qq.com/',"http://www.163.com/",
                   "http://www.baidu.com","http://www.renren.com/"]
    
    # init result_dic
    result_dic = {}
    for url in urllist:
        result_dic[url] = []
    
    # save path
    save_path = save_dir+'/'+ '_'.join(ip.split('.'))+'.txt'
    
    # connect to remote pc
    try:
        client = rpyc.classic.connect(ip)
    except Exception:
        page_white_time_error_flag = True
        raise Exception("Can't connect to %s!"%ip)
    
    # upload the files
    try:
        rpyc.classic.upload(client, './__init__.py', './plugin/__init__.py')
        if not client.modules.os.path.exists('./plugin/page_white_time/'):
            client.modules.os.mkdir('./plugin/page_white_time/')
        rpyc.classic.upload(client, './__init__.py', './plugin/page_white_time/__init__.py')
        rpyc.classic.upload(client, './r_page_white_time.py', './plugin/page_white_time/r_page_white_time.py')
        
    except Exception:
        page_white_time_error_flag = True
        raise Exception("Upload the files failed!")
        
    logging.info("%s finish upload plugin!"%ip)
    
    # run remote function 
    logging.info('Running, please wait ...')
    try:
        client.modules["plugin.page_white_time.r_page_white_time"]
        client.modules.imp.reload(client.modules["plugin.page_white_time.r_page_white_time"])
        run = client.modules["plugin.page_white_time.r_page_white_time"].run
        for i in range(config.test_times):
            logging.info('%s run %s times'%(ip,i+1))  
            for url in urllist:
                white_time = run(url=url,timeout=10)
                result_dic[url].append(white_time)
        
        # write the result 
            txt_result = open(save_path,"w")    
            for _url in urllist:
                write_txt = _url.ljust(40)+'  '
                total_time = 0
                for ttime in result_dic[_url]:
                    wtime = str(round(ttime,2)).ljust(8)
                    total_time = total_time + ttime
                    write_txt = write_txt + wtime
                avg_time = total_time/len(result_dic[_url])
                write_txt =  write_txt + "total:"+ str(round(total_time,2)).ljust(8) +\
                            "avg:" + str(round(avg_time,2)).ljust(8) + '\n' 
                txt_result.write(write_txt)         
                
            txt_result.close()
            
        global all_result
        lock.acquire()
        all_result[ip]=result_dic
        lock.release()
    except Exception:
        page_white_time_error_flag = True
        raise Exception("Run r_page_white_time.py failed! ")

def write_result_to_excel(allResult,save_dir):
    
    ip_list = sorted(allResult.keys())
    ip_num = len(ip_list)
        
    url_num = len(config.url_list)
    test_times = config.test_times
  
    excelApp = win32com.client.Dispatch('Excel.Application')
    excelApp.DisplayAlerts = False
#     print excelApp.xlWorkbookNormal
    try:
        workBook = excelApp.Workbooks.Add()
        workBook.Worksheets.Add(None,None,ip_num+1)
        
        # init 'AllResult' Sheet
        allSheet = workBook.Worksheets(1)
        allSheet.name = 'AllResult'
        if ip_num != 0:
            allSheet.Range(allSheet.Cells(1,2),allSheet.Cells(1,ip_num+1)).Merge()
            allSheet.Range(allSheet.Cells(1,ip_num+2),allSheet.Cells(1,ip_num+ip_num+1)).Merge()
            allSheet.Cells(1,1).Value = ' '
            allSheet.Cells(1,2).Value = 'Total'
            allSheet.Cells(1,ip_num+2).Value = 'Avg'
        else:
            allSheet.Cells(1,1).Value = 'No result!!!'
        
        #--------- write result to each ip ----------------------------------------
        i = 1
        for ip in ip_list:
            i += 1
            nowSheet = workBook.Worksheets(i) # select sheet
            nowSheet.name = ip
             
            # first column
            for test_i in range(test_times):
                nowSheet.Cells(test_i+2, 1).Value = test_i + 1 
            nowSheet.Cells(test_i+3, 1).Value = 'Total'
            nowSheet.Cells(test_i+4, 1).Value = 'Avg'
              
            # each url column
            for url_i in range(url_num):
                url = config.url_list[url_i]
                nowSheet.Cells(1, url_i+2).Value = url
                totalTime = 0
                for test_i in range(test_times):
                    whiteTime = allResult[ip][url][test_i]
                    totalTime = totalTime + whiteTime
                    nowSheet.Cells(test_i+2, url_i+2).Value = whiteTime
                  
                avgTime = totalTime/test_times
                  
                # write totalTime and avgTime to each ip sheet
                nowSheet.Cells(test_i+3, url_i+2).Value = round(totalTime,2)
                nowSheet.Cells(test_i+4, url_i+2).Value = round(avgTime,2)
              
        #--------- Write to AllResult' sheet --------------------------------------
                # 1.write 'AllResult' sheet's first column 
                allSheet.Cells(url_i+3,1).Value = config.url_list[url_i]
                allSheet.Cells(url_i+3,1).Value = config.url_list[url_i]
                  
                # 2.write totalTime and avgTime to 'AllResult' Sheet
                allSheet.Cells(url_i+3,i).Value = round(totalTime,2)
                allSheet.Cells(url_i+3,ip_num+i).Value = round(avgTime,2)
                 
            # 3.write 'AllResult' sheet's second row
            allSheet.Cells(2,i).Value = ip
            allSheet.Cells(2,ip_num+i).Value = ip
               
        #--------- format each ip sheet -------------------------------------------
            nRowCount = nowSheet.usedrange.rows.count    
            nColCount = nowSheet.usedrange.columns.count
            nowSheet.Cells.Font.Name='Times New Roman'
            nowSheet.Range(nowSheet.Cells(1,1),nowSheet.Cells(nRowCount,nColCount)).Borders.LineStyle=1 
            nowSheet.Columns.Columnwidth = 15
            nowSheet.Columns(1).Columnwidth = 8
            nowSheet.Cells(1,nColCount+1).Value = ' ' 
            nowSheet.Range(nowSheet.Cells(1,1),nowSheet.Cells(1,nColCount)).Interior.Color = 0x50d092
             
        #--------- formate 'AllResult' sheet --------------------------------------
        aRowCount = allSheet.usedrange.rows.count    
        aColCount = allSheet.usedrange.columns.count
        allSheet.Cells.Font.Name='Times New Roman'
        allSheet.Range(allSheet.Cells(1,1),allSheet.Cells(aRowCount,aColCount)).Borders.LineStyle=1 
        allSheet.Columns.AutoFit()
        allSheet.Columns(1).Columnwidth = 15
        allSheet.Range(allSheet.Cells(1,1),allSheet.Cells(1,aColCount)).Interior.Color = 0x50d092
        
        # save and close
        save_path = os.path.abspath(save_dir) + os.sep + 'allResult'
        workBook.SaveAs(save_path)
        workBook.Close(SaveChanges=0)
        del workBook
    except Exception,e:
        raise Exception('Write result to excel failed! Error message: %s'%e)
    finally:
        excelApp.Quit()

def main():
    
    # make dir
    cur_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())
    save_dir = './result/'+cur_time
    is_exists = os.path.exists(save_dir)
    if not is_exists:
        os.mkdir(save_dir)
    
    logging.getLogger().setLevel(logging.INFO)
    thread_page = {}
    ip_list = config.ip_list
    url_list = config.url_list
 
    for ip in ip_list:
        thread_page[ip] = Thread(target = remote_run, args = (ip,url_list,save_dir))
        thread_page[ip].start()
            
    for ip in ip_list:
        thread_page[ip].join()
    
    global all_result
    
    logging.info('Write result...')
    write_result_to_excel(all_result,save_dir)
    
if __name__ == '__main__':
    try:
#         save_path = '.\\'
#         ar = {'172.168.8.81': {'http://www.163.com/': [0.485, 0.434, 0.515], 
#                                'http://www.qq.com/': [1.108, 0.442, 1.121]}, 
#               '172.168.8.83': {'http://www.163.com/': [5.985, 6.687, 5.656], 
#                                'http://www.qq.com/': [1.656, 2.078, 1.514]},}
#         for i in range(100):
#             print i
#             write_result_to_excel(ar,save_path)
        main()
    except Exception,e:
        print traceback.format_exc()
        raw_input('Input anything to quit ...')
     
    if page_white_time_error_flag:
        raw_input('Input anything to quit ...')
