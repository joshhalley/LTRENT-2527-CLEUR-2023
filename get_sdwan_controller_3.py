import requests
import sys
import json
import time
from datetime import date, datetime, timedelta
import logging
import yaml
import os
import pprint
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
    vmanage_host = os.environ.get("vManage_IP")
    vmanage_port = os.environ.get("vManage_PORT")
    username = os.environ.get("vManage_USERNAME")
    password = os.environ.get("vManage_PASSWORD")

    Auth = Authentication()
    jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,username,password)
#    print(jsessionid)
    token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)
#    print(token)

    if token is not None:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid}

    # base dataservice URL
    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

###############################################################################################

    url = base_url + "/system/device/controllers"
    print(url)
    response = requests.get(url=url, headers=headers,verify=False)
    items = response.json()['data']
    print(json.dumps(items, indent=4))
    for device in items:
        print(f"Device controller => {device['deviceType']} with IP address {device['deviceIP']}")
		
		
