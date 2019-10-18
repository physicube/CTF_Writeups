import struct
from re import *
from pwn import u16

with open('dump', 'r') as f: # tshark -r ev3_player.pklg -Y 'btrfcomm && data.data' -T fields -e data.data  > dump
    dump = f.read()
'''
with open('dcmd.txt', 'r') as f:
    data = f.read()

dcmd = {}

data = findall('\w+\s+= 0x\w+', data)
for line in data:
    string, num = tuple(findall('\w+', line))
    dcmd[int(num, 16)] = string
'''
ctype = {
0x00:'DCMD_REPLY',
0x01:'SCMD_REPLY',
0x02:'DIRECT_REPLY',
0x03:'SYSTEM_REPLY',
0x04:'DIRECT_REPLY_ERROR',
0x05:'SYSTEM_REPLY_ERROR',
0x80:'DCMD_NO_REPLY',
0x81:'SCMD_NO_REPLY',
}

scmd = {
0x92:'BEGIN_DOWNLOAD',
0x93:'CONTINUE_DOWNLOAD',
0x94:'BEGIN_UPLOAD',
0x95:'CONTINUE_UPLOAD',
0x96:'BEGIN_GETFILE',
0x97:'CONTINUE_GETFILE',
0x98:'CLOSE_FILEHANDLE',
0x99:'LIST_FILES',
0x9a:'CONTINUE_LIST_FILES',
0x9b:'CREATE_DIR',
0x9c:'DELETE_FILE',
0x9d:'LIST_OPEN_HANDLES',
0x9e:'WRITEMAILBOX',
0x9f:'BLUETOOTHPIN',
0xa0:'ENTERFWUPDATE'
}

isdump = False
f = 1

for line in dump.split('\n'):
    packet = line.replace(':', '').decode('hex')
    size, cnt, cmd_type = struct.unpack('<HHB', packet[:5])
    
    if cmd_type == 0x01 or cmd_type == 0x81: # system command
        print ctype[cmd_type], ':', scmd[ord(packet[5])]
        print 'data :', packet[6:]

        if ord(packet[5]) == 0x92 and packet[6:].find('ag.rsf') != -1:
            f = open('ag.rso', 'wb')
            isdump = True
        if ord(packet[5]) == 0x93 and isdump:
            f.write(packet[7:])
        if ord(packet[5]) == 0x98 and isdump:
            f.close()
            isdump = False
            
    elif cmd_type == 0x03 or cmd_type == 0x05: # system command replies
        print 'reply type :', cmd_type, 'to', scmd[ord(packet[5])], ', status :', ord(packet[6])
        print 'data : ', packet[7:]
    elif cmd_type == 0x00 or cmd_type == 0x80: # direct command
        #print ctype[cmd_type], ',', 'code :', dcmd[ord(packet[5])]
        print 'data : ', packet[6:]
    elif cmd_type == 0x02 or cmd_type == 0x04:
        print 'reply type :', cmd_type
        print 'data : ', packet[5:]