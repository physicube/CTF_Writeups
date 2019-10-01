r8 = 0x7f7f7f80
r9 = 0x5bdbd764
r10 = 0xfecac280
r12 = 0x69b5bd90
r13 = 0x8ac68ad8
r14 = 0x61819da6
r15 = 0x7ffffffe

flag = ''
for i in range(0x20):
    byte = 0
    byte |= ((r8 >> (31 - i)) & 1) << 5
    byte |= ((r9 >> (31 - i)) & 1) << 2
    byte |= ((r10 >> (31 - i)) & 1) << 3
    byte |= ((r12 >> (31 - i)) & 1) << 0
    byte |= ((r13 >> (31 - i)) & 1) << 1
    byte |= ((r14 >> (31 - i)) & 1) << 4
    byte |= ((r15 >> (31 - i)) & 1) << 6
    flag = chr(byte) + flag
print (flag.strip())

# PTBCTF{unusual_unclean_unholy}