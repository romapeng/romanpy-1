#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 10:51:57 2017

@author: roman

代码：(使用os.walk) walk递归地对目录及子目录处理，每次返回的三项分别为：当前递归的目录，当前递归的目录下的所有子目录，当前递归的目录下的所有文件
"""

import os,time
import pymysql

#导入csv文件目录
import_dir="/Users/roman/Downloads/test"
#import_dir="/Users/roman/stock/csv"
#输出目录
out_dir = "/Users/roman/stock/out/"
#输出日志文件
outfile_name = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time())) +"_log.txt"
#导入的文件后缀
wildcard = ".csv .*"

#测试库  
fixsql_test= "INSERT INTO `db_stock`.`stk_day_tb1` (`stkno`,`close`,`high`,`low`,\
`p_change`,`open`,`pre_close`,`volume`,`date`,`date_week`,`atr21`,`atr14`,`key`) VALUES("
#正式库
fixsql_formal= "INSERT INTO `db_stock`.`stock_day_raw` (`stkno`,`close`,`high`,`low`,\
`p_change`,`open`,`pre_close`,`volume`,`date`,`date_week`,`atr21`,`atr14`,`key`) VALUES("
#是否正式版，正式版将入正式库（1：正式 0：测试）
isrelease = 0  
fixsql = ""
        
"""
读指定目录下的stock导入文件（csv格式），并写入数据库mysql。
dir: walk目录
outfile: 日志
wildcard: 需导入的文件后缀
recursion: 是否递归子目录
"""
def WalkCSVFilesToMysql(dir,outfile,wildcard,recursion):
    
    exts = wildcard.split(" ")

    for root, subdirs, files in os.walk(dir):
        outfile.write(root + "\n")
        for name in files:
            #过虑隐藏文件
            if name.startswith("."): continue           
            
            for ext in exts:
                if (name.endswith(ext) or ext == ".*"):
                    outfile.write("开始导入文件："+name + "\n")
                    icount = 0
                    try:
                        
                        conn = pymysql.connect(  
                                host='localhost',  
                                port=3306,  
                                user='myroman',  
                                passwd='Db_Finance',  
                                database='db_stock')  
                        #conn.set_charset('utf8')  
                        cur=conn.cursor() 
                        
                        fname = root+"/"+name
                        with open(fname,'r') as f:
                            #从第二行开始遍历所有行
                            for line in f.readlines()[1:]:
                                if line.strip():
                                    line = name +"_"+line
                                    valsql = ""
                                    for valitem in line.strip().split(","):
                                       valsql += "'" + valitem + "'," 
                                    valsql = valsql[:-1]
                                    insertsql =fixsql + valsql + ")"
                                    cur.execute(insertsql)
                                    icount += 1
                                    #outfile.write("导入："+str(icount) + "行数据 --- OK\n")
                                    
                               
                                    """
                                    vals = line.split(",")
                                    keys = ['date_ind','close', 'high','low','p_change','open','pre_close',\
                                     'volume','date','date_week','atr21','atr14','key']
                                    stockvalue = zip(keys.values(),vals.values())
                                    stockvalue[0]+":"stockvalue[1]
                                    """
                        
                        conn.commit()
                        outfile.write("导入："+str(icount) + "行数据 --- OK\n")
                        
                    except pymysql.Error as e:
                        conn.rollback()
                        outfile.write("错误警告：第"+str(icount) + "行出错！%d: %s\n" % (e.args[0], e.args[1]))
                    finally:
                        cur.close()  
                        conn.close()
                    break
            
        #若不递归子目录        
        if(not recursion):
            break
        

if __name__ == "__main__":
    
    if isrelease: 
        fixsql = fixsql_formal
        outfile.write("将导入正式库！！！\n")
    else:
        fixsql = fixsql_test
        outfile.write("将导入测试库\n")
                                                                      
    with open(out_dir+outfile_name,"a") as outfile:
         WalkCSVFilesToMysql(import_dir,outfile,wildcard, 1)
         outfile.write("导入完毕！！！\n")