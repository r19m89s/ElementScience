# ElementScience

## Description Of Files
- **README.py** a project description and installation tutorial
- **element_science.log** a uwsgi log file (used in ec2 deployment)
- **element_science.pid** a uwsgi process file (used in ec2 deployment)
- **server.py** a flask application that consumes and returns the responses to the endpoints provided in the assignment 
specifications.
- **test.py** a unit test file that mocks service responses and asserts the flask applications body and status code.
- **uwsgi.ini** a uwsgi configuration file (used in ec2 deployment)

## Logging
The project is currently logging line by line to an s3 log file located here: https://element-science.s3.us-east-2.amazonaws.com/logs/log.txt. This file is currently set to be publically accessible. The current status of the log file will be downloaded as a text file every time a GET request to the s3 url is sent. 

## Python Dependencies
- **flask** (https://flask.palletsprojects.com/en/1.1.x/) used to deploy and maintain the RESTful server.
- **requests** (https://2.python-requests.org/en/master/) used to interact with the external RESTful endpoints.
- **apache-airflow** (https://airflow.apache.org/) used to retrieve and write to the s3 log document.
- **collections** (https://docs.python.org/2/library/collections.html) used to maintain the order of the returned response.
- **datetime** (https://docs.python.org/3/library/datetime.html) used to retrieve the current server's timestamp.
- **botocore** (https://pypi.org/project/botocore/) a dependency for apache-airflow's interaction with the s3 service.
- **boto3** (https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) used by botocore and apache-airflow.

## EC2 Deployment dependencies
- **nginx** (https://www.nginx.com/) maintains and controls api after server deployment to s3.
- **uwsgi** (https://uwsgi-docs.readthedocs.io/en/latest/) configures the server to serve the flask applicaton.
- **aws-cli** (https://aws.amazon.com/cli/) is required to write to the s3 file (both boto3 and apache-airflow require credentials to access the s3 file).

## Local Deployment Description
1. Clone the repository.
2. pip install the required python dependencies described above.
3. Ensure that you currently have ```aws-cli``` installed. Run ```aws2 --version``` if version-2 is installed, else run ```aws --version``` 

In the case that ```aws-cli``` isn't installed, follow the following instructions: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux-mac.html#cliv2-linux-mac-install%5D%5B1%5D

3. ```cd``` into the local directory into which the project has been cloned.
4. Fire ```GET``` requests to the following URL to test the behavior of the application ```http://0.0.0.0:5000/API```

## EC2 Deployment Description
1. If you don't currently have an AWS account, sign up for one (https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/). Ensure that both EC2 and S3 are included as services for your account. 
2. Navigate to your EC2 dashboard and choose to create a new instance. 
![EC2 Launch Instance](https://github.com/r19m89s/ElementScience/blob/master/tutorial/Screen%20Shot%202020-01-08%20at%208.16.06%20PM.png "Launch Instance")
3. Ensure that EC2 instance is of type Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
![Ubuntu Type](https://github.com/r19m89s/ElementScience/blob/master/tutorial/Screen%20Shot%202020-01-08%20at%208.24.31%20PM.png "Ubuntu Type")
4. The instance type t2.micro should suffice for the requirements of this project.
![Instance Type](https://github.com/r19m89s/ElementScience/blob/master/tutorial/Screen%20Shot%202020-01-08%20at%208.27.13%20PM.png "Instance Type")
5. Edit security group so that it allows for an ssh connection from your local IP address (if you already have an existing security group configured to respect a localized ssh connection, use that).
![Edit Security Group](https://github.com/r19m89s/ElementScience/blob/master/tutorial/Screen%20Shot%202020-01-08%20at%208.28.59%20PM.png "Edit Security Group")
![Adding SSH Connection](https://github.com/r19m89s/ElementScience/blob/master/tutorial/Screen%20Shot%202020-01-08%20at%208.31.11%20PM.png "Adding SSH Connection")
6. Create a new key pair for AWS, or, if you have a previously used AWS pair, use that
![Download SSH Key](https://github.com/r19m89s/ElementScience/blob/master/tutorial/Screen%20Shot%202020-01-08%20at%208.35.01%20PM.png "Download SSH Key")
7. Ensure that the downloaded key pair has been configured to be respected by aws by running ```sudo chmod 400 <aws_key_file>```
8. SSH into the EC2 instance that you've created, using the downloaded key, by running ```ssh -i "<aws_key_file>" ubuntu@<ec2_public_dns>```
9. Run the following commands on the command line:
    1. ```git clone https://github.com/r19m89s/ElementScience.git``` - clone the project onto the ec2 instance
    2. ```cd <path_to_cloned_library>``` - move into cloned directory
    3. ```sudo chmod a+x deploy_to_ec2.sh``` - allow dependency script to be executable
    4. ```sudo ./deploy_to_ec2.sh``` - run dependency installation script
    5. ```uwsgi <path to cloned project>/uwsgi.ini``` - configure uwsgi to use configuration found in project's uwsgi.ini file. 
    6. ```sudo service nginx restart``` - restarts nginx, correctly running the installed project. 
