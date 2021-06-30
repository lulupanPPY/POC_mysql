import base64
import os
import uuid
import paramiko
from scp import SCPClient
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import re
import numpy as np
LIST_OF_CHAR = [',','\'','\"','null']


def merge_files(path, dest,encoding='utf8'):
    files = os.listdir(path)
    with open(dest, 'w',encoding=encoding) as w:
        for f in files:
            with open(path + f, 'r',encoding=encoding) as sql:
                for line in sql:
                    print (line)
                    w.write(line + '\n')
            sql.close()
        w.close()

def gen_uuid():
    return uuid.uuid4()

def get_base64(str):
    print(str)
    str = bytes(str,'utf-8')
    encoded = base64.b64encode(str)
    return encoded

def scp(lpath,rpath,usr,pswd,host,port=22):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, usr, pswd)
    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
    try:
        scpclient.put(lpath, rpath)
    except FileNotFoundError as e:
        print(e)
        print("系统找不到指定文件" + lpath)
    else:
        print("文件上传成功")
    ssh_client.close()

def get_mysql_connection(usr,pswd,host,port,db):
    try:
        cnx = mysql.connector.connect(user=usr, password=pswd,
                                      host=host,port=port,
                                      database=db)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print ('connected to %s as %s'%(host,usr))
        return cnx
    return None

def execute_mysql(stmt):
    pass

def select_mysql_as_df(stmt,conn):
    cursor = conn.cursor()
    cursor.execute(stmt)
    rs = pd.DataFrame(cursor,columns=cursor.column_names)
    cursor.close()
    return rs

def insert_mysql(stmt,stmt_data,conn):
    cursor = conn.cursor()
    cursor.execute(stmt,stmt_data)

def commit_mysql (conn):
    conn.commit()


def is_variable(str):
    for s in LIST_OF_CHAR:
        if str.find(s)>=0:
            return True
    return False

def var_str_pattern(n):
    str = []
    for i in range(n):
        str.append('%s')
    return ','.join(str)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

if __name__ == '__main__':
    print (get_base64('db_ccc_accountin'))