# Samba Share

1. `sudo apt install samba`
2. Add the following to `/etc/samba/smb.conf`

```console
$ cat /etc/samba/smb.conf 
[global]
        log file = /var/log/samba/%m
        log level = 1
        server role = standalone server

[pishare]
        path = /mnt/PiShare
        read only = no
        inherit permissions = yes
```

3. Create a user to access the server:
NOTE that this may not be needed

```console
$ sudo useradd -M -s /sbin/nologin pishareUser
o sudo passwd pishareUser
$ sudo smbpasswd -a pishareUser
```

4. Add access (probably just double checking)
```console
$ sudo chgrp -R users /mnt/PiShare/
```

5. Test access (you can do this from any linux machine)

```console
$ smbclient -U pi //192.168.1.5/pishare
```

`-U` is the user the server is set up to accept, and then you pass the share's IP
