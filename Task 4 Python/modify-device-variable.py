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

payload = {
  "deviceTemplateList": [
    {
      "templateId": "d6231e3c-3613-499c-aabc-57c66999e38d",
      "device": [
        {
          "csv-status": "complete",
          "csv-deviceId": "C8K-6CA314A2-44A1-A49C-8E10-C36096E78608",
          "csv-deviceIP": "10.4.0.1",
          "csv-host-name": "BR2-EDGE1",
          "//system/host-name": "BR2-EDGE11",
          "//system/system-ip": "10.4.0.1",
          "//system/site-id": "400",
          "/10/vpn-instance/ip/route/vpn10_static_route1_ip_prefix/prefix": "10.4.11.0/24",
          "/10/vpn-instance/ip/route/vpn10_static_route1_ip_prefix/next-hop/vpn10_static_route1_next_hop/address": "10.4.10.65",
          "csv-templateId": "d6231e3c-3613-499c-aabc-57c66999e38d",
          "selected": "true"
        }
      ],
      "isEdited": "false",
      "isMasterEdited": "false"
    }
  ]
}

payload = json.dumps(payload)
url = base_url + "/template/device/config/attachfeature"
print(url)
response = requests.post(url=url, data=payload, headers=headers, verify=False)
print(response)


