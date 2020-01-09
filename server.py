from flask import Flask,jsonify
import requests
import airflow
import json
from airflow import DAG
from airflow.operators.python_operator import ShortCircuitOperator, PythonOperator
from airflow.hooks.S3_hook import S3Hook
import logging
from collections import OrderedDict
from datetime import datetime

s3 = None

def log_to_s3(str):
    if(s3):
        str = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")+" "+str
        if (s3.check_for_key("logs/log.txt","element-science")):
            response = s3.read_key("logs/log.txt","element-science")  
            str =response+"\n "+str
        s3.load_string(str,"logs/log.txt","element-science",True,False)
        s3_conn = s3.get_conn()
        s3_conn.put_object_acl(ACL="public-read", Bucket="element-science", Key="logs/log.txt")
    else:
        return False

app = Flask(__name__)
@app.route('/API')
def apiRequest():
    twit_body = {}
    fb_body = {}
    insta_body = {}
    twit_request = 'https://takehome.io/twitter'
    fb_request = 'https://takehome.io/facebook'
    insta_request = 'https://takehome.io/instagram'
    try:
        twit = requests.get(twit_request)
        twit.raise_for_status()
        twit_body = twit.json()
        log_to_s3("Twitter Request: "+twit_request+", Response: "+twit.text)
    except requests.exceptions.HTTPError as e:
        resp = jsonify(OrderedDict(twitter_error=e.response.text,response_code=e.response.status_code))
        log_to_s3("Twitter Request: "+twit_request+", Response: "+e.response.text)
        return resp
    except requests.exceptions.Timeout as e:
        resp = jsonify(twitter_error="timeout")
        log_to_s3("Request: "+twit_request+", Response: TIMEOUT")
        return resp

    try:
        fb = requests.get(fb_request)
        fb.raise_for_status()
        fb_body = fb.json()
        log_to_s3("Facebook Request: "+fb_request+", Response: "+fb.text)
    except requests.exceptions.HTTPError as e:
        resp = jsonify(OrderedDict(facebook_error=e.response.text,response_code=e.response.status_code))
        log_to_s3("Facebook Request: "+fb_request+", Response: "+e.response.text)
        return resp
    except requests.exceptions.Timeout as e:
        resp = jsonify(OrderedDict(facebook_error="timeout"))
        log_to_s3("Facebook Request: "+fb_request+", Response: TIMEOUT")
        return resp
 
    try:
        insta = requests.get(insta_request)
        insta.raise_for_status()
        insta_body = insta.json()
        log_to_s3("Instagram Request: "+insta_request+", Response: "+insta.text)
    except requests.exceptions.HTTPError as e:
        resp = jsonify(OrderedDict(instagram_error=e.response.text,response_code=e.response.status_code))
        log_to_s3("Instagram Request: "+insta_request+", Response: "+e.response.text)
        return  resp
    except requests.exceptions.Timeout as e:
        resp = jsonify(OrderedDict(instagam_error="timeout"))
        log_to_s3("Instagram Request: "+insta_request+", Response: TIMEOUT")
        return jsonify(instagam_error="timeout")
    
    return jsonify(OrderedDict(twitter_body=twit_body,facebook_body=fb_body,instagram_body=insta_body))

if __name__ == "__main__":
    s3 = S3Hook('MyS3Conn')
    app.run(host="0.0.0.0", port=4040)
