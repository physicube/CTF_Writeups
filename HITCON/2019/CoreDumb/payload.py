import struct
from z3 import *
from ctypes import c_uint32
from base64 import b64decode as bd

p16 = lambda x: struct.pack('<H', x)
p32 = lambda x: struct.pack('<I', x)
p64 = lambda x: struct.pack('<Q', x)
u32 = lambda x: struct.unpack('<I', x)[0]
u = lambda x: c_uint32(x).value

def xtea_decrypt(e, num_round):
    v0 = u(e)
    v1 = u(e >> 32)

    key = map(ord, ['C','0','R','3'])
    delta = 0x1337DEAD
    total = u(delta * num_round) 

    for _ in range(num_round):
        v1 = u(v1 - (u((u(v0 << 4) ^ u(v0 >> 5)) + v0) ^ u(total + key[(total >> 11) & 3])))
        total = u(total - delta)
        v0 = u(v0 - (u((u(v1 << 4) ^ u(v1 >> 5)) + v1) ^ u(total + key[total & 3])))
    return p32(v0), p32(v1)

def crc32(data,size,prev=0):
    crc = prev ^ 0xFFFFFFFF
    for i in range(0,size,8):
        crc = crc ^ (z3.LShR(data,i) & 0xFF)
        for _ in range(8):
            crc = If(crc & 1 == BitVecVal(1, size), z3.LShR(crc,1) ^ 0xEDB88320, z3.LShR(crc,1))
    #return crc ^ 0xFFFFFFFF
    return crc

# xor 
def fun1(): # flag[:10]
    ret = ''
    key = p32(0x624D7544)
    e = p64(0x413317635722649) + p16(0x5e4e)
    for i in range(10):
        ret += chr(ord(e[i]) ^ (ord(key[i % 4]) - 7))

    return ret

# xtea
def fun2(): # flag[10:18]
    key = 'C0R3'
    e = [0x95CB8DBD, 0xF84CC79, 0xB899A876, 0xA5DAB55, 0x9A8B3BBA, 0x70B238A7, 0x72B53CF1, 0xD47C0209]
    ret = ['' for _ in range(8)]
    for i in range(4):
        ret[i], ret[i+4] = xtea_decrypt(e[2*i] + (e[2*i + 1] << 32), 32)
    return ''.join(ret)

# custom base64
def fun3():
    table = p64(0x32716E66492D7C2A) + p64(0x24645A410A202130) + p64(0x7B2F445C6F583C72) + p64(0x377A5434617E434B) + \
        p64(0x7D0B60783A5E5929) + p64(0x76696D4F79317353) + p64(0x4E5F5B405D250D23) + p64(0x677551562C6A4828)
    btable = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    e = p64(0x23415F4125516034) + p64(0x7D482F41255A3A54) + p64(0xB515B41536D257B)
    d = ''
    for i in e:
        for j, entry in enumerate(table):
            if i == entry:
                d += btable[j]
    return bd(d)

# modified rc4, by rbtree
def fun4():
    key = [ i for i in range(246) ]
    arr = [ 0x50, 0x6C, 0x33, 0x61, 0x73, 0x5F, 0x64, 0x30,
            0x6E, 0x27, 0x74, 0x5F, 0x63, 0x52, 0x34, 0x35,
            0x68, 0x5F, 0x31, 0x6E, 0x5F, 0x2B, 0x68, 0x21,
            0x73, 0x5F, 0x66, 0x55, 0x6E, 0x43, 0x2B, 0x31,
            0x30, 0x6E ]
    
    store = 0
    for i in range(246):
        store = (arr[i % 34] + key[i] + store) % 246
        key[i], key[store] = key[store], key[i]
    
    target = [ 0x2B, 0x55, 0x5D, 0x93, 0xA0, 0x43, 0xDD, 0x14,
            0x43, 0x52, 0x7D, 0xE5 ]
    
    store = 0
    ans = ""
    for i in range(0, 12):
        store = (store + key[i+1]) % 246
        key[i+1], key[store] = key[store], key[i+1]
    
        ans += chr(key[(key[i+1] + key[store]) % 246] ^ target[i])
    
    return ans

# crc, by rbtree
def fun5():
    
    s = Solver()
    data = BitVec('data', 32)
    s.add(crc32(data, 32) == 0x29990129)
    
    if s.check() == sat:
        return p32(s.model()[data].as_long())
    else:
        print "unsat"

funcs = [fun1, fun2, fun3, fun4, fun5]
flag = ''
for func in funcs:
    flag += func()
    
print 'hitcon{' + flag + '}' # hitcon{tH4nK_U_s0_muCh_F0r_r3c0v3r1ng_+h3_fL4g_1_Luv_y0u_<3}