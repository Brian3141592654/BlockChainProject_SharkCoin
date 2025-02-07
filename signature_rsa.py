#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rsa
import base58
import base64
import binascii
import hashlib

def signature_verify(message, signature, pubkey):
    try:
        rsa.verify(message, signature, pubkey)
        return True
    except:
        # print("Signature verify failed!")
        return False

# 產生key並編碼存到user資料裡
def generate_key():
    # 生成RSA公鑰和私鑰
    pubkey, privkey = rsa.newkeys(512)

    # 經過base64編碼
    pubkey = base64.encodebytes(pubkey.save_pkcs1())  # byte
    privkey = base64.encodebytes(privkey.save_pkcs1())

    return pubkey.decode(), privkey.decode()

# 公鑰解碼
def decode_pubkey(pubkey):
    pubkey_str= base64.decodebytes(pubkey)
    pubkey = rsa.PublicKey.load_pkcs1(pubkey_str)

    return pubkey 

# 私鑰解碼
def decode_prikey(key):
    privkey_str= base64.decodebytes(key)
    privkey = rsa.PrivateKey.load_pkcs1(privkey_str)

    return privkey

# 產生地址
def P2PKHToAddress(pkscript, istestnet=False):
    pub = pkscript[6:-4] # get pkhash, inbetween first 3 bytes and last 2 bytes
    p = '00' + pub # prefix with 00 if it's mainnet
    if istestnet:
        p = '6F' + pub # prefix with 0F if it's testnet
    h1 = hashlib.sha256(binascii.unhexlify(p))
    h2 = hashlib.new('sha256', h1.digest())
    h3 = h2.hexdigest()
    a = h3[0:8] # first 4 bytes
    c = p + a # add first 4 bytes to beginning of pkhash
    d = int(c, 16) # string to decimal
    b = d.to_bytes((d.bit_length() + 7) // 8, 'big') # decimal to bytes
    address = base58.b58encode(b) # bytes to base58
    if not istestnet:
        address = b'1' + address # prefix with 1 if it's mainnet
    return address
