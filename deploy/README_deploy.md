# CONP Portal Deployment on portal.conp.ca Notes

### Requirements

You will need to be given the credentials of for the server to perform this procedure. There are notes that will be generally useful here for any other deployment.

These instructions pertain to an Ubuntu 18.04, with NGINX 

### Host information

The portal is deployed on `portal.conp.ca`.

It is an internal machine, so you will need to ssh to it internally.  Credentials and info will be given to appropriate personnel.

The production server uses mariadb which is hosted by the MCIN. Credentials will be distributed to appropriate personnel.

You will need sudo and access to the user `conp-admin` on the machine.

### GUNICORN

Part of the requirments.txt installs the appropriate python packages. The server used is Gunicorn, which is a python based multi-worker production server that supports WSGI.

### Source Code

The source code is deployed under the `conp-admin` user in the `conp-portal` directory, the current version of the software can be obtained from `git status`. There is a `.flaskenv` file that has the unique settings for the portal, with access being given to approprate folks.

NOTE: The package Flask-Dance required a modification to ensure that redirect urls used the https protocol.  So this has been forked into the CONP-PCNO team and the requirements.txt has been updated to install from here.

### systemctl files

In the systemctl_files directory are the scripts to add to the `/etc/systemd/system` directory.  There are two files:

1. `gunicorn.socket` - This creates an on-the-fly socket for the gunicorn service to use.

2. `gunicorn.service` - This runs the service.

Once installed, one just needs to start the socket service, and the server will pop up when someone tries to access it at the appropriate port on the server.

`sudo systemctl start gunicorn.socket`

You can use the `journalctl` tool to view the logs of the running services. To see the logs for the web server with the latest entries at the top, you can use:

`sudo journalctl gunicron.service -r`

If you make any changes to the `gunicorn.service` file, you will need to run:

`sudo systemctl daemon-reload`

### NGINX configuration

The NGINX configuration is located here in the `nginx_config` directory. The NGINX provides the proxy layer that is routing into the gunicon service. This file is to be placed in `/etc/nginx/sites-available`. Symbolic links in `/etc/niginx/sites-enabled` provide NGINX the actual configurations to use. Use `systemctl` to start | stop | restart nginx.  

For example, to restart the NGINX service:

`sudo systemctl restart nginx`

### Complete Stop of Portal

1. `sudo systemctl stop nginx`
2. `sudo systemctl stop gunicorn`
3. `suco systemctl stop gunicorn.socket`

### Complete Start up of the Portal

1. `sudo systemctl start gunicron.socket`
2. `sudo systemctl start nginx`






