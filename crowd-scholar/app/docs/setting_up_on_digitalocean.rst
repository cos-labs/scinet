Setting up CiteBin development/prototype server on AWS
------------------------------------------------------

Created June 28, 2013  -- Rob Chambers

Note that for a real MongoDB service, it's probably better to set up servers via the MongoDB AMI's
provided by AWS, as described `here. <http://docs.mongodb.org/ecosystem/tutorial/deploy-mongodb-from-aws-marketplace/#deploy-mongodb-from-aws-marketplace>`_

#) Create your droplet at http://digitalocean.com

#) Check your email and make note of:
    - IP Address of your droplet
    - Username created for your droplet
    - Password for your user

#) SSH into your droplet
    - Open up a terminal and type:
        
      ``ssh <username>@<ip address>
        enter the password located in the email``

#) Set up a local (non-root) account
    - Create the user account:
        
      ``adduser ubuntu``
    
    - Give it sudo access:
        
      ``visudo
        # Below "root ALL=(ALL:ALL) All" enter 
        ubuntu ALL=(ALL:ALL) ALL
        # Save the file and exit``

#) Logout of your current account and SSH into the server with the new one:
    - From your terminal enter:
        
        ``ssh ubuntu@<ip address>``
    
#) Create a directory to hold our data:
    
  ``sudo mkdir /vol
    sudo chown ubuntu:ubuntu /vol
    cd /vol``   
        
#) Install necessary packages:
  ``sudo apt-get update
	sudo apt-get install git python-flask python-pip build-essential python-dev python-requests
	sudo apt-get install python-pyquery uwsgi-plugin-python uwsgi nginx
	sudo pip install pymongo reppy nameparser uwsgi``
	
#) Get crowd-scholar.
	- Checkout the repo:
        
      ``# e.g.: https://github.com/hrybacki/crowd-scholar.git
        git clone https://github.com/user_name/repo.git``
        	
    - Install required libraries:
        
      ``cd /vol/crowd-scholar
        sudo pip install -r requirements.txt
        sudo pip install git+git://github.com/jmcarp/sciparse.git``

	- Test it:
		
      ``cd crowd-scholar
		python main.py``
		
	  You should get a pymongo "Connection Refused" error. 
	  
#) Install and setup mongodb:
	- Add the 10gen repo, which seems to include some nice install scripts...
	
	  ``sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
	    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list
	    sudo apt-get update
	    sudo apt-get install mongodb-10gen``

	- Edit /etc/mongodb.conf , and change ``dbpath=/var/lib/mongodb`` to ``dbpath=/vol/mongodb``, and update permissions:
	
          ``sudo mkdir /vol/mongodb
            sudo chown -R mongodb /vol/mongodb``
		
	- Restart mongo:
	
	  ``sudo service mongodb restart``                                                                                         
    - At this point, you should be able to (optionally) restart the instance and run:::
	
	    python /vol/crowd-scholar/main.py
		
      without errors.

#) Get citelet
	- Checkout the repo:::
        
        # e.g.: https://github.com/jmcarp/citelet.git
        git clone https://github.com/user_name/repo.git
        	
    - Install required libraries:::
        
        cd /vol/citelet
        sudo pip install -r requirements.txt

    - Build citelet:
        - Add the base url for the citelet make file to your to your ~/.bash_profile::
            
            export CITELET_BASE_URL="scholarly.io\/citelet"
        
        - Ensure it is in your path environment::
            
            source ~/.bash_profile

        - Run the make file::
        
            cd /vol/citelet
            make

        - Note: If an error similar to:::
        
            File "py-util/minify.py", line 3, in <module>
                import slimit
            
        - Manually install the package:::
            
            sudo pip install <package>

	- Test it:::
		
		cd /vol/citelet/app
		python main.py
		
#) Setup boto config so our keys will be loaded automatically:::
        
        sudo vi /etc/boto.cfg
        
        [Credentials]
        aws_access_key_id = <your access key> 
        aws_secret_access_key = <your secret access key>
	  
#) Install and setup NGINX and uWSGI	  
	- Configure NGINX, for example, replace ``/etc/nginx/sites-available/default``  with:
	
		``server {
            listen   80;
	
	        server_name scholarly;
	
            # crowdscholar endpoint
	        location /crowdscholar { 
	            uwsgi_pass unix:///tmp/crowdscholar.sock;
                include uwsgi_params;
                # strip path before handing it to app
                uwsgi_param SCRIPT_NAME /crowdscholar;
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
        }``

        - Finally symlink it to its sites-enabled folder

            ``ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default``

	- Configure UWSGI sockets, for example, create ``/etc/uwsgi/apps-available/crowdscholar.ini`` and populate it with
	
		``[uwsgi]
		chdir = /vol/crowd-scholar/crowd-scholar
		uid = www-data
		gid = www-data
		chmod-socket = 666
		socket = /tmp/crowdscholar.sock
		module = app
		callable = app``

        and create ``/etc/uwsgi/apps-available/citelet.ini`` and populate it with
	
		``[uwsgi]
		chdir = /vol/citelet/app
		uid = www-data
		gid = www-data
		chmod-socket = 666
		socket = /tmp/citelet.sock
		module = main
		callable = app``

        - Finally symlink them to their respective enabled folders::

            ln -s /etc/uwsgi/apps-available/crowdscholar /etc/uwsgi/apps-enabled/crowdscholar
            ln -s /etc/uwsgi/apps-available/citelet /etc/uwsgi/apps-enabled/citelet
	
    - Enable the app and restart:::
	
		sudo service nginx restart
		sudo service uwsgi restart
		
	- The site should now be up and running. You can, for instance, install lynx and visit
	- Test the site by visiting, for example, ``http://<ip address>/crowdscholar`` and ``http://<ip address>/citelet``.
		
		
Your site should now be running. Still on the to-do list:

* Pushing the site via git, with automatic server restarts, etc., implemented as git post commit hooks.
* Automating the server setup process via the tools that Jeff and Lindsy were talking about.

This site is not production ready, but it should be robust enough for some early development.
