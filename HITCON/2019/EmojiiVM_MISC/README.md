# EmojiiVM_MISC

## Instructions

Binary has emojiis for instructions and datas.

```text
INST_NOP         = 1
INST_ADD         = 2
INST_SUB         = 3
INST_MUL         = 4
INST_MOD         = 5
INST_XOR         = 6
INST_AND         = 7
INST_SETG        = 8
INST_SETEQ       = 9
INST_JMP         = 0Ah
INST_JNZ         = 0Bh
INST_JZ          = 0Ch
INST_PUSH_IMM    = 0Dh
INST_POP         = 0Eh
INST_GET_MEMO_BYTE  = 0Fh
INST_SET_MEMO_BYTE  = 10h
INST_MAKE_MEMO   = 11h
INST_DELETE_MEMO  = 12h
INST_WRITE_MEMO  = 13h
INST_PRINT_MEMO  = 14h
INST_PRINT_STACK_STR  = 15h
INST_PRINT_STACK_VAL  = 16h
INST_HLT         = 17h
```

By analysing the binary, the instructinos have these `0x1 ~ 0x17` instructions. And there are emojiis that represents constant 0 to 10.
So I wrote simple assembler for the VM.

```python
# simple assembler for emojiiVM
from re import findall

with open('payload.txt', 'rb') as f:
    code = f.read()

emoji_code = map(unichr,[0, 0x1f233, 0x2795, 0x2796, 0x274c, 0x2753, 0x274e, 0x1f46b, 0x1f480, 0x1f4af, 0x1f680, 0x1f236, 0x1f21a, 0x23ec, 0x1f51d, 0x1f4e4, 0x1f4e5, 0x1f195, 0x1f193, 0x1f4c4, 0x1f4dd, 0x1f521, 0x1f522, 0x1f6d1])
emoji_data = map(unichr,[0x1f600, 0x1f601, 0x1f602, 0x1f923, 0x1f61c, 0x1f604, 0x1f605, 0x1f606, 0x1f609, 0x1f60a, 0x1f60d])
inst = ['inv', 'nop', 'add', 'sub', 'mul', 'mod', 'xor', 'and', 'setg', 'seteq', 'jmp', 'jnz', 'jz', 'push', 'pop', 'getb_memo', 'setb_memo', 'make_memo', 'del_memo', 'write_memo', 'print_memo','print_stack_str', 'print_tos', 'hlt']

payload = ''
for line in code.split('\n'):
    prev = len(payload)
    for i in range(24):
        if line.find(inst[i]) != -1: payload += emoji_code[i]
    if line.find(inst[13]) != -1: payload += emoji_data[int(findall('\d+', line)[0])]
    if prev == len(payload): print line

print payload

with open('payload.evm', 'wb') as f:
    f.write(payload.encode('utf-8'))
```

## Writing Code

The restriction is 2000 byte, so I had to wrote a code that uses loops.
The pseudocode is like this.

```text
make memo and store ' * ' and ' = '
for i, j in 0..9
    get ' * ' from memo and ' = '
    print i + ' * ' + j + ' = '
halt
```

And this is the code for assembler.

```text
push 10
push 10
push 10
mul
mul
make_memo
push 1
push 0
push 0
setb_memo
push 1
push 1
push 0
setb_memo
push 0
push 0
getb_memo
print_tos
push 0
push 10
push 3
mul
push 2
add
add
print_stack_str
push 0
push 10
push 4
mul
push 2
add
add
print_stack_str
push 0
push 10
push 3
mul
push 2
add
add
print_stack_str
print_stack_str
push 1
push 0
getb_memo
print_tos
push 0
push 10
push 3
mul
push 2
add
add
print_stack_str
push 0
push 10
push 6
mul
push 1
add
add
print_stack_str
push 0
push 10
push 3
mul
push 2
add
add
print_stack_str
print_stack_str
push 1
push 0
getb_memo
push 0
push 0
getb_memo
mul
print_tos
push 10
print_stack_str
push 0
push 0
getb_memo
push 9
seteq
push 1
push 0
getb_memo
push 9
seteq
and
push 10
push 10
mul
push 2
mul
push 10
push 2
mul
push 4
add
add
jnz
push 1
push 0
getb_memo
push 9
seteq
push 10
push 10
mul
push 2
mul
push 0
add
push 2
add
jz
push 0
push 1
push 0
setb_memo
push 0
push 0
getb_memo
push 1
add
push 0
push 0
setb_memo
push 1
push 0
getb_memo
push 1
add
push 1
push 0
setb_memo
push 10
push 2
mul
push 3
add
jmp
hlt
```

The final emojiis for submission :

```text
⏬😍⏬😍⏬😍❌❌🆕⏬😁⏬😀⏬😀📥⏬😁⏬😁⏬😀📥⏬😀⏬😀📤🔢⏬😀⏬😍⏬🤣❌⏬😂➕➕🔡⏬😀⏬😍⏬😜❌⏬😂➕➕🔡⏬😀⏬😍⏬🤣❌⏬😂➕➕🔡🔡⏬😁⏬😀📤🔢⏬😀⏬😍⏬🤣❌⏬😂➕➕🔡⏬😀⏬😍⏬😅❌⏬😁➕➕🔡⏬😀⏬😍⏬🤣❌⏬😂➕➕🔡🔡⏬😁⏬😀📤⏬😀⏬😀📤❌🔢⏬😍🔡⏬😀⏬😀📤⏬😊💯⏬😁⏬😀📤⏬😊💯👫⏬😍⏬😍❌⏬😂❌⏬😍⏬😂❌⏬😜➕➕🈶⏬😁⏬😀📤⏬😊💯⏬😍⏬😍❌⏬😂❌⏬😀➕⏬😂➕🈚⏬😀⏬😁⏬😀📥⏬😀⏬😀📤⏬😁➕⏬😀⏬😀📥⏬😁⏬😀📤⏬😁➕⏬😁⏬😀📥⏬😍⏬😂❌⏬🤣➕🚀🛑
```

The flag is `hitcon{M0mmy_I_n0w_kN0w_h0w_t0_d0_9x9_em0j1_Pr0gr4mM!ng}`