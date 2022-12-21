# rick

## Description
Author: @Gary#4657

These files were on a USB I bought from a pawn shop.

Download the files below.
Attachments: [program](https://ctf.nahamcon.com/files/e8daa520cc817bb922084b1bb58724a6/program?token=eyJ1c2VyX2lkIjoxNDI1LCJ0ZWFtX2lkIjo3NzUsImZpbGVfaWQiOjIzfQ.Y50k_Q.6szfbgxdP2EGKCCji5zL3pjApGw) [ct.enc](https://ctf.nahamcon.com/files/d8f6af6cfa68e9a2b81085542112a944/ct.enc?token=eyJ1c2VyX2lkIjoxNDI1LCJ0ZWFtX2lkIjo3NzUsImZpbGVfaWQiOjIyfQ.Y50k_Q.-Hqe0Jmv6xduROI-y6Cgmxt_MzI)

## Solve
First I opened the `program` binary in Ghidra and started renaming variables to get an easier understanding.

Here is the `main()` function:
```c
bool main(void)

{
  int ct;
  ulong length;
  void *input_buf;
  bool opened;
  
  input_file = fopen("input.txt","rb");
  opened = input_file != (FILE *)0x0;
  if (opened) {
    fseek(input_file,0,2);
    length = ftell(input_file);
    fseek(input_file,0,0);
    input_buf = malloc((long)(int)length);
    fread(input_buf,(long)(int)length,1,input_file);
    fclose(input_file);
    ct = encrypt(input_buf,length & 0xffffffff);
    output_file = fopen("ct.enc","wb");
    fwrite(ciphertext,(long)ct,1,output_file);
    fclose(output_file);
  }
  else {
    puts("Could not open flag.txt\n");
  }
  return opened;
}
```
Basically what this is doing is opening `input.txt`, reading it into a buffer, then calling the `encrypt()` function (I renamed this), and writing the ciphertext to `ct.enc`.

Now let's look at the encryption process:
```c
int encrypt(uchar *plaintext,int plaintext_len)

{
  long in_FS_OFFSET;
  int len;
  int local_24;
  EVP_CIPHER_CTX *ctx;
  EVP_CIPHER *EVP_aes_256_cbc;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  len = plaintext_len;
  memset(&iv,0,0x10);
  ciphertext = (uchar *)malloc((long)plaintext_len);
  ctx = EVP_CIPHER_CTX_new();
  EVP_aes_256_cbc = EVP_aes_128_cbc();
  generate_key();
  EVP_EncryptInit(ctx,EVP_aes_256_cbc,&key,&iv);
  EVP_EncryptUpdate(ctx,ciphertext,&len,plaintext,plaintext_len);
  EVP_EncryptFinal_ex(ctx,ciphertext + len,&local_24);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_24 + len;
}
```
This function is encrypting the plaintext with EVP encryption. I read some documentation [here](https://wiki.openssl.org/index.php/EVP_Symmetric_Encryption_and_Decryption) to get an understanding of the functions being called. The cipher is an implementation of AES.

I renamed the `generate_key()` function for readability but inside this function a 16 byte key is generated. Here is the decompiled C code:
```c
void generate_key(void)

{
  uint local_10;
  int i;
  
  for (i = 0; i < 0x10; i = i + 1) {
    if (i == 0) {
      local_10 = 0x27e2;
    }
    else {
      local_10 = (local_10 + i) * 4 ^ 0x29fa;
    }
    (&key)[i] = (char)local_10;
  }
  return;
}
```

Trying to script this out to build the key wasn't working for me so I decided to use `gdb` and grab the key and IV from memory. This is going to help us decode the `ct.enc` file that the challenge gave us.
```as
user@arch:~/cyber/ctf/nahamcon-2022/rick$ gdb ./program 
GNU gdb (GDB) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
GEF for linux ready, type `gef' to start, `gef config' to configure
90 commands loaded and 5 functions added for GDB 12.1 in 0.00ms using Python engine 3.10
Reading symbols from ./program...
Debuginfod has been disabled.
To make this setting permanent, add 'set debuginfod enabled off' to .gdbinit.
(No debugging symbols found in ./program)
gef➤  r
Starting program: /home/user/cyber/ctf/nahamcon-2022/rick/program 
[*] Failed to find objfile or not a valid file format: [Errno 2] No such file or directory: 'system-supplied DSO at 0x7ffff7fc8000'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
[Inferior 1 (process 139902) exited with code 01]
gef➤  info file
Symbols from "/home/user/cyber/ctf/nahamcon-2022/rick/program".
Local exec file:
	`/home/user/cyber/ctf/nahamcon-2022/rick/program', file type elf64-x86-64.
	Entry point: 0x555555555220
	0x0000555555554318 - 0x0000555555554334 is .interp
	0x0000555555554338 - 0x0000555555554358 is .note.gnu.property
	0x0000555555554358 - 0x000055555555437c is .note.gnu.build-id
	0x000055555555437c - 0x000055555555439c is .note.ABI-tag
	0x00005555555543a0 - 0x00005555555543c4 is .gnu.hash
	0x00005555555543c8 - 0x00005555555545c0 is .dynsym
	0x00005555555545c0 - 0x0000555555554709 is .dynstr
	0x000055555555470a - 0x0000555555554734 is .gnu.version
	0x0000555555554738 - 0x0000555555554788 is .gnu.version_r
	0x0000555555554788 - 0x0000555555554848 is .rela.dyn
	0x0000555555554848 - 0x00005555555549b0 is .rela.plt
	0x0000555555555000 - 0x000055555555501b is .init
	0x0000555555555020 - 0x0000555555555120 is .plt
	0x0000555555555120 - 0x0000555555555130 is .plt.got
	0x0000555555555130 - 0x0000555555555220 is .plt.sec
	0x0000555555555220 - 0x0000555555555605 is .text
	0x0000555555555608 - 0x0000555555555615 is .fini
	0x0000555555556000 - 0x0000555555556034 is .rodata
	0x0000555555556034 - 0x0000555555556088 is .eh_frame_hdr
	0x0000555555556088 - 0x00005555555561d0 is .eh_frame
	0x0000555555557d38 - 0x0000555555557d40 is .init_array
	0x0000555555557d40 - 0x0000555555557d48 is .fini_array
	0x0000555555557d48 - 0x0000555555557f48 is .dynamic
	0x0000555555557f48 - 0x0000555555558000 is .got
	0x0000555555558000 - 0x0000555555558010 is .data
	0x0000555555558010 - 0x0000555555558058 is .bss
	0x00007ffff7fca2a8 - 0x00007ffff7fca2e8 is .note.gnu.property in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fca2e8 - 0x00007ffff7fca30c is .note.gnu.build-id in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fca310 - 0x00007ffff7fca4dc is .hash in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fca4e0 - 0x00007ffff7fca6c8 is .gnu.hash in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fca6c8 - 0x00007ffff7fcaa88 is .dynsym in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fcaa88 - 0x00007ffff7fcad49 is .dynstr in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fcad4a - 0x00007ffff7fcad9a is .gnu.version in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fcada0 - 0x00007ffff7fcae8c is .gnu.version_d in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fcae90 - 0x00007ffff7fcaf38 is .rela.dyn in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fcaf38 - 0x00007ffff7fcaf50 is .relr.dyn in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fcb000 - 0x00007ffff7ff0f85 is .text in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ff1000 - 0x00007ffff7ff6f78 is .rodata in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ff6f78 - 0x00007ffff7ff6f79 is .stapsdt.base in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ff6f7c - 0x00007ffff7ff78c0 is .eh_frame_hdr in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ff78c0 - 0x00007ffff7ffac58 is .eh_frame in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ffb9e0 - 0x00007ffff7ffce20 is .data.rel.ro in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ffce20 - 0x00007ffff7ffcfa0 is .dynamic in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ffcfa0 - 0x00007ffff7ffcfe8 is .got in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ffd000 - 0x00007ffff7ffe0e8 is .data in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7ffe0f0 - 0x00007ffff7ffe2b8 is .bss in /lib64/ld-linux-x86-64.so.2
	0x00007ffff7fc8120 - 0x00007ffff7fc8168 is .hash in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8168 - 0x00007ffff7fc81c4 is .gnu.hash in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc81c8 - 0x00007ffff7fc8300 is .dynsym in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8300 - 0x00007ffff7fc838b is .dynstr in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc838c - 0x00007ffff7fc83a6 is .gnu.version in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc83a8 - 0x00007ffff7fc83e0 is .gnu.version_d in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc83e0 - 0x00007ffff7fc8500 is .dynamic in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8500 - 0x00007ffff7fc8554 is .note in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8554 - 0x00007ffff7fc8598 is .eh_frame_hdr in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8598 - 0x00007ffff7fc8698 is .eh_frame in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc86a0 - 0x00007ffff7fc8d01 is .text in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8d01 - 0x00007ffff7fc8d55 is .altinstructions in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7fc8d55 - 0x00007ffff7fc8d71 is .altinstr_replacement in system-supplied DSO at 0x7ffff7fc8000
	0x00007ffff7c002a8 - 0x00007ffff7c002d8 is .note.gnu.property in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c002d8 - 0x00007ffff7c002fc is .note.gnu.build-id in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c00300 - 0x00007ffff7c077cc is .gnu.hash in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c077d0 - 0x00007ffff7c22320 is .dynsym in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c22320 - 0x00007ffff7c37d11 is .dynstr in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c37d12 - 0x00007ffff7c3a0ae is .gnu.version in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c3a0b0 - 0x00007ffff7c3a2e0 is .gnu.version_d in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c3a2e0 - 0x00007ffff7c3a3c0 is .gnu.version_r in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c3a3c0 - 0x00007ffff7c74cc8 is .rela.dyn in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c75000 - 0x00007ffff7c75020 is .init in /usr/lib/libcrypto.so.1.1
	0x00007ffff7c76000 - 0x00007ffff7e20e01 is .text in /usr/lib/libcrypto.so.1.1
	0x00007ffff7e20e04 - 0x00007ffff7e20e11 is .fini in /usr/lib/libcrypto.so.1.1
	0x00007ffff7e21000 - 0x00007ffff7e64b00 is .rodata in /usr/lib/libcrypto.so.1.1
	0x00007ffff7e64b00 - 0x00007ffff7e708f4 is .eh_frame_hdr in /usr/lib/libcrypto.so.1.1
	0x00007ffff7e708f8 - 0x00007ffff7ead770 is .eh_frame in /usr/lib/libcrypto.so.1.1
	0x00007ffff7eae0f0 - 0x00007ffff7eae0f8 is .init_array in /usr/lib/libcrypto.so.1.1
	0x00007ffff7eae0f8 - 0x00007ffff7eae100 is .fini_array in /usr/lib/libcrypto.so.1.1
	0x00007ffff7eae100 - 0x00007ffff7ed8928 is .data.rel.ro in /usr/lib/libcrypto.so.1.1
	0x00007ffff7ed8928 - 0x00007ffff7ed8b08 is .dynamic in /usr/lib/libcrypto.so.1.1
	0x00007ffff7ed8b08 - 0x00007ffff7ed8ff0 is .got in /usr/lib/libcrypto.so.1.1
	0x00007ffff7ed9000 - 0x00007ffff7edab00 is .data in /usr/lib/libcrypto.so.1.1
	0x00007ffff7edab00 - 0x00007ffff7edef48 is .bss in /usr/lib/libcrypto.so.1.1
	0x00007ffff7a19350 - 0x00007ffff7a193a0 is .note.gnu.property in /usr/lib/libc.so.6
	0x00007ffff7a193a0 - 0x00007ffff7a193c4 is .note.gnu.build-id in /usr/lib/libc.so.6
	0x00007ffff7a193c4 - 0x00007ffff7a193e4 is .note.ABI-tag in /usr/lib/libc.so.6
	0x00007ffff7a193e8 - 0x00007ffff7a1db00 is .gnu.hash in /usr/lib/libc.so.6
	0x00007ffff7a1db00 - 0x00007ffff7a2f848 is .dynsym in /usr/lib/libc.so.6
	0x00007ffff7a2f848 - 0x00007ffff7a37843 is .dynstr in /usr/lib/libc.so.6
	0x00007ffff7a37844 - 0x00007ffff7a3900a is .gnu.version in /usr/lib/libc.so.6
	0x00007ffff7a39010 - 0x00007ffff7a39574 is .gnu.version_d in /usr/lib/libc.so.6
	0x00007ffff7a39578 - 0x00007ffff7a395b8 is .gnu.version_r in /usr/lib/libc.so.6
	0x00007ffff7a395b8 - 0x00007ffff7a39fd8 is .rela.dyn in /usr/lib/libc.so.6
	0x00007ffff7a39fd8 - 0x00007ffff7a3a2d8 is .rela.plt in /usr/lib/libc.so.6
	0x00007ffff7a3a2d8 - 0x00007ffff7a3a3f0 is .relr.dyn in /usr/lib/libc.so.6
	0x00007ffff7a3b000 - 0x00007ffff7a3b210 is .plt in /usr/lib/libc.so.6
	0x00007ffff7a3b210 - 0x00007ffff7a3b410 is .plt.sec in /usr/lib/libc.so.6
	0x00007ffff7a3b440 - 0x00007ffff7b9415d is .text in /usr/lib/libc.so.6
	0x00007ffff7b94160 - 0x00007ffff7b95189 is __libc_freeres_fn in /usr/lib/libc.so.6
	0x00007ffff7b96000 - 0x00007ffff7bbba64 is .rodata in /usr/lib/libc.so.6
	0x00007ffff7bbba64 - 0x00007ffff7bbba65 is .stapsdt.base in /usr/lib/libc.so.6
	0x00007ffff7bbba70 - 0x00007ffff7bbba8e is .interp in /usr/lib/libc.so.6
	0x00007ffff7bbba90 - 0x00007ffff7bc2eac is .eh_frame_hdr in /usr/lib/libc.so.6
	0x00007ffff7bc2eb0 - 0x00007ffff7be8630 is .eh_frame in /usr/lib/libc.so.6
	0x00007ffff7be8630 - 0x00007ffff7be8c20 is .gcc_except_table in /usr/lib/libc.so.6
	0x00007ffff7be8c20 - 0x00007ffff7becb98 is .hash in /usr/lib/libc.so.6
	0x00007ffff7bed830 - 0x00007ffff7bed840 is .tdata in /usr/lib/libc.so.6
	0x00007ffff7bed840 - 0x00007ffff7bed8c0 is .tbss in /usr/lib/libc.so.6
	0x00007ffff7bed840 - 0x00007ffff7bed850 is .init_array in /usr/lib/libc.so.6
	0x00007ffff7bed850 - 0x00007ffff7bed938 is __libc_subfreeres in /usr/lib/libc.so.6
	0x00007ffff7bed938 - 0x00007ffff7bed940 is __libc_atexit in /usr/lib/libc.so.6
	0x00007ffff7bed940 - 0x00007ffff7bee6a8 is __libc_IO_vtables in /usr/lib/libc.so.6
	0x00007ffff7bee6c0 - 0x00007ffff7bf0ac0 is .data.rel.ro in /usr/lib/libc.so.6
	0x00007ffff7bf0ac0 - 0x00007ffff7bf0cd0 is .dynamic in /usr/lib/libc.so.6
	0x00007ffff7bf0cd0 - 0x00007ffff7bf0fe8 is .got in /usr/lib/libc.so.6
	0x00007ffff7bf0fe8 - 0x00007ffff7bf1100 is .got.plt in /usr/lib/libc.so.6
	0x00007ffff7bf1100 - 0x00007ffff7bf27a8 is .data in /usr/lib/libc.so.6
	0x00007ffff7bf27c0 - 0x00007ffff7bffe90 is .bss in /usr/lib/libc.so.6
gef➤  
```
Unfortunately this binary had no debugging symbols which is why I ran `info file` to get the entry point. From here I will just output instructions `x` bytes after the program counter `$pc` until I find functions I recognize to set breakpoints.

Run the command `b *0x555555555220` (replace with whatever Entry point you have) in gdb and then run `r` to run the program and stop at the breakpoint.

Now output the next `150` instructions:
```as
gef➤  x/150i $pc
=> 0x555555555220:	endbr64 
   0x555555555224:	xor    ebp,ebp
   0x555555555226:	mov    r9,rdx
   0x555555555229:	pop    rsi
   0x55555555522a:	mov    rdx,rsp
   0x55555555522d:	and    rsp,0xfffffffffffffff0
   0x555555555231:	push   rax
   0x555555555232:	push   rsp
   0x555555555233:	lea    r8,[rip+0x3c6]        # 0x555555555600
   0x55555555523a:	lea    rcx,[rip+0x34f]        # 0x555555555590
   0x555555555241:	lea    rdi,[rip+0xc1]        # 0x555555555309
   0x555555555248:	call   QWORD PTR [rip+0x2d92]        # 0x555555557fe0
   0x55555555524e:	hlt    
   0x55555555524f:	nop
   0x555555555250:	lea    rdi,[rip+0x2db9]        # 0x555555558010
   0x555555555257:	lea    rax,[rip+0x2db2]        # 0x555555558010
   0x55555555525e:	cmp    rax,rdi
   0x555555555261:	je     0x555555555278
   0x555555555263:	mov    rax,QWORD PTR [rip+0x2d7e]        # 0x555555557fe8
   0x55555555526a:	test   rax,rax
   0x55555555526d:	je     0x555555555278
   0x55555555526f:	jmp    rax
   0x555555555271:	nop    DWORD PTR [rax+0x0]
   0x555555555278:	ret    
   0x555555555279:	nop    DWORD PTR [rax+0x0]
   0x555555555280:	lea    rdi,[rip+0x2d89]        # 0x555555558010
   0x555555555287:	lea    rsi,[rip+0x2d82]        # 0x555555558010
   0x55555555528e:	sub    rsi,rdi
   0x555555555291:	mov    rax,rsi
   0x555555555294:	shr    rsi,0x3f
   0x555555555298:	sar    rax,0x3
   0x55555555529c:	add    rsi,rax
   0x55555555529f:	sar    rsi,1
   0x5555555552a2:	je     0x5555555552b8
   0x5555555552a4:	mov    rax,QWORD PTR [rip+0x2d45]        # 0x555555557ff0
   0x5555555552ab:	test   rax,rax
   0x5555555552ae:	je     0x5555555552b8
   0x5555555552b0:	jmp    rax
   0x5555555552b2:	nop    WORD PTR [rax+rax*1+0x0]
   0x5555555552b8:	ret    
   0x5555555552b9:	nop    DWORD PTR [rax+0x0]
   0x5555555552c0:	endbr64 
   0x5555555552c4:	cmp    BYTE PTR [rip+0x2d45],0x0        # 0x555555558010
   0x5555555552cb:	jne    0x5555555552f8
   0x5555555552cd:	push   rbp
   0x5555555552ce:	cmp    QWORD PTR [rip+0x2d22],0x0        # 0x555555557ff8
   0x5555555552d6:	mov    rbp,rsp
   0x5555555552d9:	je     0x5555555552e7
   0x5555555552db:	mov    rdi,QWORD PTR [rip+0x2d26]        # 0x555555558008
   0x5555555552e2:	call   0x555555555120 <__cxa_finalize@plt>
   0x5555555552e7:	call   0x555555555250
   0x5555555552ec:	mov    BYTE PTR [rip+0x2d1d],0x1        # 0x555555558010
   0x5555555552f3:	pop    rbp
   0x5555555552f4:	ret    
   0x5555555552f5:	nop    DWORD PTR [rax]
   0x5555555552f8:	ret    
   0x5555555552f9:	nop    DWORD PTR [rax+0x0]
   0x555555555300:	endbr64 
   0x555555555304:	jmp    0x555555555280
   0x555555555309:	endbr64 
   0x55555555530d:	push   rbp
   0x55555555530e:	mov    rbp,rsp
   0x555555555311:	sub    rsp,0x30
   0x555555555315:	mov    DWORD PTR [rbp-0x24],edi
   0x555555555318:	mov    QWORD PTR [rbp-0x30],rsi
   0x55555555531c:	lea    rsi,[rip+0xce1]        # 0x555555556004
   0x555555555323:	lea    rdi,[rip+0xcdd]        # 0x555555556007
   0x55555555532a:	call   0x555555555190 <fopen@plt>
   0x55555555532f:	mov    QWORD PTR [rip+0x2d1a],rax        # 0x555555558050
   0x555555555336:	mov    rax,QWORD PTR [rip+0x2d13]        # 0x555555558050
   0x55555555533d:	test   rax,rax
   0x555555555340:	jne    0x555555555358
   0x555555555342:	lea    rdi,[rip+0xcc8]        # 0x555555556011
   0x555555555349:	call   0x555555555150 <puts@plt>
   0x55555555534e:	mov    eax,0x0
   0x555555555353:	jmp    0x555555555449
   0x555555555358:	mov    rax,QWORD PTR [rip+0x2cf1]        # 0x555555558050
   0x55555555535f:	mov    edx,0x2
   0x555555555364:	mov    esi,0x0
   0x555555555369:	mov    rdi,rax
   0x55555555536c:	call   0x555555555160 <fseek@plt>
   0x555555555371:	mov    rax,QWORD PTR [rip+0x2cd8]        # 0x555555558050
   0x555555555378:	mov    rdi,rax
   0x55555555537b:	call   0x555555555140 <ftell@plt>
   0x555555555380:	mov    DWORD PTR [rbp-0x14],eax
   0x555555555383:	mov    eax,DWORD PTR [rbp-0x14]
   0x555555555386:	mov    DWORD PTR [rbp-0x10],eax
   0x555555555389:	mov    rax,QWORD PTR [rip+0x2cc0]        # 0x555555558050
   0x555555555390:	mov    edx,0x0
   0x555555555395:	mov    esi,0x0
   0x55555555539a:	mov    rdi,rax
   0x55555555539d:	call   0x555555555160 <fseek@plt>
   0x5555555553a2:	mov    eax,DWORD PTR [rbp-0x10]
   0x5555555553a5:	cdqe   
   0x5555555553a7:	mov    rdi,rax
   0x5555555553aa:	call   0x555555555180 <malloc@plt>
   0x5555555553af:	mov    QWORD PTR [rbp-0x8],rax
   0x5555555553b3:	mov    rdx,QWORD PTR [rip+0x2c96]        # 0x555555558050
   0x5555555553ba:	mov    eax,DWORD PTR [rbp-0x10]
   0x5555555553bd:	movsxd rsi,eax
   0x5555555553c0:	mov    rax,QWORD PTR [rbp-0x8]
   0x5555555553c4:	mov    rcx,rdx
   0x5555555553c7:	mov    edx,0x1
   0x5555555553cc:	mov    rdi,rax
   0x5555555553cf:	call   0x5555555551b0 <fread@plt>
   0x5555555553d4:	mov    rax,QWORD PTR [rip+0x2c75]        # 0x555555558050
   0x5555555553db:	mov    rdi,rax
   0x5555555553de:	call   0x5555555551e0 <fclose@plt>
   0x5555555553e3:	mov    edx,DWORD PTR [rbp-0x10]
   0x5555555553e6:	mov    rax,QWORD PTR [rbp-0x8]
   0x5555555553ea:	mov    esi,edx
   0x5555555553ec:	mov    rdi,rax
   0x5555555553ef:	call   0x55555555544b
   0x5555555553f4:	mov    DWORD PTR [rbp-0xc],eax
   0x5555555553f7:	lea    rsi,[rip+0xc2c]        # 0x55555555602a
   0x5555555553fe:	lea    rdi,[rip+0xc28]        # 0x55555555602d
   0x555555555405:	call   0x555555555190 <fopen@plt>
   0x55555555540a:	mov    QWORD PTR [rip+0x2c0f],rax        # 0x555555558020
   0x555555555411:	mov    rdx,QWORD PTR [rip+0x2c08]        # 0x555555558020
   0x555555555418:	mov    eax,DWORD PTR [rbp-0xc]
   0x55555555541b:	movsxd rsi,eax
   0x55555555541e:	mov    rax,QWORD PTR [rip+0x2c03]        # 0x555555558028
   0x555555555425:	mov    rcx,rdx
   0x555555555428:	mov    edx,0x1
   0x55555555542d:	mov    rdi,rax
   0x555555555430:	call   0x5555555551f0 <fwrite@plt>
   0x555555555435:	mov    rax,QWORD PTR [rip+0x2be4]        # 0x555555558020
   0x55555555543c:	mov    rdi,rax
   0x55555555543f:	call   0x5555555551e0 <fclose@plt>
   0x555555555444:	mov    eax,0x1
   0x555555555449:	leave  
   0x55555555544a:	ret    
   0x55555555544b:	endbr64 
   0x55555555544f:	push   rbp
   0x555555555450:	mov    rbp,rsp
   0x555555555453:	sub    rsp,0x30
   0x555555555457:	mov    QWORD PTR [rbp-0x28],rdi
   0x55555555545b:	mov    DWORD PTR [rbp-0x2c],esi
   0x55555555545e:	mov    rax,QWORD PTR fs:0x28
   0x555555555467:	mov    QWORD PTR [rbp-0x8],rax
   0x55555555546b:	xor    eax,eax
   0x55555555546d:	mov    eax,DWORD PTR [rbp-0x2c]
   0x555555555470:	mov    DWORD PTR [rbp-0x20],eax
   0x555555555473:	mov    edx,0x10
   0x555555555478:	mov    esi,0x0
   0x55555555547d:	lea    rdi,[rip+0x2bbc]        # 0x555555558040
   0x555555555484:	call   0x555555555130 <memset@plt>
   0x555555555489:	mov    eax,DWORD PTR [rbp-0x2c]
   0x55555555548c:	cdqe   
   0x55555555548e:	mov    rdi,rax
```
If we cross refernce the disassembled code in Ghidra we can guess that the call to `0x55555555544b` is where the encryption function is at. Let's set another breakpoint and continue:
```as
gef➤  b *0x55555555544b
Breakpoint 2 at 0x55555555544b
gef➤  c
```

Now lets output the next `100` instructions.
```as
gef➤  x/100i $pc
=> 0x55555555544b:	endbr64 
   0x55555555544f:	push   rbp
   0x555555555450:	mov    rbp,rsp
   0x555555555453:	sub    rsp,0x30
   0x555555555457:	mov    QWORD PTR [rbp-0x28],rdi
   0x55555555545b:	mov    DWORD PTR [rbp-0x2c],esi
   0x55555555545e:	mov    rax,QWORD PTR fs:0x28
   0x555555555467:	mov    QWORD PTR [rbp-0x8],rax
   0x55555555546b:	xor    eax,eax
   0x55555555546d:	mov    eax,DWORD PTR [rbp-0x2c]
   0x555555555470:	mov    DWORD PTR [rbp-0x20],eax
   0x555555555473:	mov    edx,0x10
   0x555555555478:	mov    esi,0x0
   0x55555555547d:	lea    rdi,[rip+0x2bbc]        # 0x555555558040
   0x555555555484:	call   0x555555555130 <memset@plt>
   0x555555555489:	mov    eax,DWORD PTR [rbp-0x2c]
   0x55555555548c:	cdqe   
   0x55555555548e:	mov    rdi,rax
   0x555555555491:	call   0x555555555180 <malloc@plt>
   0x555555555496:	mov    QWORD PTR [rip+0x2b8b],rax        # 0x555555558028
   0x55555555549d:	call   0x5555555551a0 <EVP_CIPHER_CTX_new@plt>
   0x5555555554a2:	mov    QWORD PTR [rbp-0x18],rax
   0x5555555554a6:	call   0x5555555551c0 <EVP_aes_128_cbc@plt>
   0x5555555554ab:	mov    QWORD PTR [rbp-0x10],rax
   0x5555555554af:	mov    eax,0x0
   0x5555555554b4:	call   0x555555555539
   0x5555555554b9:	mov    rsi,QWORD PTR [rbp-0x10]
   0x5555555554bd:	mov    rax,QWORD PTR [rbp-0x18]
   0x5555555554c1:	lea    rcx,[rip+0x2b78]        # 0x555555558040
   0x5555555554c8:	lea    rdx,[rip+0x2b61]        # 0x555555558030
   0x5555555554cf:	mov    rdi,rax
   0x5555555554d2:	call   0x555555555170 <EVP_EncryptInit@plt>
   0x5555555554d7:	mov    rsi,QWORD PTR [rip+0x2b4a]        # 0x555555558028
   0x5555555554de:	mov    edi,DWORD PTR [rbp-0x2c]
   0x5555555554e1:	mov    rcx,QWORD PTR [rbp-0x28]
   0x5555555554e5:	lea    rdx,[rbp-0x20]
   0x5555555554e9:	mov    rax,QWORD PTR [rbp-0x18]
   0x5555555554ed:	mov    r8d,edi
   0x5555555554f0:	mov    rdi,rax
   0x5555555554f3:	call   0x555555555210 <EVP_EncryptUpdate@plt>
   0x5555555554f8:	mov    rdx,QWORD PTR [rip+0x2b29]        # 0x555555558028
   0x5555555554ff:	mov    eax,DWORD PTR [rbp-0x20]
   0x555555555502:	cdqe   
   0x555555555504:	lea    rcx,[rdx+rax*1]
   0x555555555508:	lea    rdx,[rbp-0x1c]
   0x55555555550c:	mov    rax,QWORD PTR [rbp-0x18]
   0x555555555510:	mov    rsi,rcx
   0x555555555513:	mov    rdi,rax
   0x555555555516:	call   0x555555555200 <EVP_EncryptFinal_ex@plt>
   0x55555555551b:	mov    edx,DWORD PTR [rbp-0x20]
   0x55555555551e:	mov    eax,DWORD PTR [rbp-0x1c]
   0x555555555521:	add    eax,edx
   0x555555555523:	mov    rcx,QWORD PTR [rbp-0x8]
   0x555555555527:	xor    rcx,QWORD PTR fs:0x28
   0x555555555530:	je     0x555555555537
   0x555555555532:	call   0x5555555551d0 <__stack_chk_fail@plt>
   0x555555555537:	leave  
   0x555555555538:	ret    
   0x555555555539:	endbr64 
   0x55555555553d:	push   rbp
   0x55555555553e:	mov    rbp,rsp
   0x555555555541:	mov    DWORD PTR [rbp-0x4],0x0
   0x555555555548:	jmp    0x555555555584
   0x55555555554a:	cmp    DWORD PTR [rbp-0x4],0x0
   0x55555555554e:	jne    0x555555555559
   0x555555555550:	mov    DWORD PTR [rbp-0x8],0x27e2
   0x555555555557:	jmp    0x55555555556c
   0x555555555559:	mov    edx,DWORD PTR [rbp-0x4]
   0x55555555555c:	mov    eax,DWORD PTR [rbp-0x8]
   0x55555555555f:	add    eax,edx
   0x555555555561:	shl    eax,0x2
   0x555555555564:	xor    eax,0x29fa
   0x555555555569:	mov    DWORD PTR [rbp-0x8],eax
   0x55555555556c:	mov    eax,DWORD PTR [rbp-0x4]
   0x55555555556f:	cdqe   
   0x555555555571:	lea    rdx,[rip+0x2ab8]        # 0x555555558030
   0x555555555578:	add    rax,rdx
   0x55555555557b:	mov    edx,DWORD PTR [rbp-0x8]
   0x55555555557e:	mov    BYTE PTR [rax],dl
   0x555555555580:	add    DWORD PTR [rbp-0x4],0x1
   0x555555555584:	cmp    DWORD PTR [rbp-0x4],0xf
   0x555555555588:	jle    0x55555555554a
   0x55555555558a:	nop
   0x55555555558b:	nop
   0x55555555558c:	pop    rbp
   0x55555555558d:	ret    
   0x55555555558e:	xchg   ax,ax
   0x555555555590:	endbr64 
   0x555555555594:	push   r15
   0x555555555596:	lea    r15,[rip+0x279b]        # 0x555555557d38
   0x55555555559d:	push   r14
   0x55555555559f:	mov    r14,rdx
   0x5555555555a2:	push   r13
   0x5555555555a4:	mov    r13,rsi
   0x5555555555a7:	push   r12
   0x5555555555a9:	mov    r12d,edi
   0x5555555555ac:	push   rbp
   0x5555555555ad:	lea    rbp,[rip+0x278c]        # 0x555555557d40
   0x5555555555b4:	push   rbx
   0x5555555555b5:	sub    rbp,r15
```

Great, now we see the call to `EVP_EncryptInit` at address `0x5555555554d2`. From reading the documentation we know the key will be the 3rd argument in the call to this function. If we set a breakpoint at `0x5555555554d2` we can analyze the arguments that will be passed.
```as
gef➤  b *0x5555555554d2
Breakpoint 3 at 0x5555555554d2
gef➤  c
...
●→ 0x5555555554d2                  call   0x555555555170 <EVP_EncryptInit@plt>
   ↳  0x555555555170 <EVP_EncryptInit@plt+0> endbr64 
      0x555555555174 <EVP_EncryptInit@plt+4> bnd    jmp QWORD PTR [rip+0x2e05]        # 0x555555557f80 <EVP_EncryptInit@got.plt>
      0x55555555517b <EVP_EncryptInit@plt+11> nop    DWORD PTR [rax+rax*1+0x0]
      0x555555555180 <malloc@plt+0>   endbr64 
      0x555555555184 <malloc@plt+4>   bnd    jmp QWORD PTR [rip+0x2dfd]        # 0x555555557f88 <malloc@got.plt>
      0x55555555518b <malloc@plt+11>  nop    DWORD PTR [rax+rax*1+0x0]
──────────────────────────────────────────────────────────────────────────────────────────────────────────── arguments (guessed) ────
EVP_EncryptInit@plt (
   $rdi = 0x005555555594b0 → 0x0000000000000000,
   $rsi = 0x007ffff7ebb580 → 0x00000010000001a3,
   $rdx = 0x00555555558030 →  loop 0x5555555580a8,
   $rcx = 0x00555555558040 →  add BYTE PTR [rax], al
)
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "program", stopped 0x5555555554d2 in ?? (), reason: BREAKPOINT
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555554d2 → call 0x555555555170 <EVP_EncryptInit@plt>
[#1] 0x5555555553f4 → mov DWORD PTR [rbp-0xc], eax
[#2] 0x7ffff7a3c290 → mov edi, eax
[#3] 0x7ffff7a3c34a → __libc_start_main()
[#4] 0x55555555524e → hlt 
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤ 
```
I am using an extension called GEF in gdb which shows me this additional info such as the function arguments. If this wasn't available we could still get the third argument based on the [x64 calling convention in Linux](https://www.ired.team/miscellaneous-reversing-forensics/windows-kernel-internals/linux-x64-calling-convention-stack-frame). This lets us know the third argument of a function call is stored in `$rdx`

We know from before that the key will be 16 bytes long, so lets output 16 bytes of data from the `$rdx` register.
```as
gef➤  x/16xb $rdx
0x555555558030:	0xe2	0x76	0x1a	0x8e	0xb2	0x26	0x4a	0xbe
0x555555558038:	0xe2	0x56	0x7a	0xee	0x12	0x86	0xaa	0x1e
```

If we clean this formatting up we get the hex representation of the key as `e2761a8eb2264abee2567aee1286aa1e`

Before we get into decryption let's get the contents of the `ct.enc` file. Since it is stored as raw bytes I will output it in base64 format and decode it in my code.
```bash
user@arch:~/cyber/ctf/nahamcon-2022/rick$ base64 ct.enc 
pNUmvTZxrIlgqNwa3IVysgB6lG/ZcfQcXhVsMeugJxV62P61P5KHC0OjpsV7SF2aguTRGhbbp/uX
qa03+zTHCpem5pzZQVh8et/BvOWRE6LGyhE9EfrzK90vdjewhHDtbavPMa35YKi03cscIt8bMkZT
rUHq7f2qELPmXr5a7lKdLbPwWrh96zqBMSQJ7QJorF6Rv1F1YpQVIXI/LYJzpZizDukOAPBLdxFr
YBj+Ndch/rihIMLHayg/MFcKlpLQ3rQX6qwKmJv21Gu51BWqFkUJMfhpUWeG7bB9AgUdCI+ecpqF
9fHM34TkdSKzKCmbffq/0ZkxGZZgqrpV3wnZZKCvgGtVUh9c1LKB4bWenUnjyB5275pGCSLMUk7V
Wo9q
```

Now we have everything we need to decrypt the text. I write this script to handle the AES decryption and print the flag:
```python
from Crypto.Cipher import AES
import base64

key = bytes.fromhex("e2761a8eb2264abee2567aee1286aa1e")

ct = base64.b64decode("pNUmvTZxrIlgqNwa3IVysgB6lG/ZcfQcXhVsMeugJxV62P61P5KHC0OjpsV7SF2aguTRGhbbp/uX\
qa03+zTHCpem5pzZQVh8et/BvOWRE6LGyhE9EfrzK90vdjewhHDtbavPMa35YKi03cscIt8bMkZT\
rUHq7f2qELPmXr5a7lKdLbPwWrh96zqBMSQJ7QJorF6Rv1F1YpQVIXI/LYJzpZizDukOAPBLdxFr\
YBj+Ndch/rihIMLHayg/MFcKlpLQ3rQX6qwKmJv21Gu51BWqFkUJMfhpUWeG7bB9AgUdCI+ecpqF\
9fHM34TkdSKzKCmbffq/0ZkxGZZgqrpV3wnZZKCvgGtVUh9c1LKB4bWenUnjyB5275pGCSLMUk7V\
Wo9q")

aes = AES.new(key, AES.MODE_CBC)
pt = aes.decrypt(ct)
print(pt)
```

## Flag
```
flag{6265a883a2d001d4fe291277bb171bac}
```