#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import client
import threading
import tkinter.messagebox
import sys
import os
import time
from connect import *
from signature_rsa import generate_key

login_flag = 0

def login_check():
    if login_flag:
        return True
    else:
        return False

# 檢查帳號是否存在
def acc_check(acc, pwd):
    try:
        mydb = connect()
    except:
        print("dbconnect error")
        tkinter.messagebox.showwarning(
            'Error', '    Connect server fail !\nClick "OK" button to exit.')
        client.file_flag = 1
        time.sleep(0.3)
        
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM `user` WHERE ACCOUNT=%s AND PASSWORD=%s"
    mycursor.execute(sql, (acc, pwd))
    result = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    if result[0] == (0,):  # 查無此帳號
        return False
    else:
        return True
    
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def login(self):
    def miner():
        client.stop_flag = 0
        client.end_flag = 0
        client.file_flag = 0
        start.config(text="Pause", command=Pause)
        t.start()
            
        update_performance()
        update_success()
        update_proof_hash()
        update_diff()
        check_file()

    def Finish():
        global login_flag
        login_flag = 0
        client.end_flag = 1
        client.success_count = 0
        # 銷燬視窗。
        window_miner.destroy()
        window_hash.destroy()

    def Pause():
        start.config(text="Resume", command=Resume)
        client.stop_flag = 1

    def Resume():
        start.config(text="Pause", command=Pause)
        client.stop_flag = 0

    def update_performance():
        # 每秒更新算力
        window_miner.after(1000, update_performance)
        performance.set(str(client.count)+"/s")
        client.count = 0

    def update_success():
        # 自動更新成功數量
        window_miner.after(100, update_success)
        if client.stop_flag != 1:
            success.set(str(client.success_count))

    def update_proof_hash():
        window_miner.after(100, update_proof_hash)
        if(client.success_flag and client.stop_flag != 1):
            time.sleep(0.5)
            success_text.insert("end", str(client.success_proof) + "\n")
            success_text.see("end")
            hash_text.insert("end", client.show_hash + "\n")
            hash_text.see("end")
  
            client.success_flag = 0

    def update_diff():
        window_hash.after(100, update_diff) # check difficulty
        if client.diff_flag and client.stop_flag != 1:
            hash_text.insert("end", "Adjust difficulty to " + str(client.difficulty) + "\n")
            hash_text.see("end")
            client.diff_flag = 0

    def check_file():
        window_miner.after(100, check_file)
        if client.file_flag:
            Finish()
    
    # 挖礦建立多執行續
    t = threading.Thread(target=client.start)

    client.account = e1.get()
    pwd = e2.get()
    print(client.account)
    print(pwd)

    global login_flag

    if login_check():
        print(login_flag)
        tkinter.messagebox.showwarning('Error', 'Already login!')
    elif acc_check(client.account, pwd):
        login_flag = 1  # 已登入狀態
        print(login_flag)
        
        msg = "Hi, {}.\nLogin Successful.".format(client.account)
        tkinter.messagebox.showinfo(title="info",
                                    message=msg)
        
        # 產生挖礦視窗
        window_miner = tk.Toplevel(window)
        window_miner.geometry('326x160+700+270')
        window_miner.title('Miner window')

        username = tk.Label(window_miner, text='USER: %s' % client.account)
 
        success_label = tk.Label(window_miner, text='Success:')
        
        start = tk.Button(window_miner, text='Start', command=miner)
        finish = tk.Button(window_miner, text='Exit', command=Finish)

        # 算力圖片
        global img2
        img2 = tk.PhotoImage(file=resource_path(
            os.path.join("pic", "performance.png")))
        speedLogo = tk.Label(window_miner, image=img2)

        # 算力
        performance = tk.StringVar()
        performance.set("0/s")
        performance_label = tk.Label(
            window_miner, textvariable=performance, width=6, font=('Calibri', 9))

        # 成功解密
        success = tk.StringVar()
        success.set("0")
        success_count = tk.Label(
            window_miner, textvariable=success, width=6, font=('Calibri', 12))

        # 解密視窗
        success_text = tk.Text(window_miner, width=10, height=3)

        username.place(x=1, y=10)
        start.place(x=160, y=120)
        finish.place(x=250, y=120)
        speedLogo.place(x=120, y=2)
        performance_label.place(x=196, y=65)
        success_count.place(x=0, y=120)
        success_label.place(x=0, y=100)
        success_text.place(x=10, y=40)
        
        window_miner.protocol("WM_DELETE_WINDOW", disable_event)
        window_miner.resizable(width=0, height=0) #視窗不可調整大小

        # Hash視窗
        window_hash = tk.Toplevel(window_miner)
        window_hash.title('Hash window')
        # window_hash.geometry("720x345+1100+200")
        window_hash.geometry("840x420+1030+200")

        # Hash值和時間
        scrollbar = tk.Scrollbar(window_hash)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hash_text = tk.Listbox(window_hash, font=('Courier', 10), yscrollcommand=scrollbar.set)
        hash_text.pack(side="left",fill="both", expand=True)
        scrollbar.config(command=hash_text.yview)

        window_hash.protocol("WM_DELETE_WINDOW", disable_event)
        window_hash.resizable(width=0, height=0) #視窗不可調整大小
    else:
        print(login_flag)
        msg = "Login fail."
        tkinter.messagebox.showwarning(title="info",
                                       message=msg)

# Sign_up Window
def register():
    def sign_to_SharkCoin_Website():
        # 註冊時所輸入的資訊
        nacc = new_acc.get()
        npwd = new_pwd.get()
        npwdc = new_pwd_confirm.get()

        pubkey, prikey = generate_key()

        path = 'pubkey.txt'
        f = open(path, 'w')
        f.write(pubkey)
        f.close()

        path = 'prikey.txt'
        f = open(path, 'w')
        f.write(prikey)
        f.close()

        # 檢查密碼
        if npwd != npwdc:
            tkinter.messagebox.showwarning(
            'Error', 'Password not correct!')
        else:
            # 註冊檢查
            try:
                mydb = connect()
            except:
                print("dbconnect error")
                tkinter.messagebox.showwarning(
                    'Error', '    Connect server fail !\nClick "OK" button to exit.')
                client.file_flag = 1
                time.sleep(0.3)
            mycursor = mydb.cursor()
            sql = "INSERT INTO `user` VALUE(%s, %s, %s, %s, CURRENT_TIMESTAMP)"

            try:
                mycursor.execute(sql,(nacc, npwd, pubkey, prikey))
                mydb.commit()
                # 註冊成功
                tkinter.messagebox.showinfo(
                    'Welcome', '            You have successfully signed up!\nPubkey and Prikey have stored in your computer!')
                # 然後銷燬視窗。
                window_sign_up.destroy()
            except:
                # 註冊失敗
                tkinter.messagebox.showwarning(
                    'Error', 'Account exist!')
            
            mycursor.close()
            mydb.close()

    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('326x160+700+270')
    window_sign_up.title('Sign up window')

    tk.Label(window_sign_up, text='User name: ').place(
        x=10, y=10)
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y=90)

    new_acc = tk.Entry(window_sign_up, width=14, font=(
        'Calibri', 12))
    new_pwd = tk.Entry(window_sign_up, show='*',
                       width=14, font=('Calibri', 12))
    new_pwd_confirm = tk.Entry(
        window_sign_up, show='*', width=14, font=('Calibri', 12))

    btn_comfirm_sign_up = tk.Button(
        window_sign_up, text='Sign up', command=sign_to_SharkCoin_Website)

    new_acc.place(x=160, y=10)
    new_pwd.place(x=160, y=50)
    new_pwd_confirm.place(x=160, y=90)
    btn_comfirm_sign_up.place(x=205, y=120)

def exit():
    client.end_flag = 1
    window.destroy()

window = tk.Tk()
window.title('SharkCoin')
window.geometry("360x120+800+400")
window.bind('<Return>', login)

# 建立按鈕
button1 = tk.Button(window, text='Login', command=lambda: login("") )
button1.config(bg="skyblue")
button1.config(width=4, height=1)

button2 = tk.Button(window, text='Sign up', command=register)
button2.config(bg="SeaGreen3")
button2.config(width=6, height=1)

imgExit = tk.PhotoImage(file=resource_path(os.path.join("pic", "exit.png")))
buttonExit = tk.Button(window, height=20, width=40,
                       image=imgExit, command=exit)

# 標示文字
label1 = tk.Label(window, text='SharkAcc:')
label2 = tk.Label(window, text='SharkPwd:')

# 輸入
e1 = tk.Entry(window, show=None, width=14, font=('Calibri', 12))  # 顯示成明文形式
e2 = tk.Entry(window, show='*', width=14, font=('Calibri', 12))   # 顯示成密文形式

# 圖片
img = tk.PhotoImage(file=resource_path(os.path.join("pic", "coin.png")))
img1 = img.subsample(3, 3)
labelLogo = tk.Label(window, image=img1)

# 排版
label1.place(x=0, y=10)
label2.place(x=0, y=40)

e1.place(x=90, y=10)
e2.place(x=90, y=40)

button1.place(x=95, y=70)
button2.place(x=165, y=70)

labelLogo.place(x=250, y=0)
buttonExit.place(x=2, y=90)

# 禁止視窗按X

def disable_event():
    pass

window.protocol("WM_DELETE_WINDOW", disable_event)
window.resizable(width=0, height=0) #視窗不可調整大小
window.mainloop()
