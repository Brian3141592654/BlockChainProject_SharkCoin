#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
import hashlib
import threading
from signature_rsa import *
from connect import *
from datetime import datetime

miner_stop = 0

Mydb = connectPool().connection()
Mycursor = Mydb.cursor()

def set_difficulty():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT difficulty FROM `diff`"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    diff = result[0]

    mycursor.close()
    mydb.close()
    
    return diff

difficulty = set_difficulty()

def set_broadcast():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT pubkey, transaction, signature FROM `broadcast`"
    mycursor.execute(sql)
    result = mycursor.fetchone()

    if result[0]==None:
        return " , , "

    bc = result[0] + ',' + result[1] + ',' +result[2]

    mycursor.close()
    mydb.close()
    
    return bc

broadcast = 'broadcast,'+set_broadcast()
# ---------------------------------------------------------------

def firstblock():  # check if there are not any inital block
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT MAX(height) as maxi from block"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    str1 = result[0][0]
    if str1 is None:
        return True
    else:
        return False
    

# --------------------------------------------------------------

# ---------------------------
def settopblock():  # set the top block
    if firstblock():

        sql = "INSERT INTO block (height) VALUES (%s)"
        v1 = (1,)
        Mycursor.execute(sql, v1)  # 111

        t = time.localtime()
        result1 = time.strftime("%Y-%m-%d %H:%M:%S", t)
        block = "block:1"
        block = block+"\ntime:"
        block = block+result1
        block = block+"\ntransaction: first block \n"
        block = block+"proof:"
        sql = "Update  block  set blockdata=%s where height = %s"
        v1 = (block, 1)
        Mycursor.execute(sql, v1)

    else:
        t = time.localtime()
        result1 = time.strftime("%Y-%m-%d %H:%M:%S", t)
        mydb = connect()
        mycursor = mydb.cursor()
        sql = "SELECT MAX(height) as maxi from block"  # block number
        mycursor.execute(sql)
        result = mycursor.fetchall()
        topblock = result[0][0]

        topblock = topblock+1  # new block id

        sql = "SELECT hash from block where height=%s"  # prehash
        v1 = (topblock-1,)
        mycursor.execute(sql, v1)
        result2 = mycursor.fetchall()
        prehash = result2[0][0]

        if prehash == "":
            return
       
        sql = "SELECT transaction FROM `broadcast`"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        transaction = result[0]

        block = "block:"+str(topblock)
        block = block+"\ntime:"
        block = block+result1
        block = block+"\nprehash:"
        block = block+prehash
        block = block+"\ntransaction:\n"
        block = block+transaction
        block = block+"proof:"

        sql = "INSERT INTO block (height,blockdata) VALUES (%s,%s)"
        v1 = (topblock, block)
        Mycursor.execute(sql, v1)

        # 調整難度
        # difficulty_adjust()

        time.sleep(2)

def topblocklist():  # return topblock list that miner need
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT MAX(height) as maxi from block"  # block number
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for x in result:
        topblock = x[0]
    sql = "SELECT blockdata from block where height=%s"
    v1 = (topblock,)
    mycursor.execute(sql, v1)
    result = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    block = result[0][0]
    return block


def checksucceedhash(proof):  # check the miner if cheat
    data = topblocklist()+str(proof)  # use database blockdata to prove
    data = hashlib.sha256(data.encode('utf-8')).hexdigest()

    if data[0:difficulty] == "0" * difficulty:
        return True
    else:
        print(datetime.now())
        print("checksuccessedhash:")
        print(topblocklist())
        print(proof)
        print('difficulty:')
        print(difficulty)

        return False

def completeblock(hashnumber, blockdata, proof):  # complete a block by add hash

    mydb = connect()
    mycursor = mydb.cursor()

    if checksucceedhash(proof) == False:
        return False

    sql = "SELECT MAX(height) as maxi from block"  # block number
    mycursor.execute(sql)
    result = mycursor.fetchall()
    topblock = result[0][0]

    sql = "Update  block  set hash=%s,blockdata=%s where height = %s"
    v1 = (hashnumber, blockdata, topblock)
    Mycursor.execute(sql, v1)

    mycursor.close()
    mydb.close()

    settopblock()  # 112

def difficulty_adjust():
    def block_amount_check():
        mydb = connect()
        cursor = mydb.cursor()

        # 找前十塊
        sql = "SELECT height FROM `block` order by height desc"
        cursor.execute(sql)
        result = cursor.fetchone()
        height = result[0] - 10 

        if height > 0 and height % 10 == 0:
            # 找第前十塊的時間
            sql = "SELECT blockdata FROM `block` where height = %d" % height
            cursor.execute(sql)
            result = cursor.fetchone() 

            cursor.close()
            mydb.close()

            # 從blockdata取出時間
            str = result[0].split('\n') 
            last_time = str[1][5:24] 

            end = datetime.now()
            start = datetime.strptime(last_time,"%Y-%m-%d %H:%M:%S")

            # 取得每塊平均時間
            delta = (end - start).seconds / 10

            # limit about 1 block every 10 minutes
            if delta > 720:
                print(end)
                print(start)
                return 3
            elif delta < 480:
                return 2
            else:
                return 1
        return 1

    try:
        check = block_amount_check() # 1 難度不變 2 增加 3 減少
    except:
        check = 1
        ## print('error')

    if check != 1: # 從資料庫取得難度
        mydb = connect()
        cursor = mydb.cursor()
        sql = "SELECT * FROM `diff`"
        cursor.execute(sql)
        result = cursor.fetchone()

        global difficulty
        difficulty = result[0]

        cursor.close()
        mydb.close()

    temp = difficulty

    if check == 3: # 時間大於設定值，減少難度，最小為5
        if difficulty > 5:
            temp -= 1    
    elif check == 2: # 時間小於設定值，增加難度
        if difficulty < 6:
            temp += 1

    if check != 1: # 更新難度
        if((check != 2 or difficulty != 6) and (check != 3 or difficulty != 5)):
            sql = "UPDATE `diff` SET difficulty = %d " % temp
            Mycursor.execute(sql)

            print(datetime.now())
            print("difficulty:")
            print(temp)

    difficulty = temp

# -------sever
settopblock()  # creat first block

HOST = '192.168.0.109'
PORT = 12121

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(50)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

def NotifyAll(ss):
    global data
    if con.acquire():#獲取鎖
        data = ss
    con.notifyAll()#當前線程放棄對資源的占有，通知所有等待x線程
    con.release()

def clientThreadIn(conn, addr): 
    global data
    global broadcast
    global miner_stop
    while True:
        try:
            indata = conn.recv(1024).decode()#客戶端發過來的消息
            if not indata:
                # conn.close()
                print(str(addr) + ' disconnected')
                return
            if indata == "list": # 傳送block資訊給client
                outdata = topblocklist()
                conn.send(outdata.encode())
            elif indata[:9] == "broadcast":  # 廣播給所有client
                broadcast = indata
                miner_stop = 1
                NotifyAll('miner_stop')
            elif indata == 'req_broadcast': # client請求廣播
                conn.send(broadcast.encode())
            elif indata == 'req_miner': # client請求是否能開始挖礦
                if miner_stop:
                    conn.send('miner_stop'.encode())
                else:
                    conn.send('miner_start'.encode())
            elif indata == 'req_diff': # client請求難度
                conn.send(('diff' + str(difficulty)).encode())
            elif  indata == 'req_initial_diff': # client設定初始難度
                conn.send(('initial_diff' + str(difficulty)).encode())
            elif indata[0:7] == "succeed":  # hash and block add to database
                str2 = indata.split(',')
                print(datetime.now())
                print("proof = "+str2[3])
                if completeblock(str2[1], str2[2], str2[3]) == False: # 停2秒
                    conn.send("miner_fail".encode())
                miner_stop = 0
                                

        except:
            # outdata = topblocklist()
            # conn.send(outdata.encode())
            # conn.close()
            print(datetime.now())
            print(str(addr) + ' disconnected')
            return
            """
                if completeblock(str2[1],str2[2],str2[3])==False:
                    outdata="error"
                    conn.send(outdata.encode())
                else:
                    outdata="ok"
                    conn.send(outdata.encode())
            """

def clientThreadOut(conn):
    global data
    while True:
        if con.acquire():
            con.wait()#堵塞，放棄對資源的占有 等待通知運行後面的代碼
        if data:
            try:
                conn.send(data.encode())
                con.release()
            except:
                con.release()
                return

con = threading.Condition()#條件
data = ''

while True:
    conn, addr = s.accept()
    print(datetime.now())
    print('connected by ' + str(addr))

    threading.Thread(target=clientThreadIn,args=(conn, addr)).start()
    threading.Thread(target=clientThreadOut,args=(conn,)).start()

