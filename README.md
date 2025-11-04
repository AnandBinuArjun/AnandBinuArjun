```bash
anand@cyberprofile:~$ cat /etc/os-release
PRETTY_NAME="GitHub Ubuntu 20.04.6 LTS"
NAME="Ubuntu"
VERSION_ID="20.04"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://github.com/AnandBinuArjun"
SUPPORT_URL="https://github.com/AnandBinuArjun"
BUG_REPORT_URL="https://github.com/AnandBinuArjun"

anand@cyberprofile:~$ whoami
anand

anand@cyberprofile:~$ id
uid=1000(anand) gid=1000(anand) groups=1000(anand),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lxd)

anand@cyberprofile:~$ echo $SHELL
/bin/bash

anand@cyberprofile:~$ uname -a
Linux cyberprofile 5.4.0-1097-aws #104~18.04.1-Ubuntu SMP x86_64 GNU/Linux

anand@cyberprofile:~$ pwd
/home/anand

anand@cyberprofile:~$ ls -la
total 56
drwxr-xr-x 1 anand anand  4096 Nov  4 15:30 .
drwxr-xr-x 1 root  root   4096 Nov  4 15:30 ..
-rw-r--r-- 1 anand anand  3771 Nov  4 15:30 .bashrc
drwx------ 1 anand anand  4096 Nov  4 15:30 .cache
drwx------ 1 anand anand  4096 Nov  4 15:30 .config
drwxr-xr-x 1 anand anand  4096 Nov  4 15:30 .local
-rw-r--r-- 1 anand anand   807 Nov  4 15:30 .profile
drwxr-xr-x 1 anand anand  4096 Nov  4 15:30 Projects
-rw-r--r-- 1 anand anand  1234 Nov  4 15:30 README.md
drwx------ 1 anand anand  4096 Nov  4 15:30 .ssh

anand@cyberprofile:~$ cat /proc/cpuinfo | grep "model name" | head -1
model name      : AMD EPYC 7763 64-Core Processor

anand@cyberprofile:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:           30Gi       2.0Gi        25Gi       128Mi       3.0Gi        28Gi
Swap:         2.0Gi          0B       2.0Gi

anand@cyberprofile:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        96G   12G   84G  13% /
tmpfs            16G     0   16G   0% /dev/shm
/dev/nvme0n1p1  492M  4.0K  492M   1% /boot/efi

anand@cyberprofile:~$ ps aux | grep anand | head -5
anand     1234  0.0  0.0  12345  6789 ?        S    15:30   0:00 /bin/bash
anand     1235  0.0  0.0  23456  7890 ?        S    15:30   0:00 /usr/bin/python3
anand     1236  0.0  0.0  34567  8901 ?        S    15:30   0:00 /usr/bin/node
anand     1237  0.0  0.0  45678  9012 ?        S    15:30   0:00 /usr/bin/docker
anand     1238  0.0  0.0  56789  0123 ?        S    15:30   0:00 /usr/bin/git

anand@cyberprofile:~$ cat /etc/passwd | grep anand
anand:x:1000:1000:Anand Binu Arjun,,,:/home/anand:/bin/bash

anand@cyberprofile:~$ groups anand
anand : anand adm cdrom sudo dip plugdev lxd

anand@cyberprofile:~$ cat ~/.profile
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

echo "Welcome to Anand's Cybersecurity Profile!"
echo "MSc Cyber Security @ Birmingham City University"

anand@cyberprofile:~$ cat ~/Projects/README.md

# Anand Binu Arjun 👨‍💻

## System Information
┌────────────────────────────────────────────────────────────────────┐
│  ██████╗ ██╗   ██╗██████╗  █████╗ ███╗   ██╗██████╗               │
│  ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗████╗  ██║██╔══██╗              │
│  ██████╔╝ ╚████╔╝ ██████╔╝███████║██╔██╗ ██║██║  ██║              │
│  ██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║              │
│  ██████╔╝   ██║   ██║     ██║  ██║██║ ╚████║██████╔╝              │
│  ╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝               │
│                                                                   │
│  Name: Anand Binu Arjun                                           │
│  Title: Cybersecurity Specialist                                  │
│  Location: India                                                  │
│  Education: MSc Cyber Security @ Birmingham City University       │
│  Specialization: ML-Driven Intrusion Detection                    │
│  Languages: Python, JavaScript                                    │
│  Technologies: Machine Learning, Network Security, Discord Bots  │
│  Tools: Docker, Git, Linux                                        │
│  Terminal: Bash                                                   │
│  Shell: zsh 5.8                                                   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

## Active Projects
• Security Assistant - Next-Gen Discord Bot for Cybersecurity
• IDS_ML - Machine Learning Project for Network Intrusion Detection

## Contact Information
📧 Email: [your.email@example.com](mailto:your.email@example.com)
💼 LinkedIn: [linkedin.com/in/anand-b-arjun](https://linkedin.com/in/anand-b-arjun)
🌐 GitHub: [github.com/AnandBinuArjun](https://github.com/AnandBinuArjun)

## System Status
uptime: 24/7 Learning Mode - Continuous Improvement in Cybersecurity

anand@cyberprofile:~$ history | tail -5
 1230  whoami
 1231  ls -la
 1232  cat /proc/cpuinfo
 1233  ps aux | grep anand
 1234  cat ~/Projects/README.md

anand@cyberprofile:~$ echo "Happy Coding!" && exit 0
Happy Coding!
```
