#! /usr/bin/env python
import requests
import sys
import json
import click
import os
import tabulate
import yaml
import time
from datetime import date, datetime, timedelta
import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

vmanage_host = os.environ.get("vManage_IP")
vmanage_port = os.environ.get("vManage_PORT")
vmanage_username = os.environ.get("vManage_USERNAME") 
vmanage_password = os.environ.get("vManage_PASSWORD")

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
    print("CISCO SDWAN details must be set via environment variables before running.")
    print("export vManage_IP=198.18.1.10")
    print("export vManage_PORT=8443")
    print("export vManage_USERNAME=admin")
    print("export vManage_PASSWORD=C1sco12345")
    exit()

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

    Auth = Authentication()
    jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
    print(jsessionid)
    token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)
    print(token)

    if token is not None:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid}

    # base dataservice URL
    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

###############################################################################################


    payload = {
                "templateId":"d6231e3c-3613-499c-aabc-57c66999e38d",  
                "deviceIds":
                    [                    
                      "C8K-6CA314A2-44A1-A49C-8E10-C36096E78608"
                    ]
             }

    payload = json.dumps(payload)
    mount_point = "/template/device/config/input"
    response = requests.post(url = f'{base_url}{mount_point}', data = payload, headers=headers, verify=False)
    print(response)
    items = response.json()['data']
    print(json.dumps(items, indent=4))
 
