import requests
import sys
import json
import time
from datetime import date, datetime, timedelta
import logging
import yaml
import os
import pprint
from logging.handlers import TimedRotatingFileHandler
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings()
pp = pprint.PrettyPrinter(indent=4)

class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}
        
        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()
       
    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None
    


if __name__ == '__main__':

    # set variables
    vmanage_host = "198.18.1.10"
    vmanage_port = "8443"
    username = "admin"
    password = "C1sco12345"

    Auth = Authentication()
    jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,username,password)
    token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

    if token is not None:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid}

    # base dataservice URL
    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

###############################################################################################

    payload = {
   "group":[
      "pythongrp"
       ],
       "description":"Demo User",
       "userName":"pythonuser",
       "password":"password"
    }

    payload = json.dumps(payload)
    mount_point = "/admin/user"
    response = requests.post(url = f'{base_url}{mount_point}', data = payload, headers=headers, verify=False)
    print(response)
 
