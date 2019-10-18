from pwn import *

def proof(p):
    p.recvuntil('token:\n')
    cmd = p.recvline().strip().split(' ')
    print cmd
    h = process(cmd)
    h.recvuntil('token: ')
    rec = h.recvline().strip()
    print rec
    p.sendline(rec)

with open('payload.evm', 'rb') as f:
    ans = f.read()

p = remote('3.115.122.69', 30261)

proof(p)

p.recvuntil('bytes')
p.sendline(str(len(ans)))
p.recvuntil('file:')
p.send(ans)

p.interactive() # hitcon{M0mmy_I_n0w_kN0w_h0w_t0_d0_9x9_em0j1_Pr0gr4mM!ng}