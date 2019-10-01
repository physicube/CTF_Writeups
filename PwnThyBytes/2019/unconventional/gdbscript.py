# gdb-peda$ source gdbscript.py

cmd = lambda x:gdb.execute(x, to_string=True) 

def setbp():
    cmd('file unconventional_mod')
    cmd('d')
    cmd('catch syscall')
    
    # set read watchpoint to start of flag
    cmd('rwatch *(0x403c46)')
    # set read watchpoint to end of flag
    cmd('rwatch *(0x403c46 + 0x20 - 4)')
    
def setup(): 
    # move to read syscall
    cmd('c')
    cmd('c')

    # prevent errno 14 (Bad address)
    cmd('set $rsi = $rsi - 0x1000')
    cmd('set $rsp = $rsi')
    cmd('c')
    
    # skip to flag read
    for i in range(4):
        cmd('c')

# use this to get deobfuscated trace.txt
def trace():
    f = open('trace.txt', 'w')

    while 1:
        cmd('ni')
        inst = cmd('x/i $rip')
        if "nop" not in inst and "rip" not in inst and "\tf" not in inst:
            f.write(inst)
            f.flush()

    f.close()


flag = 'PTBCTF{'
flag += 'a' * (0x20 - len(flag) - 1) + '}'

setbp()
cmd('r <<< ' + flag)
setup()

# trace()