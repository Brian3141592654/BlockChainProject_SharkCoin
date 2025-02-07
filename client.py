#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import tkinter.messagebox
import hashlib
import random
import time
import signature_rsa 
import base64
from datetime import datetime
from connect import *
from signature_rsa import *
import threading

HOST = '112.104.189.126'
PORT = 1200

end_flag = 0
stop_flag = 0
diff_flag = 0 
file_flag = 0
miner_stop = 0
success_flag = 0
connect_error_flag = 0

cnt = 0
temp = 0
count = 0
hashnumber = 0
difficulty = 0
success_count = 0
success_proof = 0

pubkey = ""
prikey = ""
account = ""
show_hash = ""
blockdata = ""
pubkey_recv = ""
signature_recv = ""
transaction_recv = ""

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

def produce_trans(s):
    mydb = connect()
    mycursor = mydb.cursor()

    # pubkey經過Hash產生地址
    global pubkey
    tmp = hashlib.sha256(pubkey.encode('utf-8')).hexdigest()
    address = P2PKHToAddress(tmp).decode()

    # 挖礦成功報酬，每100個block獎勵減半
    sql = "SELECT height FROM `block` order by height DESC LIMIT 0,1"
    mycursor.execute(sql)
    result5 = mycursor.fetchone()

    base = 50
    h = result5[0]
    div = pow(2, int(h/100))
    coin = round(base / div)
    if coin < 1:
        coin = 1

    if coin > 1:
        transaction = address + '\nreward '+ str(coin) + ' coins\n'
    else:
        transaction = address + '\nreward '+ str(coin) + ' coin\n'

    ### 產生簽章
    # str to bytes
    global prikey
    prikey_byte = prikey.encode()

    # 可加密私鑰
    prikey_real = decode_prikey(prikey_byte)

    # 產生交易 bytes
    Trans = transaction.encode()

    # 產生簽章
    signature = rsa.sign(Trans, prikey_real, 'SHA-256')
    signature = base64.urlsafe_b64encode(signature) # 編碼，避免無法轉成字串
    signature = signature.decode()                  # 轉成字串，上傳資料庫      

    # 開始廣播
    sql = "UPDATE `broadcast` SET `pubkey`=%s,`transaction`=%s,`signature`=%s WHERE 1"
    mycursor.execute(sql,(pubkey, transaction, signature))
    mydb.commit()

    mycursor.close()
    mydb.close()

    trans_broadcast = 'broadcast,' + pubkey + ','+ transaction + ',' + signature

    try:
        s.send(trans_broadcast.encode())
        time.sleep(1)
    except:
        print("connect error")
        tkinter.messagebox.showwarning(
            'Error', '    Connect server fail !\nClick "OK" button to exit.')
        global file_flag
        file_flag = 1
        time.sleep(0.3)

def minerequestlist(s):  # request a list to mine
    outdata = 'list'
    #print('send: ' + outdata)

    try:
        s.send(outdata.encode())
        time.sleep(1)
    except:
        print("connect error")
        tkinter.messagebox.showwarning(
            'Error', '    Connect server fail !\nClick "OK" button to exit.')
        global file_flag
        file_flag = 1
        time.sleep(0.3)
        return

    global blockdata
    return blockdata

def start():  # start mine
    global pubkey
    global prikey
    global miner_stop
    global difficulty
    global temp
    global end_flag
    global file_flag

    try:
        # Pubkey read from pubkey.txt
        f = open('pubkey.txt')
        pubkey = f.read()
        f.close()

        # Prikey read from pubkey.txt
        f = open('prikey.txt')
        prikey = f.read()
        f.close()
    except:
        print("pubkey.txt or prikey.txt not found.")
        tkinter.messagebox.showwarning(
        'Error', 'pubkey.txt or prikey.txt not found.')
        file_flag = 1

    if not file_flag:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            s.send('req_initial_diff'.encode())
            threading.Thread(target=recv_data,args=(s,)).start()
            threading.Thread(target=alive,args=(s,)).start()
            time.sleep(1)
        except:
            print("connect error")
            tkinter.messagebox.showwarning(
            'Error', '    Connect server fail !\nClick "OK" button to exit.')
            file_flag = 1
            time.sleep(0.3)

        while True:
            if end_flag:
                s.close()
                break
            elif stop_flag:
                continue
            elif miner_stop:
                try:
                    s.send('req_miner'.encode())
                    time.sleep(1)
                    continue
                except:
                    print("connect error")
                    tkinter.messagebox.showwarning(
                    'Error', '    Connect server fail !\nClick "OK" button to exit.')
                    file_flag = 1
                    time.sleep(0.3)
            else:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print('Initializing ...')

                ### 驗證簽章
                try:
                    s.send('req_broadcast'.encode())
                    time.sleep(1) # 等待收到簽章資訊
                except:
                    print("connect error")
                    tkinter.messagebox.showwarning(
                    'Error', '    Connect server fail !\nClick "OK" button to exit.')
                    file_flag = 1
                    time.sleep(0.3)

                try:
                    de_pubkey = pubkey_recv
                    Trans = transaction_recv.encode()
                    signature = signature_recv
                    # 轉換簽章編碼
                    signature = signature.encode()
                    signature = base64.urlsafe_b64decode(signature)
                except:
                    print("Signature verify failed!")
                    de_pubkey = None
                    Trans = None
                    signature = None

                # 可解密公鑰
                if de_pubkey != None and de_pubkey != '' and de_pubkey != " ":
                    de_pubkey = de_pubkey.encode() # 轉成byte
                    de_pubkey = signature_rsa.decode_pubkey(de_pubkey)
                else:
                    de_pubkey = None

                # First Block挖礦
                global cnt
                if cnt == 0:
                    mydb = connect()
                    mycursor = mydb.cursor()
                    sql = "SELECT COUNT(*) FROM `block`"
                    mycursor.execute(sql)
                    result = mycursor.fetchall()
                    cnt = result[0][0]
                    cnt += 1
                    mycursor.close()
                    mydb.close()

                # 驗證正確則開始挖礦
                if signature_rsa.signature_verify(Trans, signature, de_pubkey) or cnt == 2: 
                    blockdata = minerequestlist(s)
                    if end_flag:
                        s.close()                    
                        break
                    proof = random.randint(0, 100000000)
                    hashnumber = "11111"
                    test = "1111"

                    # 取得難度
                    try:
                        s.send('req_diff'.encode())
                        time.sleep(1) # 等待難度回傳
                    except:
                        print("connect error")
                        tkinter.messagebox.showwarning(
                        'Error', '    Connect server fail !\nClick "OK" button to exit.')
                        file_flag = 1
                        time.sleep(0.3)

                    if difficulty != temp:
                        global diff_flag
                        diff_flag = 1
                    temp = difficulty

                    print("Mining ...")
                    start = time.time()
                    while hashnumber[0:difficulty] != "0" * difficulty:
                        if end_flag:
                            break
                        elif stop_flag:
                            continue
                        elif miner_stop:
                            print("\nBlock has been mined.")
                            print("Detecting new block ...")
                            time.sleep(10)
                            break

                        proof = proof + 1

                        # 計算算力
                        global count
                        count += 1

                        test = blockdata+str(proof)
                        hashnumber = hashlib.sha256(test.encode('utf-8')).hexdigest()
                        print(hashnumber)
                    end = time.time()
                    print()

                    if hashnumber[0:difficulty] == "0" * difficulty:  # complete block and sent to sever
                        if miner_stop:
                            continue

                        print("Success mining!")
                        print("Detecting new block ...\n")

                        # 交易簽章
                        produce_trans(s)

                        # 顯示在視窗
                        global show_hash
                        show_hash = str(hashnumber) + " time: " + str(round(end - start, 2)) + "s"
                        global success_flag
                        success_flag = 1
                        global success_proof
                        success_proof = proof
                        global success_count
                        success_count += 1

                        outdata = "succeed,"+hashnumber
                        test = ","+test
                        outdata = outdata+test
                        test = ","+str(proof)
                        outdata = outdata+test

                        if end_flag:                     
                            s.close()   
                            break

                        try:
                            s.send(outdata.encode())
                            time.sleep(9)
                        except:
                            print("connect error")
                            tkinter.messagebox.showwarning(
                            'Error', '    Connect server fail !\nClick "OK" button to exit.')
                            file_flag = 1
                            time.sleep(0.3)

def recv_data(s):
    global difficulty
    global temp
    global miner_stop
    global pubkey_recv
    global transaction_recv
    global signature_recv
    global blockdata

    while True:
        if end_flag:
            break
        if stop_flag:
            continue
        try:
            data = s.recv(1024).decode()
        except:
            print('Connection close')
            break
        if data[:4] == 'diff': # 從server取得難度
            difficulty = int(data[4:])
        elif data[:12] == 'initial_diff': # 從server取得初始難度
            temp = int(data[12:])
        elif data == 'miner_stop': # server要求停止挖礦
            miner_stop = 1
        elif data == 'miner_start': # server準許開始挖礦
            miner_stop = 0  
        elif data[:9] == 'broadcast': # 從server取得簽章資訊
            str = data.split(',')
            pubkey_recv = str[1]
            transaction_recv = str[2]
            signature_recv = str[3]
        elif data[0:5] == 'block': # 從server取得block資訊
            blockdata = data

# 讓server知道client還在線
def alive(s):
    while True:
        for i in range(3000):
            if end_flag:
                break
            time.sleep(0.1)
        if end_flag:
            break
        try:
            s.send("alive".encode())
        except:
            print('Connection close')
            break
        