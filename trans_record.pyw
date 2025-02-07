#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import hashlib
import base64, os
import tkinter.messagebox
from trans_icon import iconImg
from connect import connect
from signature_rsa import P2PKHToAddress

end_flag = 0

window_trans = tk.Tk()
window_trans.geometry('780x345+1100+200')
window_trans.title('Transaction record')

scrollbar = tk.Scrollbar(window_trans)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(window_trans, width=160, height=40, yscrollcommand=scrollbar.set)

# Pubkey read from pubkey.txt
try:
    f = open('pubkey.txt')
    pubkey = f.read()
    tmp = hashlib.sha256(pubkey.encode('utf-8')).hexdigest()
    address = P2PKHToAddress(tmp).decode()
    print(address)
    f.close()
except:
    end_flag = 1
    tkinter.messagebox.showwarning(
            'Error', 'pubkey.txt not found.')

if not end_flag:

    def get_coin():
        # Comparing address from transaction record
        mydb = connect()
        cursor = mydb.cursor()
        sql = "SELECT height, blockdata FROM `block`"
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        mydb.close()

        str1 = "proof"
        str2 = "transaction"
        str3 = "coin"
        str4 = "\nreward"

        coin = 0
        for x in result:
            if(x[0] != 1):
                s1 = x[1][:x[1].index(str1)]
                s2 = s1[s1.index(str2):]
                s3 = s2[13:] # trans record
                s4 = s2[13:s2.index(str4)] # address
                s5 = 0 # coin
                
                s5 = s3[:s3.index(str3)][51:]
                if address == s4:
                    coin += float(s5)
        return coin

    # Comparing address from transaction record
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "SELECT height, blockdata, hash FROM `block`"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    str1 = "proof"
    str2 = "transaction"
    str3 = "reward"

    count = 0
    for x in result:
        if x[0] != 1:
            s1 = x[1][:x[1].index(str1)]
            s2 = s1[s1.index(str2):]
            s3 = s2[13:] # trans record
            s4 = s3[:s3.index(str3) - 1] # address
            s5 = s3.replace('\n', ' ')

            if address == s4:
                listbox.insert(tk.END, "Block: " + str(x[0] - 1))
                listbox.insert(tk.END, s5)
                count += 1

    listbox.insert(tk.END, "")
    listbox.insert(tk.END, "Total transactions: " + str(count))
    listbox.insert(tk.END, "Total SharkCoin: " + str(get_coin()))

    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=listbox.yview)

    window_trans.resizable(width=0, height=0) #視窗不可調整大小

    tmpIcon = open('tmp.ico', 'wb+')
    tmpIcon.write(base64.b64decode(iconImg))
    tmpIcon.close()

    window_trans.iconbitmap('tmp.ico')
    os.remove('tmp.ico')
    window_trans.mainloop()
