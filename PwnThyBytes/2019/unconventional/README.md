# Unconventional - Rev

- Solved during CTF.

The binary's elf header had an invalid class(0x80) so I changed it to 0x2(x64) to use gdb. After that, I used `gdbscript.py` to get the actual trace(binary is obfuscated with FPU operations).

Flag(argv) bytes are saved in `0x403c46`. And this binary shuffles flag bits and moves flag bits to `flags` register and modifies registers.

This is what binary actually does to input.

```
# flag bit change
flag 76543210
flag 07654321
flag 70654321
flag 73214065
flag 23X14065
SF, ZF, AF, PF, CF <- flag bit 2, 3, 1, 0, 5

simplified routine
r8 <<= 1
if flag[5]:
    r8 |= 1
r9 <<= 1
if flag[2]:
    r9 |= 1
r10 <<= 1
if flag[3]:
    r10 |= 1
r12 <<= 1
if flag[0]:
    r12 |= 1
r13 <<= 1
if flag[1]:
    r13 |= 1
r14 <<= 1
if flag[4]:
    r14 |= 1
r15 <<= 1
if flag[6]:
    r15 |= 1
register's upper 32 bits should be equal to lower 32 bits
```

The payload is in `payload.py`.
