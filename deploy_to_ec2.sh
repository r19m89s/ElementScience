apt-get update && sudo apt-get -y upgrade
git clone https://github.com/r19m89s/ElementScience.git
apt-get install python-pip
pip install --upgrade pip
pip install --user flask
pip install --user requests
pip install --user apache-airflow
pip install --user botocore
pip install --user boto3
apt-get install nginx
apt-get install uwsgi-core uwsgi-plugin-python
