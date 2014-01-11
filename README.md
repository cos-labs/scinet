## OSF SciNet -- Crowd-Sourcing the Scientific Citation Network

### What is SciNet?

SciNet is a open source, collaborative project being developed at the Center for Open Science. The primary purpose of Scholarly is to provide the public with a free, open, and comprehensive dataset containing meta-data for academic citations as well as corresponding references. This dataset will allow the public to access, analyze, and distribute academic citation meta-data without restriction. 

### Relevant Wiki Pages:

* [Contributing -- Working with Git branches](https://github.com/centerforopenscience/scinet/wiki/Creating-and-using-branches-with-Git)

* [API Call Examples](https://github.com/centerforopenscience/scinet/wiki/API-Call-Examples)

* [Resources](https://github.com/centerforopenscience/scinet/wiki/Resources)

### Getting started with SciNet

**Note:** This set of packages is not production ready, but it should be robust enough for some early development. Additionally, these instructions were prepared using a Digial Ocean server running Ubuntu 12.04 but they can easily be adapted for running locally or on another cloud service.

1. Create your droplet:
    http://digitalocean.com

1. Check your email and make note of:
    IP Address of your droplet
    Username created for your droplet
    Password for your user

1. SSH into your droplet:

  1. Open up a terminal and type:

          ssh <username>@<ip address>
        enter the password located in the email
          
1. Set up a local (non-root) account:

  1. Create the user account:

          adduser <username>

  1. Give it sudo access:

          visudo
          # Below "root ALL=(ALL:ALL) All" enter
          <username> ALL=(ALL:ALL) ALL
          # Save the file and exit

1. Logout of your current account and SSH into the server with the new one:

  1. From your terminal enter:

          ssh <username>@<ip address>

1. Create a directory to hold our data:

  1. From your terminal enter:

          sudo mkdir /vol
          sudo chown <username>:<username> /vol
          cd /vol

1. Install necessary packages (Note: This can take a minute):

  1. From your terminal enter:

          sudo apt-get update
          sudo apt-get install git python-flask python-pip build-essential python-dev python-requests
          sudo apt-get install python-pyquery uwsgi-plugin-python uwsgi nginx
          sudo pip install pymongo reppy nameparser uwsgi

1. Clone and install SciNet:

  1. Checkout the repo:

          # e.g.: https://github.com/centerforopenscience/scinet.git
          git clone https://github.com/user_name/repo.git

  1. Install required libraries:

          cd /vol/scinet
          sudo pip install -r requirements.txt

  **Note:** If you are installing on Ubuntu, remove the lxml requirement from requirements.txt before running pip install.

  1. Test it:

          cd /vol/scinet/scinet
          python main.py

  You should get a pymongo "Connection Refused" error.

1. Install and setup mongodb:

  1. Add the 10gen repo:

          sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
          echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list
          sudo apt-get update
          sudo apt-get install mongodb-10gen

  1. Edit */etc/mongodb.conf* and change **dbpath=/var/lib/mongodb** to **dbpath=/vol/mongodb**, and update permissions:

          sudo mkdir /vol/mongodb
          sudo chown -R mongodb /vol/mongodb

  1. Restart mongo:

          sudo service mongodb restart

    At this point, you should be able to (optionally) restart the instance and run:

        python /vol/scinet/crowd-scholar/main.py

    without errors.

1. Get Citelet:

  1. Checkout the repo:

          # e.g.: https://github.com/jmcarp/citelet.git
          git clone https://github.com/user_name/repo.git

  1. Install required libraries::

          cd /vol/citelet
          sudo pip install -r requirements.txt

1. Build Citelet:

  1. Verify config file is pointing to your desired urls:

          vi /vol/citelet/cfg.py

  For more information visit the [Citelet docs](https://github.com/jmcarp/citelet/blob/master/README.md).

  1. Run the fabric build process:

          fab rsudo deploy

  1. Test it:

          cd /vol/citelet/app
          python main.py

1. Setup boto config so our keys will be loaded automatically:

  1. sudo vi /etc/boto.cfg:

          [Credentials]
          aws_access_key_id = <your access key>
          aws_secret_access_key = <your secret access key>

1. Install and setup NGINX and uWSGI:

  1. Configure NGINX, for example, replace /etc/nginx/sites-available/default with:

          server {
              listen   80;
                    server_name scinet;
                # scinet endpoint
                  location /scinet {
                      uwsgi_pass unix:///tmp/scinet.sock;
                  include uwsgi_params;
                  # strip path before handing it to app
                  uwsgi_param SCRIPT_NAME /scinet;
                  uwsgi_modifier1 30;
              }
              # citelet endpoint
                  location /citelet {
                      uwsgi_pass unix:///tmp/citelet.sock;
                  include uwsgi_params;
                  # strip path before handing it to app
                  uwsgi_param SCRIPT_NAME /citelet;
                  uwsgi_modifier1 30;
              }
          }

  1. Finally symlink it to its sites-enabled folder:

          sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

  1. Configure UWSGI sockets, for example, create /etc/uwsgi/apps-available/scinet.ini and populate it with:

          [uwsgi]
          chdir = /vol/scinet/scinet
          uid = www-data
          gid = www-data
          chmod-socket = 666
          socket = /tmp/scinet.sock
          module = app
          callable = app

  1. And, create /etc/uwsgi/apps-available/citelet.ini and populate it with:

          [uwsgi]
          chdir = /vol/citelet/app
          uid = www-data
          gid = www-data
          chmod-socket = 666
          socket = /tmp/citelet.sock
          module = main
          callable = app

  1. Finally symlink them to their respective enabled folders:

          sudo ln -s /etc/uwsgi/apps-available/scinet.ini /etc/uwsgi/apps-enabled/scinet.ini
          sudo ln -s /etc/uwsgi/apps-available/citelet.ini /etc/uwsgi/apps-enabled/citelet.ini

  1. Enable the app and restart:

          sudo service nginx restart
          sudo service uwsgi restart

  The site should now be up and running. You can, for instance, install lynx and visit Test the site by visiting, for example, http://<ip address>/scinet -or- http://<ip address>/citelet.

1. Still on the to-do list:

* Pushing the site via git, with automatic server restarts, etc., implemented as git post commit hooks.
* Automating the server setup process via the tools that Jeff and Lindsy were talking about.
