Setting up CiteBin development/prototype server on AWS
------------------------------------------------------

Created June 28, 2013  -- Rob Chambers

Note that for a real MongoDB service, it's probably better to set up servers via the MongoDB AMI's
provided by AWS, as described `here. <http://docs.mongodb.org/ecosystem/tutorial/deploy-mongodb-from-aws-marketplace/#deploy-mongodb-from-aws-marketplace>`

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
 	
 	- Storage Device Configuration
 	
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
 	  
    - Find the device path:::
    	sudo fdisk -l
    	
    	 
 			

      
     

