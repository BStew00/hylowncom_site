---
title: Remote Git Server -- Homelab | Hylown
html_template: homelab/hylowncom_homelab.html
id_to_make_active: RemoteGitServer
source: true
---

# Setup Git on a remote server

### *A personal, private Git server on a secure, remote machine* {: class="subtitle" }

## Features {: class="template__section" }

* Encrypted read & write to/from the server via SSH
* Web interface via gitweb and its functionalities -- already installed by web host provider

## Machine {: class="template__section" }

* Local: Windows 11 & Raspberry Pi 5 (with Raspberry Pi OS Debian 12 Bookworm) local machines
* Remote: 
  * Web host provider: Bluehost
    * Hosting plan: WordPress Plus Hosting
  * Hosting platform: cPanel
  * OS: Red Hat 4.8.5-44

### Software used {: class="template__section" }

* cPanel Terminal
* git (already installed on server by cPanel; on Windows: git, including Git Bash; on Debian: git)
* gitweb (already installed on server by cPanel)
* Linux utilities (likely already installed): keygen, nano

## On local machines (using Git Bash in Windows) {: class="template__section" }

```bash
cd # start at user home dir, e.g. /c/Users/junkb
ssh-keygen -o # allow to place keys in default dir; no passkey, i.e. hit enter twice
cat ~/.ssh/id_ed25519.pub # or whatever name it was given; use PUBLIC key
```
Then copy contents of the public key file into the clipboard.

## On the remote server
```bash
touch ~/.ssh/tmp id_ed25519.win1.pub # a temp file to hold key
nano ~/.ssh/tmp id_ed25519.win1.pub
```
Then paste contents of the public key file; make sure it is all one line, should look something like this:
```bash
ssh-ed25519 AAAACTHEQUICKBROWNFOXHELLOTHEREaThISALOOONGSTRINGust junkb@DESKTOP-3ICM930
```
Add the public key to the `authorized_keys` file:
```bash
cat ~/.ssh/tmp/id_ed25519.win1.pub >> ~/.ssh/authorized_keys
```
Create a bare repo:
```bash
cd ~/git/repos
mkdir project.git # the repo's dir name should end in .git
cd project.git
git init --bare
```
## On a local machine  {: class="template__section" }

### Push an existing repo to the new repo

An existing repo should first be pushed to the new repo on the server; this is why we add a `readme.md` file:
```bash
mkdir ~/Desktop/temp/myproject
cd ~/Desktop/temp/myproject
git init
touch readme.md # so the repo is not empty
git add .
git commit -m 'hello'
git remote add origin hylownco@hylown.com:git/repos/project.git
git push origin master
```
Now other users can clone the repo; here we do it in another project on the same Windows machine:
```bash
cd ~/Desktop/temp
git clone hylownco@hylown.com:git/repos/project.git
```
Now we can make changes and push to the server repo:
```bash
cd project # this is the name given from the clone of project.git
nano readme.md
# add text
git add .
git commit -m 'changed readme.md in cloned repo'
git push origin master
```
Now other users can pull these changes; again here we do it in another repo on the same Windows machine:
```bash
mkdir ~/Desktop/temp/myproject
cd ~/Desktop/temp/myproject
git init
git remote add origin hylownco@hylown.com:git/repos/project.git
git pull origin master
```
Note that another format can be used with the SSH protocol:
```bash
ssh://hylownco@hylown.com/home3/hylownco/git/repos/project.git
```

## On the remote server {: class="template__section" }

Note: the above works at first; I'm not sure what breaks it, but after making some small changes and trying to push back again, I was getting this:

```bash
$ git push origin master
fatal: bad config value for 'receive.denycurrentbranch' in config
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

An internet search of "git ssh bad config value for 'receive.denycurrentbranch' in config" led me to:

https://stackoverflow.com/questions/56990207/fatal-bad-config-value-for-receive-denycurrentbranch-in-config

Following this answer worked for me; git is in exaclty the same location on my server as in this answer, so running this exactly as in the answer on my server worked perfectly:

> I also got the same issue. When I run the command git --version it shows 2.24.1 but it wasn't accepting 
> updateInstead as mentioned in the above question.
> 
> I did this to solve this issue:
> 
> Run this command.
>
> ```bash
> which git
> ```
>
> It will give you the path of git.
> 
> Example output
> 
> ```bash
> /usr/local/cpanel/3rdparty/lib/path-bin/git
> ```
>
> Go to ```~/.bashrc``` file and add this code to the bottom of the file
>
> ```bash
> export PATH=/usr/local/cpanel/3rdparty/lib/path-bin:$PATH
> ```
>
> *Note that I am not including git at the end of the path.
> 
> Hope this solves the issue.


