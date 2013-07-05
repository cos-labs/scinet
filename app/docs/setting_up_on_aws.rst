Setting up CiteBin development/prototype server on AWS
------------------------------------------------------

Created June 28, 2013  -- Rob Chambers

Note that for a real MongoDB service, it's probably better to set up servers via the MongoDB AMI's
provided by AWS, as described `here. <http://docs.mongodb.org/ecosystem/tutorial/deploy-mongodb-from-aws-marketplace/#deploy-mongodb-from-aws-marketplace>`_

#) Go to AWS Console -> EC2 Dashboard. Choose the correct region in the upper-right. (Everything here can be done w/ command line tools; obviously, that's best in the long-term. )
#) Launch New Instance. 
    - Choose on-demand vs. spot
        - If you're using the free usage tier, then do ``Instances -> Launch Instance`` to begin starting an on-demand (usually expensive,
          but guaranteed) instance.
        - If you're actually paying, then you'll want to do a spot instance: ``Spot Instances -> Request Spot Instance``. When you get to 
          choose the spot price, pick a high one (for instance $1 - $2) so that your instance is unlikely to be shut down. In the long run,
          even if the price spikes once in a while, the spot instances are still ~80% cheaper than the on-demand instances.
    - Choose "Quick Start"
    - Choose Ubuntu Server 12.04 LTS (or some other relatively new but not bleeding-edge version.) Choose HVM if you need an extremely fast
      instance, and choose non-HVM if you want to run on smaller instances (recommended). (Note that another strong choice
      is Amazon Linux, which is RPM-based. I prefer Ubuntu, but Amazon is a solid choice.)
    - Choose Spot or On-Demand
        - Num of instances: 1
        - Instance Type: T1 Micro (note that micro is very slow compared to even the "small".)
        - Availability Zone: If you have other resources on AWS, be sure to use the same availability zone to avoid surcharges and
          get the best performance.
        - If you're using spot instances: Max Price: $1   Persistent Request: Yes.
    - Advanced Instance Options
        - Choose "Termination Protection".
    - Storage Device Configuration. (We create an auxiliary data partition here... this is in anticipation of the db eventually being very large.)
        - Root Volumes: click "Edit".
        - EBS Volumes tab: Create a new volume with:
            - Snapshot: None
            - Size: 10 GB (Note that you get 30GB free under free tier.)
    - Instance Details
        - Name: CiteBase Test Server 1    (or some similarily descriptive name, b/c it can be hard to tell instances apart when you have several).
    - Create Key Pair
        - Create a new key pair.
        - Enter a name, download the key pair. Save the .pem file somewhere safe/private.
        - Choose a security group, i.e., quicklaunch-1.
    - Create the instance. It typically takes a few minutes to start.
#) SSH to the Instance.
    - In EC2 under Instances, select the instance. It should be status 'running'.
    - Actions -> Connect.
    - Follow the instructions to connect either with a native SSH client (mac/linux) or with Putty (windows)
      or with Amazon's Java client (Windows). 
      - Username: ubuntu
#) Mount the EBS Volume.
    - Check to make sure that the EBS Volume (Elastic Block Store -> Volumes) is attached to your instance
      (under column "Attachment Information", your instance should be listed.)
    - Find the device path, for instance, ``/dev/xvdb`` :::
    
        sudo fdisk -l

    - Format the filesystem:::
    
    	sudo mkfs.ext4 /dev/xvdf
    	
    - Mount it permenantly:::
    
	  sudo mkdir -m 000 /vol
	  echo "/dev/xvdb /vol auto noatime 0 0" | sudo tee -a /etc/fstab
	  sudo mount /vol
	  sudo chown ubuntu:ubuntu -R /vol
        


    - You might check that this worked:::
    
    	touch /vol/tmp
    	sudo shutdown -r now
    	
      and then check that /vol/tmp still exists on restart.
#) Install necessary packages:::
	
	sudo apt-get update
	sudo apt-get install git python-flask python-pip build-essential python-dev python-requests
	sudo apt-get install python-pyquery uwsgi-plugin-python uwsgi nginx
	sudo pip install pymongo reppy nameparser uwsgi
	
#) Get crowd-scholar.
	- Checkout the repo:::
	
		cd /vol
		git clone https://github.com/user_name/repo.git
	
	- Test it:::
		
		cd crowd-scholar
		python main.py
		
	  You should get a pymongo "Connection Refused" error. 
	  
#) Install and setup mongodb:
	- Add the 10gen repo, which seems to include some nice install scripts...::
	
	    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
	    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list
	    sudo apt-get update
	    sudo apt-get install mongodb-10gen

	- Edit /etc/mongodb.conf , and change ``dbpath=/var/lib/mongodb`` to ``dbpath=/vol/mongodb``, and update permissions:::
	
		sudo mkdir /vol/mongodb
		sudo chown -R mongodb /vol/mongodb
		
	- Restart mongo:::
	
		sudo service mongodb restart                                                                                         
		
    - Create storage for raw data coming into crowdscholar and set permissions:::

        cd /vol/crowdscholar/
        sudo mkdir /vol/crowdscholar/app/raw
        sudo chown www-data /vol/crowdscholar/app/raw
        sudo chgrp www-data /vol/crowdscholar/app/raw
	
    - At this point, you should be able to (optionally) restart the instance and run:::
	
		python /vol/crowd-scholar/main.py
		
	  without errors.

#) Update and setup boto
    - Ubuntu 12.04 has an old version of boto, we need to update this so it can find our keys:::
      sudo pip uninstall boto
      sudo pip install boto

    - Setup boto config so our keys will be loaded automatically:::
      sudo vi /etc/boto.cfg
      ``[Credentials]
      aws_access_key_id = <your access key> 
      aws_secret_access_key = <your secret access key>``
	  
#) Install and setup NGINX and uWSGI	  
	- Configure NGINX, for example, replace ``/etc/nginx/sites-available/default``  with:::
	
		server {
	        listen   80;
	
	        # Make site accessible from http://localhost/
	        server_name localhost;
	
	        location / { 
                    try_files $uri @app;
                    }
	        location @app {
	                include uwsgi_params;
                    uwsgi_pass unix:/tmp/uwsgi.sock;
	                }                                                                                                                       
	        }

	- Configure UWSGI, for example, replace ``/etc/uwsgi/apps-available/uwsgi.ini`` with:::
	
		[uwsgi]
		chdir = /vol/crowd-scholar
		uid = www-data
		gid = www-data
		chmod-socket = 666
		socket = /tmp/uwsgi.sock
		module = app
		callable = app
	
	- Enable the app w/ a symlink and restart:::
	
		sudo ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/
		sudo service nginx restart
		sudo service uwsgi restart
		
	- The site should now be up and running. You can, for instance, install lynx and visit
	  ``http://localhost/`` via the terminal and see Citebin.	  
#) Enable HTTP.
	- Open AWS EC2 Web Console.
	- Select the running instance under 'Instances'.
		- Under 'Description', note the host address, such as ``ec2-67-202-56-148.compute-1.amazonaws.com``. 
	  Note that you can assign an elastic IP to this host instead, and you can quite easily associate
	  a domain name with the elastic IP; but for now, we'll use the AWS-provided domain name.
	- Note the security group; for instance, "quicklaunch-1". 
	- Click 'Security Groups' and then the appropriate group (e.g. quicklaunch-1).
	- Click the ``Inbound`` tab.
	- Create a new rule:
		- Type: HTTP
		- Source: 0.0.0.0/0 (the default)
		- "Add Rule"
		- "Apply Rule Changes"
	- Test the site by visiting, for example, ``http://ec2-67-202-56-148.compute-1.amazonaws.com``.
		
		
Your site should now be running. Still on the to-do list:

* Pushing the site via git, with automatic server restarts, etc., implemented as git post commit hooks.
* Automating the server setup process via the tools that Jeff and Lindsy were talking about.

This site is not production ready, but it should be robust enough for some early development.





