# padlock

## Description
Author: @birch#9901

I forgot the combination to my pad lock :(

Download the file below.
Attachments: [padlock](https://ctf.nahamcon.com/files/a70c2a24990246d49713b7c75e12333e/padlock?token=eyJ1c2VyX2lkIjoxNDI1LCJ0ZWFtX2lkIjo3NzUsImZpbGVfaWQiOjEwfQ.Y50ivg.fMh2raCfRhFN-mTNoOPYgxH4Mso)

## Solve
Running the file asks us for a code:
```
user@arch:~/cyber/ctf/nahamcon-2022/padlock$
     .--------.
    / .------. \
   / /        \ \
   | |        | |
  _| |________| |_
.' |_|        |_| '.
'._____ ____ _____.'
|     .'____'.     |
'.__.'.'    '.'.__.'
'.__  | ???? |  __.'
|   '.'.____.'.'   |
'.____'.____.'____.'
'.________________.'
Please enter the passcode: 1234
The passcode you entered was: 1234
```

Opening the file in Ghidra gives us a better idea of the program's logic:
```c

undefined8
main(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,undefined8 param_5,
    undefined8 param_6)

{
  int iVar1;
  size_t sVar2;
  long in_FS_OFFSET;
  char guess [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  print_lock(0x3f,0x3f,0x3f,0x3f,param_5,param_6,param_2);
  printf("Please enter the passcode: ");
  __isoc99_fscanf(stdin,&DAT_00102129,guess);
  printf("The passcode you entered was: %s\n",guess);
  replace(guess,L'3',L'e');
  replace(guess,L'_',L' ');
  replace(guess,L'0',L'o');
  replace(guess,L'4',L'a');
  sVar2 = strlen(guess);
  if (sVar2 == 0x26) {
    iVar1 = strcmp("master locks arent vry strong are they",guess);
    if (iVar1 == 0) {
      replace(guess,L'e',L'3');
      replace(guess,L' ',L'_');
      replace(guess,L'o',L'0');
      replace(guess,L'a',L'4');
      unlock(guess);
    }
  }
  else {
    printf("Not quite!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

The program will read our input into a buffer via `scanf()` and then preform replacements on it before checking that the length is 38 chars comparing it to the string `master locks arent vry strong are they`.

The `replace()` function will replace `3` with `e`, `_` with ` `, `0` with `o`, and `4` with `a`. You might be thinking "why can't we just pass the correct string as input?". The reason for this is because `scanf()` ends our string once it hits a whitespace.

So to solve this we need to substitute the characters and the program will make its replacements, compare the strings, and give us our flag.
```
user@arch:~$ python
Python 3.10.8 (main, Nov  1 2022, 14:18:21) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> key = "master locks arent vry strong are they"
>>> key.replace('e', '3').replace(' ', '_').replace('o', '0').replace('a', '4')
'm4st3r_l0cks_4r3nt_vry_str0ng_4r3_th3y'
```
Now let's enter this into the program:
```
user@arch:~/cyber/ctf/nahamcon-2022/padlock$ ./padlock 
     .--------.
    / .------. \
   / /        \ \
   | |        | |
  _| |________| |_
.' |_|        |_| '.
'._____ ____ _____.'
|     .'____'.     |
'.__.'.'    '.'.__.'
'.__  | ???? |  __.'
|   '.'.____.'.'   |
'.____'.____.'____.'
'.________________.'
Please enter the passcode: m4st3r_l0cks_4r3nt_vry_str0ng_4r3_th3y
The passcode you entered was: m4st3r_l0cks_4r3nt_vry_str0ng_4r3_th3y
flag{264cec034faef71c642de1721ea26b1f}
```

## Flag
```
flag{264cec034faef71c642de1721ea26b1f}
```