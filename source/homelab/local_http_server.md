---
title: Local HTTP Server -- Homelab | Hylown
html_template: homelab/hylowncom_homelab.html
id_to_make_active: LocalHTTPServer
source: true
---

# Setup a Home HTTP Server

### *Start your own intranet* {: class="subtitle" }

## Installation {: class="template__section" }

If apache is installed then either stop it

```bash
$ sudo systemctl stop apache2
```

or remove it.

```bash
$ sudo apt purge apache2
```

Update the machine:

```bash
$ sudo apt update && sudo apt full-upgrade
```

Install necessary packages:

```bash
$ sudo apt-get install nginx git gitweb nano fcgiwrap apache2-utils php8.2-fpm -y
```

Note: we're including git & gitweb here because this machine will also be a Git server.  

After installing NGINX you should be able to view its welcome page by entering either ```<hostname>.local``` or ```<ip-address>``` in the address bar of a web browser on another machine on the network.  

We're actually going to be setting up multiple intranet websites in addition to the Git server.  So let's change this homepage.

Make a copy of the original NGINX file.  This is optional, but good practice.  

```bash
$ cd /var/www/html
$ cp index.nginx-debian.html index.nginx-debian.html.original
```

Then open the file

```bash
$ sudo nano index.nginx-debian.html
```

and make its contents the following:

```html
<!DOCTYPE html>
<html>
<head>
<title> Git Server</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to Our Git Server Homepage!</h1>
<p><a href="http://<hostname>.local/gitweb">Gitweb</a></p>

<p><a href="http://<hostname>.local/newrepo">Make a new repo</a></p>

<p><em>Thank you for supporting me in this project!</em></p>
</body>
</html>
```

where ```<hostname>``` is the hostname of the server.  









## NGINX Config {: class="template__section" }

I used:

```
<repo-root> = /mnt/raid5/git
<gitweb-root> = /usr/share/gitweb/  which I believe is the default for Gitweb. 
<hostname> = the hostname of your server
```

Make a backup copy of the original NGINX config file:

```bash
$ cd /etc/nginx/sites-available
$ cp default default.original
```

Configure NGINX by editing the following file

```bash
$ sudo nano /etc/nginx/sites-available/default
```

and making its contents the following:

```bash
server {
    listen 80;
    server_name <hostname>.local;

    location ~ ^/git(/.*) {
#        auth_basic "Restricted";
#        auth_basic_user_file "<repo-root>/htpasswd";
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
        fastcgi_param GIT_HTTP_EXPORT_ALL "";
        fastcgi_param GIT_PROJECT_ROOT <repo-root>;
        fastcgi_param PATH_INFO $1;
    }

    location /newrepo {
        root <gitweb-root>;
        index index.php;
    }

    location ~ \.php$ {
        root <gitweb-root>;
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    }

     # deny access to Apache .htaccess on Nginx with PHP, 
     # if Apache and Nginx document roots concur
    location ~ /git/\.ht {
        deny all;
    }

    location /index.cgi {
        root <gitweb-root>;
        include fastcgi_params;
        gzip off;
        fastcgi_param SCRIPT_NAME $uri;
        fastcgi_param GITWEB_CONFIG /etc/gitweb.conf;
        fastcgi_pass  unix:/var/run/fcgiwrap.socket;
    }
# need to add symbolic link to the static dir
# sudo ln -s <gitweb-root>/static /var/www/html/static


    location /gitweb {
        return 301 /index.cgi;
    }

    location / {
        root /var/www/html;
        index index.html index.htm index.php index.cgi index.nginx-debian.html;
    }

}
```

Run the NGINX test command ...

```bash
$ sudo nginx -t
```

... and you should see something like this

```console
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

If you do see errors, go back into the configuration file above and make sure each of the things being pointed to exist in the correct locations.  

Here's a list of all the directories and files used:

```bash
/var/run/fcgiwrap.socket
/etc/nginx/fastcgi_params
/usr/lib/git-core/git-http-backend
/etc/nginx/snippets/fastcgi-php.conf
/run/php/php8.2-fpm.sock
/etc/gitweb.conf
```











If you wish to require username and password for HTTP access, then uncomment the two ```auth_basic``` lines in the NGINX config, create a user 

```bash
$ sudo adduser gitusera
```

and put a password in the proper location:

```bash

$ sudo htpasswd -c <repo-root>/.htpasswd gitusera

```

and I hit enter for no password.

Restart NGINX:

```bash
$ sudo systemctl restart nginx
```

You should now be able to go to ```<hostname>.local/gitweb``` in a web browser on any other machine on the network and view the gitweb homepage.

