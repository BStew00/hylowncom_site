---
title: Local Git Server -- Homelab | Hylown
html_template: homelab/hylowncom_homelab.html
id_to_make_active: LocalGitServer
source: true
---

# Setup a Home Git Server
### *Your own personal, private Git server in your home!* {: class="subtitle" }


![](../../assets/git_server.jpg){: width=612 height=262}


## Features {: class="template__section" }

A local, private, free git server.

HTTP acces to Gitweb interface in a web browser; local use of ```gitk``` and ```git-gui``` graphical interfaces that are bundled with git.

HTTP access can be either authenticated (requires username and password), or unauthenticated.

Git repositories can be stored on the server somewhere having a long path name, e.g. ```/mnt/my-raid/www/git/repos```, but accessed with a shorter path, e.g. ```/git```, by using a symbolic link.

The HTTP URL usage is a lot like using GitHub or GitLab.

Can also fully interact with the git server using SSH (slightly more complicated URL) without a password.

Do not need to enter the server to create new repos. Can either use passwordless-SSH, or a PHP form over HTTP in a web browser.

The PHP form sanitizes the input, returns a message if the repo name is already used on the server, and returns an error message if the wrong format has been given for the repo name.





## Machines {: class="template__section" }

### Server

A Raspberry Pi 5 8Gb machine having:

* Raspberry Pi Lite OS (Debian Bookworm)
* RAID storage

### Clients

Local machines running one of:

* Raspberry Pi OS
* Windows 11
* MacOS





## Software used {: class="template__section" }

* NGINX
* Git
* Gitweb
* fcgiwrap
* apache2-utils
* PHP-FPM









## Minimal config {: class="template__section" }

Note both sytem and global configs:

```bash
$ git config --global user.name "<user>"
$ git config --global user.email <email address>

$ git config --system init.defaultBranch master
```

## Repo root {: class="template__section" }

Create and configure a directory to house repositories.

I used ```/mnt/raid10/git``` as ```<repo-root>```.

We make the git root directory, ```<repo-root>```, user and group the same as needed for using the HTML interface, and give this useer and group full permissions, but others only read and execute permissions.

```bash
$ sudo mkdir <repo-root>
$ sudo chown -R www-data:www-data <repo-root>
$ sudo chmod -R 775  <repo-root>
```

Give it a shorter symbolic link.

```bash
$ sudo ln -s <repo-root> /git
```

Do NOT do ```mkdir /git``` first, just run the ```ln -s``` command.









## Gitweb Config {: class="template__section" }

I used:

 ```<repo-root> = /mnt/raid10/git```

In the gitweb config file

```bash
/etc/gitweb.conf
```

change the value of `$projectroot`

```bash
# path to git projects (<project>.git)
#$projectroot = "/var/lib/git";
$projectroot = "<repo-root>";
```

Contents of this file before our major, final reinstall:

```bash
pis@radxahost:~ $ cat /etc/gitweb.conf
# path to git projects (<project>.git)
#$projectroot = "/var/lib/git";
#$projectroot = "/var/www/html/git";
$projectroot = "/mnt/raid1/git";

# directory to use for temp files
$git_temp = "/tmp";

# target of the home link on top of all pages
#$home_link = $my_uri || "/";

# html text to include at home page
#$home_text = "indextext.html";

# file with project list; by default, simply scan the projectroot dir.
#$projects_list = $projectroot;

# stylesheet to use
#@stylesheets = ("static/gitweb.css");
#@stylesheets = ("/usr/share/gitweb/static/gitweb.css");

# javascript code for gitweb
#$javascript = "static/gitweb.js";
#$javascript = "/usr/share/gitweb/static/gitweb.js";

# logo to use
#$logo = "static/git-logo.png";
#$logo = "/usr/share/gitweb/static/git.logo.png";

# the 'favicon'
#$favicon = "static/git-favicon.png";
#$favicon = "/usr/share/gitweb/static/git-favicon.png";

# git-diff-tree(1) options to use for generated patches
#@diff_opts = ("-M");
@diff_opts = ();
```









## Creating a new repo {: class="template__section" }

I used:

```
<repo-root> = /mnt/raid10/git
<gitweb-root> = /usr/share/gitweb which I believe is the default for Gitweb.
<hostname> = intra
```

## SSH without a password {: class="template__section" }

Since we already setup SSH without a password, we can do this:

```bash
$ ssh user@server git init --bare <project>.git
```

e.g.

```
$ ssh [user@]<hostname> git init --bare --share /path/to/project.git
```








## HTTP/PHP Form {: class="template__section" }

Here we create a PHP form accessed at ```http://<hostname>.local/newrepo``` that can be used to create a new repo over the LAN.

Ref: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Nginx-PHP-FPM-config-example

If not already installed, install PHP **fpm** version and restart NGINX:

```bash
$ sudo apt-get install php8.2-fpm -y
$ sudo systemctl restart nginx
```

Create and configure the following directory:

```bash
$ mkdir <gitweb-root>/newrepo

$ chown -R www-data:www-data <gitweb-root>/newrepo

$ chmod -R 755 <gitweb-root>/newrepo
```

Create a bash script ```<gitweb-root>/newrepo/create_repo.sh``` with the following contents:

```bash
#!/usr/bin/env bash

mkdir /mnt/raid10/git/$1.git

cd /mnt/raid10/git/$1.git

git init --bare --share=group

git update-server-info

chgrp -R www-data .
chmod -R g+rw .
find -type d -exec chmod g+s {} +
```

and configure it to be executable:

```bash
$ chmod +x <gitweb-root>/newrepo/create_repo.sh
```

and make sure all SSH users are in the ```www-data``` group, e.g. do

```bash
$ sudo usermod -a -G www-data <git-user>
```

for each git user.

Create a php file ```<gitweb-root>/newrepo/index.php``` with the following contents:

```php
<!DOCTYPE HTML>
<html>
  <head>
    <title>Create New Repository</title>
  </head>
  <body>
    <?php
      session_start();
    ?>
    <a href="/">Return to Home Page</a>
    <h3>Create a New Repository</h3>
    <form method="post" action="/newrepo/newrepoexe.php">
      Name: <input type="text" name="name">
      <input type="submit" name="submit" value="Create Repo">
    </form>
    <?php
      echo "<br><br>";
      if($_SESSION['name_submitted'] != ""){
        print_r($_SESSION['output']);
      }
      $_SESSION['name_submitted'] = "";
    ?>
  </body>
</html>
```

and another php file ```<gitweb-root>/newrepo/newrepoexe.php``` with the following contents:

```php
<?php
  session_start();
  function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
  }
  $name = test_input($_POST["name"]);
  $_SESSION['name_submitted'] = $name;
  $_SESSION['output'] = null;
  $_SESSION['retval'] = null;
  $correct_format = preg_match("/^[A-Za-z0-9_-]+$/", $name);
  $existing_repos = file_get_contents('http://<hostname>.local/index.cgi?a=project_index');
  $is_in_existing_repo_list = preg_match("/" . $name . ".git" . "/i" , $existing_repos);
  if ($correct_format & !$is_in_existing_repo_list) {
      exec("/usr/share/gitweb/newrepo/create_repo.sh $name 2>&1", $output, $retval);
  }
  if(!$correct_format){
      $output = 'Name: ' . $name . '<br>Error: repo name can only include letters, numbers, underscores, and dashes.';
      $retval = 1;
  }
  if($is_in_existing_repo_list){
      $output = 'Error: a repo named ' . $name . ' already exists.';
      $retval = 1;
  }
  $_SESSION['output'] = $output;
  $_SESSION['retval'] = $retval;
  header("Location: /newrepo/index.php");
?>
```

You should now be able to go to 

```http://<hostname>.local/newrepo```

in a web browser on a machine on the same network and use the form to create a new repo.

Any new repos made with this form should show up on the gitweb homepage.





## Finalize {: class="template__section" }

After a repo has been created on the server with either method above, it is necessary to push a non-empty repo to it before doing any cloning or pulling from it. 

We do this from another machine using either an existing repo or making a minimal non-empty repo:

```bash
$ mkdir ~/testproject
$ cd ~/testproject
$ git init
$ git remote add origin http://<hostname>.local/git/<project-name>.git
$ touch README.md
$ git add .
$ git commit -a -m "some message"
$ git push origin master
```









## Using a repo {: class="template__section" }

After a **_non-empty_** project has been pushed to a new repo on the server, other users can clone or pull it.

```bash
$ git clone http://<hostname>.local/git/<project>.git
```

```bash
$ mkdir ~/testproject
$ cd ~/testproject
$ git init
$ git remote add origin http://<hostname>.local/git/<project>.git
$ git pull origin master
```

Note that on Windows it might work better to use the user-URL like:

```bash
$ git clone http://<user>@<hostname>.local/git/<project-name>.git
# or 
$ mkdir ~/testproject
$ cd ~/testproject
$ git init
$ git remote add origin http://<user>@<hostname>.local/git/<project>.git
$ git pull origin master
```



