# -*- coding:utf-8 -*-
'''
部署时需要修改日志和配置文件绝对路径

'''

import paramiko
import ConfigParser
import datetime
import os
import logging

dtoday=datetime.date.today() #今日日期

#输出日志定义,绝对路径
logfilename="/FS1/share/sftplog/log/sftplog_"+dtoday.strftime('%Y-%m-%d')+".log"
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=logfilename,
                filemode='a')


private_key = paramiko.RSAKey.from_private_key_file('/FS1/share/.ssh/id_rsa')
listfilename=[]  #远程目录要备份文件名

def sftp_exec_command(host,user,command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#       ssh_client.connect(host, 22, user, password)
        ssh_client.connect(host, 22, user,pkey=private_key)
        logging.info('Beginning to exec')
        logging.info(command)
        std_in, std_out, std_err = ssh_client.exec_command(command)
        for line in std_out:
            print line.strip("\n")
        ssh_client.close()
        logging.info('exec success')
    except Exception, e:
        print e

def sftp_get_filelist(host,user,src_filepath,command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#       ssh_client.connect(host, 22, user, password)
        ssh_client.connect(host, 22, user,pkey=private_key)
        logging.info('Beginning to exec')
        logging.info(command)
        std_in, std_out, std_err = ssh_client.exec_command(command)
        for line in std_out:
            filename = line.strip()
            listfilename.append(filename)
        ssh_client.close()
        if listfilename:
            logging.info('get filelist')
        else:
            logging.info('not get filelist')

    except Exception, e:
        print e

def sftp_down_file(host,user,server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user,pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(t)
        server_path = str(server_path)
        local_path = str(local_path)
        logging.info('Beginning to download file')
        logging.info(server_path)
        logging.info(local_path)
        sftp.get(server_path, local_path)
        logging.info('Download file success')
        t.close()
    except Exception, e:
        print e

def sftp_upload_file(host,user,server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user,pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception, e:
        print e

def sftp_get_log_file(hostpath):
    try:
        logging.info(hostpath);
        config = ConfigParser.ConfigParser()
        #配置文件写绝对路径
        with open("/FS1/share/sftplog/sftplog.cfg", "rw") as cfgfile:
            config.readfp(cfgfile)
            host = config.get(hostpath, "host")
            src_filepath = config.get(hostpath, "src_file_path")
            des_filepath = config.get(hostpath, "des_file_path")
            user = config.get(hostpath, "user")
            day =int(config.get(hostpath, "day"))
            match =int(config.get(hostpath, "match"))
            delefile=int(config.get(hostpath, "delefile"))
        #根据保留日志时间计算备份日期
        # match 配置日期 1：yyyy-mm-dd 2: yyyymmdd 3: yyyymm
        dyesterday = (dtoday - datetime.timedelta(days=day))  # 昨日日期
        if (match==1):
            stryesterday = dyesterday.strftime('%Y-%m-%d')
        elif (match==2) :
            stryesterday = dyesterday.strftime('%Y%m%d')
        elif (match==3) :
            stryesterday = dyesterday.strftime('%Y%m')
        #拼接今日要下载的文件
        if (hostpath=="132.77.134.14_vipsyncFile"):
            strmonthday= dyesterday.strftime('%Y%m%d')
            src_filepath=src_filepath+strmonthday
            exec_command='cd '+src_filepath+'\n ls *'+stryesterday+'*'
        else:
            exec_command='cd '+src_filepath+'\n ls *'+stryesterday+'*'
        #远程执行命令取得下载的文件名
        sftp_get_filelist(host,user,src_filepath,exec_command)
        #循环下载文件
        for list_file_name in listfilename:
            src=os.path.join(src_filepath, list_file_name)
            des=os.path.join(des_filepath, list_file_name)
            sftp_down_file(host,user,src, des)
            #下载完成删除远程文件
            if (delefile==2 ):
               sftp_delete_command="rm "+src
               sftp_exec_command(host,user,sftp_delete_command)
        global listfilename
        listfilename = []  # 初始化为空
    except Exception, e:
        print e
if __name__ == '__main__':

    logging.info("begin sftp log file ")
    sftp_get_log_file("132.77.134.14_smgsync_yy")
    sftp_get_log_file("132.77.134.14_quduanjuall")
    sftp_get_log_file("132.77.134.14_PAYLOGREMIND")
    sftp_get_log_file("132.77.134.14_OweDataSync")
    sftp_get_log_file("132.77.134.14_usersync")
    sftp_get_log_file("132.77.134.14_usersync_log")
    sftp_get_log_file("132.77.134.14_ftpsync")
    sftp_get_log_file("132.77.134.14_ftpsync_log")
    sftp_get_log_file("132.77.134.14_callout")
    sftp_get_log_file("132.77.134.14_callout_log")
    sftp_get_log_file("132.77.134.14_care")
    sftp_get_log_file("132.77.134.14_care_log")
    sftp_get_log_file("132.77.134.14_vipsyncFile")
    sftp_get_log_file("132.77.134.14_busiType")
    sftp_get_log_file("132.77.134.14_Disorder")
    sftp_get_log_file("132.77.134.14_ftpcrm")

    sftp_get_log_file("132.77.134.46_wtcdomain")
    sftp_get_log_file("132.77.134.46_audioupload")
    sftp_get_log_file("132.77.134.46_message")
    sftp_get_log_file("132.77.134.46_predictionDialer")
    sftp_get_log_file("132.77.134.46_vip_ivr")
    sftp_get_log_file("132.77.134.46_WirelessModem_ivr")
    sftp_get_log_file("132.77.134.46_mms")
    sftp_get_log_file("132.77.134.46_oweDialer")
    sftp_get_log_file("132.77.134.46_phonetrans1")
    sftp_get_log_file("132.77.134.46_phonetrans2")
    sftp_get_log_file("132.77.134.46_smg_2012")
    sftp_get_log_file("132.77.134.46_mdatasync")
    sftp_get_log_file("132.77.134.46_ats")

##   sftp_get_log_file("132.77.134.46_csputbd_date")
##   sftp_get_log_file("132.77.134.46_csputbd_utf8data")
##   sftp_get_log_file("132.77.134.46_uploadSheet")


    sftp_get_log_file("132.77.134.48_wtcdomain")
    sftp_get_log_file("132.77.134.48_vip_ivr")
    sftp_get_log_file("132.77.134.48_mms")
    sftp_get_log_file("132.77.134.48_phonetrans1")
    sftp_get_log_file("132.77.134.48_phonetrans2")
    sftp_get_log_file("132.77.134.48_smg_2012")

    sftp_get_log_file("132.81.77.18_icddir")
    sftp_get_log_file("132.81.77.17_icddir")
    sftp_get_log_file("132.80.180.244_icddir")
    sftp_get_log_file("132.80.180.245_icddir")

    logging.info("end sftp log file ")
