# Task 0: Setup the Ubuntu Environment 

Install all the needed linux packages for establishing SD-WAN network automation environment.

```
sudo apt update
sudo apt install -y git vim 
sudo apt install python3-pip -y
sudo pip3 install --upgrade pip
```
Please check the version of Python installed on your system.
```
python3 -V
python3 --version
```
Ensure the version 3.8.10 or above

## Setting up Python Automation Environment

We will install all the required packages in this task 

```
vim requirements.txt 
```
Copy the below packages 
```
ansible==6.7.0
ansible-core==2.13.7
certifi==2019.3.9
chardet==3.0.4
click==8.1.3
et-xmlfile==1.0.1
Flask-BasicAuth==0.2.0
Flask==2.2.2
idna==2.8
itsdangerous==2.1.2
jdcal==1.4.1
Jinja2==3.1.2
MarkupSafe==2.1.2
napalm==4.0.0
ncclient==0.6.13
netmiko==3.4.0
nornir==3.3.0
nornir-ansible==2022.7.30
nornir-jinja2==0.2.0
nornir-napalm==0.3.0
nornir-netmiko==0.1.2
nornir-scrapli==2021.7.30
nornir-utils==0.2.0
numpy==1.19.0
openpyxl==3.0.4
pandas==1.0.1
paramiko==2.7.2
pyaml==20.4.0
python-dateutil==2.8.1
pytz==2020.1
requests==2.21.0
requests-toolbelt==0.9.1
six==1.15.0
tabulate==0.8.10
urllib3==1.24.3
Werkzeug==2.2.2
xmltodict==0.13.0
json2html==1.3.0
```
Run the following command 
```
python3 -m pip install -r requirements.txt
```
To find out the version of an installed package, use
```
pip feeze
```


# Task 1: Rest API with CURL 

cURL: Linux command line application.

https://curl.se/

Curl has an extensive command line syntax, and being an open source project, is heavily used by developers within the field. 

To begin with this task, we are going to follow a number of steps to familairize you with cURL and its operations. 

In the first step, we are simply going to login to a vManage server via a API POST call, and retrieve the JSESSIONID cookie, this cookie will be used within subsequent steps. 
## Step 1: Log In
•	Before using various REST APIs, you must first log in to vManage. 
•	Specifically, execute as follows. 
•	A successful login saves the JSESSIONID in a cookie.
```
curl --insecure \
     --location \
     --request POST "https://198.18.1.10/j_security_check" \
     --header "Content-Type: application/x-www-form-urlencoded" \
     --data "j_username=admin&j_password=C1sco12345" \
     --cookie-jar cookie.txt
```
From the above execution a few observations should be made from the CLI syntax. 

--insecure 

 This switch needs to be used in scenarios where the certificate may not be trusted. 

Such scenarios where this happens, is when a certificate is present on the device which is not from a public CA, or if a private CA is in use, and the server executing the request, does not consider the certificate as trusted.

--location 

<josh to update> 

--request

--header

--data

--cookie-jar

## Step 2: Get a list of Devices
As an example of REST API, let's try "Get device list"
```
curl --insecure \
     --location \
     --request GET "https://198.18.1.10/dataservice/device" \
     --cookie cookie.txt
```

Responses are returned in JSON format. To improve readability for humans, format it by piping it to python -m json.tool
```
curl --insecure \
     --location \
     --request GET "https://198.18.1.10/dataservice/device" \
     --cookie cookie.txt \
     | python -m json.tool
```


# Task 3: Rest API with Postman

## Step 1: Postman Configuration
A Postman environment is a list of variables that can be used to easily switch between different environments. By simply modifying the vManage username, password, port and hostname in the case of your environment, you can access and interact with different Cisco SD-WAN fabrics. The variables that are defined in the environment can be re-used also throughout the API calls that are defined in the collection.

A Postman collection is a group of API calls that define endpoints or resources that are available for that specific API. The collection also includes other parameters, headers, or authentication methods that are needed to successfully complete the call.

Login to the windows machine using RDP and launch the Postman Application

Before running any exercise, verify that your Postman configuration has SSL certificate verification disabled

![postman](images/pm-1.png) 


A sample Postman Collection and a set of environment variables are already created to save time 

![postman](images/pm-2.png) 

![postman](images/pm-3.png) 
 


 



## Step 2: Authentication
The first step in interacting with an API is usually authentication. Authentication ensures that only legitimate users have access to the API.

In your Cisco-SD-WAN collection, you can see that the first API call that you have is called Authentication and is in a folder named Authentication.

The Authentication call is a POST call.

 To define the endpoint for the authentication call, you use the environment variable {{vmanage}}. These values will be replaced with the ones you have defined in the environment variables

The resource that you are sending the API call to is j_security_check.

After the variables are replaced, the resulting endpoint for authentication is https://{ip_address}.com/j_security_check 

Under the Headers tab, you define the Content-Type header.

For Cisco SD-WAN authentication, the type is application/x-www-form-urlencoded.
The username and password are URL-encoded in the Body or the request and are sent as key value pairs j_username and j_password. You will populate the values for the username and password from the environment variables with the same names.

These are all the parameters that you need to authenticate to the vManage instance: the endpoint, the method, the header, and the body.

![postman](images/pm-4.png) 

The body of the returned information should be empty and the status should be 200 OK if everything went well. This status means that the user was successfully authenticated. Notice that the response returns a Cookie named JSESSIONID. You use this cookie in the subsequent API calls in the next sections of this Lab. This cookie has a limited lifetime and is a temporary representation of the successful authentication of the admin account.

![postman](images/pm-5.png) 
 

## Step 3: API Cross-Site Request Forgery Prevention
This feature adds protection against Cross-Site Request Forgery (CSRF) that could occur when using Cisco SD-WAN REST APIs. The system provides this protection by requiring a CSRF token with API requests. This token is need to POST requrest. 

Execute the GET token request to generate the XSRF Token

![postman](images/pm-6.png) 

## Step 4: GET SD-WAN Fabric Devices 
After you successfully authenticated and obtained the JSESSIONID cookie, you can now obtain the data that you want from the Cisco SD-WAN REST API.
The Fabric Devices API call uses the GET method and the /dataservice/device endpoint to obtain a JSON-formatted list of all the devices that are part of the SD-WAN fabric. 
After you press Send in Postman for this first API call, you should see a response similar to the following:
 
![postman](images/pm-7.png) 

If you do not get a response, check to make sure that the status code response is 200 OK, if not the most probable cause is that your JSESSIONID cookie has expired and you need to re-authenticate once more. The output in the body of the response is verbose and informative, containing extensive data about each device in the fabric.

The next API in the collection is called Devices Status and uses the GET method on the /dataservice/device/monitor endpoint to obtain specific information regarding the status of all the devices in the fabric.

## Step 5: GET SD-WAN Devices Status
The next API in the collection is called Devices Status and uses the GET method on the /dataservice/device/monitor endpoint to obtain specific information regarding the status of all the devices in the fabric.
After you press Send in Postman for this first API call, you should see a response similar to the following:
 
![postman](images/pm-8.png) 

You can see that the JSON output is the same and consistent no matter if you get the data through the swagger documentation or Postman.

## Step 6: GET SD-WAN Devices Counters
The next API call in the Postman collection uses a GET method on the https://{{vmanage}}:{{port}}/dataservice/device/counters resource. 
 
![postman](images/pm-9.png) 

## Step 7: GET SD-WAN Interface Statistics
Next, you try to obtain interface statistics for the devices that are part of the SD-WAN fabric. The endpoint that will return extensive statistics for all the interfaces on all the devices in the fabric is /dataservice/statistics/interface


![postman](images/pm-10.png) 

Depending on the size of the fabric, this call can take a large amount of time to return data or time out entirely. You can clearly see the power of the API, in which, with one call you can obtain extensive statistics for all the interfaces on all the devices in the fabric. By passing different parameters with this API call, like specific time intervals, specific devices or even specific interfaces, the output can be limited significantly.	

Explore the other API GET calls in the postman collections and observe the results 

## Step 8: Add User Group
Goto the admin tasks folder and explore “Add User Group” API call. 
This being a POST request needs the XSRF token. The token is taken as a variable and is loaded in the environment variable from the previous GET call

![postman](images/pm-11.png) 

Look at the Request body it will create a user group called “demogrp” with read and write access to “Manage user” feature 

![postman](images/pm-12.png) 

## Step 9: Add User 
The next call with let us create a user “demouser” and assign it to “demogrp”. 

![postman](images/pm-13.png) 

## Step 10: Generate code with Postman
You have learned how to authenticate to the Cisco SD-WAN REST API and how to interact with it to extract data by using Postman. Postman has another very useful feature: code generation.
Once you build your API call, you specify the method, the endpoint, the headers, body, authentication and parameters, and then you can generate code in several programming languages that re-create the same API call in the programming language you have chosen.
The following example uses the Add User call from the collection. On the right corner of the Postman client page, there is a Code option:

![postman](images/pm-14.png) 

If you click the Code option, you can select between several programming languages, including Python, Ruby, Go, C#, C, NodeJS, JavaScript, and PHP.
If you select Python, the Authentication will be reproduced in Python by using the requests library.

The following code is in cURL, observe the inclusion of XSRF token and JSESSION ID

![postman](images/pm-15.png)  

The following image shows the Python code generated by Postman. Use Copy to clipboard to copy the code snippet in the Postman interface, after which you can paste the code in your favorite IDE and start to use it.

![postman](images/pm-16.png) 

At the top of the code snippet, the requests library is imported, after which variables are defined for the API resource that is being accessed (url), the username and password (payload), and the headers (headers).
The response variable contains the response of the POST request and at the end, the text method of the response object is displayed to the user.
You can do the same for all the other calls you explored in this Lab and obtain the Python code for them. You can then combine them in scripts and applications for automation and network programmability purposes


# Task 4: Rest API with Python

Postman is great to start interacting with and discovering APIs, but to automate and program the infrastructure, you need to build code that can be reused
We will now explore the APIs using python

## Step 1: Authenticate

Below is the script for authentication, in which we have the following 
•	A class named Authenticaton
•	Under the class we have defined 2 functions 
o	get_jsessionid
o	get_token

```
cat vmanage_auth.py 
```
```python
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

    # set variables
vmanage_host = os.environ.get("vManage_IP")
vmanage_port = os.environ.get("vManage_PORT")
username = os.environ.get("vManage_USERNAME") 
password = os.environ.get("vManage_PASSWORD")

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

    Auth = Authentication()
    jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,username,password)
    print(jsessionid)
    token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)
    print(token)

    if token is not None:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        headers = {'Content-Type': "application/json",'Cookie': jsessionid}

    # base dataservice URL
    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)
```

•	The final section in the authentication is using the Authentication class 
•	This is used to log in to SD-WAN vManage and get the jsessionid and token.
•	The get_jsessionid() is used to log in to SD-WAN vManage and get the jsessionid.
•	The get_token() is used to get the token
•	The variable jsessionid is used to set the cookie that is required for the API endpoint to be accessed.
•	Here the token is the value of the token that is stored in the session.
•	The token is stored in the session when the user logs in.
•	The base url is composed of the vmanage_host and vmanage_port variables.
•	The vmanage ip, port username and passwords are taken from the environment variables
Add the environment variable, execute the above script, it will print the JSESSION ID and the XSRF token 
```
export vManage_IP=198.18.1.10
export vManage_PORT=443
export vManage_USERNAME=admin
export vManage_PASSWORD=C1sco12345

python3 vmanage_auth.py 
JSESSIONID=I5Jw-qCdy5nqxcsKZCadZSda-QytelBbGqY6lQFu.f781faf4-cf63-4f7c-9f80-b63169da9c7b
1AB84846F363D8849BCA647558FC89ACA8C4F835B3456BF8935B44DF08258C27EBB6EA8960E865B6EFCD851BD00DBDFAF449
dcloud@ubuntu:~/lab/final_scripts$
```
## Step 2: GET with Python
Now using the above authentication class, we can create scripts to run GET and POST operations

GET Controller List

Below script uses the authentication class and then at the end run a GET for controllers and extracts just the [data] portion of the JSON and store it in a variable called items
It now iterates over each device in the items with a for loop and extract data for the devicetype and deviceIP. After this display the data as specified in the print statement
```
cat get_sdwan_controller_1.py 
```
```python
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

    for device in items:
        print(f"Device controller => {device['deviceType']} with IP address {device['deviceIP']}")
```
```
python3 get_sdwan_controller_1.py 
https://198.18.1.10:443/dataservice/system/device/controllers
Device controller => vmanage with IP address 10.10.10.10
Device controller => vsmart with IP address 12.12.12.12
Device controller => vsmart with IP address 22.22.22.22
Device controller => vbond with IP address 11.11.11.11
```

Modify the code as below if you want to see the full response 
```
    url = base_url + "/system/device/controllers"
    print(url)
    response = requests.get(url=url, headers=headers,verify=False)
    items = response.json()['data']
    print(items)
    for device in items:
        print(f"Device controller => {device['deviceType']} with IP address {device['deviceIP']}")
```

Modify the code as below if you want to see the full response in pretty format
```
    url = base_url + "/system/device/controllers"
    print(url)
    response = requests.get(url=url, headers=headers,verify=False)
    items = response.json()['data']
    print(json.dumps(items, indent=4))
    for device in items:
        print(f"Device controller => {device['deviceType']} with IP address {device['deviceIP']}")
```


### GET vEdge List
```
cat get_sdwan_edges_1.py
```
```python
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

    url = base_url + "/system/device/vedges"
    print(url) 
    response = requests.get(url=url, headers=headers,verify=False)
    vedges = response.json()['data']

    for vedge in vedges:
        print(f"vEdge device => {vedge['deviceModel']} with serialnumber {vedge['serialNumber']}")
		
```

```
python3 get_sdwan_edges_1.py 
https://198.18.1.10:443/dataservice/system/device/vedges
vEdge device => vedge-C8000V with serialnumber 5BA2D66C
vEdge device => vedge-C8000V with serialnumber 75E93603
vEdge device => vedge-C8000V with serialnumber 2485C88D
vEdge device => vedge-C8000V with serialnumber 445B38B7
vEdge device => vedge-C8000V with serialnumber 5B0A9622
```


### GET Device and Template List 
The below uses click to create the CLI component of the application
Two CLI commands are grouped under the cli Group: device_list and template-list, The commands correspond to what you want the application to do from the beginning:
* Get a list of all the devices in the SD-WAN fabric (device_list).
* Get a list of all the configuration templates on the vManage instance (template-list).

To established session with the vManage server it uses the instance of the authentication class that you called Authentication. 
It will use the get_request method of this object to get a list of all the devices and templates in the fabric and store the JSON data that is returned by the API in the response variable.
It extracts just the [data] portion of the JSON and store it in a variable called items. The items variable at this point contains all the devices in the fabric and many of additional data about each of them
It now iterates over each item in the items with a for loop and extract data for the hostname, device-type, uuid, system-ip, site-id, version, and device-model of each device. After this uses tabulate to display the data
```
cat get-device-template-list.py 
```
```python
#! /usr/bin/env python3
"""
Class with REST Api GET and POST libraries
Example: python rest_api_lib.py vmanage_hostname username password
PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage
Note: All the three arguments are manadatory
"""
import requests
import sys
import json
import click
import os
import tabulate
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

vmanage_host = os.environ.get("vManage_IP")
vmanage_port = os.environ.get("vManage_PORT")
vmanage_username = os.environ.get("vManage_USERNAME")
vmanage_password = os.environ.get("vManage_PASSWORD")

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None :
    print("CISCO SDWAN details must be set via environment variables before running.")
    print("export vManage_IP=198.18.1.10")
    print("export vManage_PORT=8443")
    print("export vManage_USERNAME=admin")
    print("export vManage_PASSWORD=C1sco12345")
    print("")
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
            if logger is not None:
                logger.error("No valid JSESSION ID returned\n")
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

Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

if token is not None:
    header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json",'Cookie': jsessionid}

base_url = "https://%s:%s/dataservice"%(vmanage_host, vmanage_port)

###############################################################################################

@click.group()
def cli():
    """Command line tool for deploying templates to CISCO SDWAN.
    """
    pass

@click.command()
def device_list():
    """Retrieve and return network devices list.
        Returns information about each device that is part of the fabric.
        Example command:
            ./sdwan.py device_list
    """
    click.secho("Retrieving the devices.")

    url = base_url + "/device"
    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of devices " + str(response.text))
        exit()

    headers = ["Host-Name", "Device Type", "Device ID", "System IP", "Site ID", "Version", "Device Model"]
    table = list()

    for item in items:
        tr = [item['host-name'], item['device-type'], item['uuid'], item['system-ip'], item['site-id'], item['version'], item['device-model']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

###############################################################################################

@click.command()
def template_list():
    """Retrieve and return templates list.
        Returns the templates available on the vManage instance.
        Example command:
            ./sdwan.py template_list
    """
    click.secho("Retrieving the templates available.")

    url = base_url + "/template/device"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of templates")
        exit()

    headers = ["Template Name", "Device Type", "Template ID", "Attached devices", "Template version"]
    table = list()

    for item in items:
        tr = [item['templateName'], item['deviceType'], item['templateId'], item['devicesAttached'], item['templateAttached']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

cli.add_command(device_list)
cli.add_command(template_list)

if __name__ == "__main__":
    cli()

```
```
python3 get-device-template-list.py device-list
Retrieving the devices.
╒═════════════╤═══════════════╤══════════════════════════════════════════╤═════════════╤═══════════╤═══════════════╤════════════════╕
│ Host-Name   │ Device Type   │ Device ID                                │ System IP   │   Site ID │ Version       │ Device Model   │
╞═════════════╪═══════════════╪══════════════════════════════════════════╪═════════════╪═══════════╪═══════════════╪════════════════╡
│ vManage     │ vmanage       │ f781faf4-cf63-4f7c-9f80-b63169da9c7b     │ 10.10.10.10 │        10 │ 20.9.2        │ vmanage        │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ vSmart1     │ vsmart        │ 10a98779-95f0-4383-871c-195d25bd9c74     │ 12.12.12.12 │        10 │ 20.9.2        │ vsmart         │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ vSmart2     │ vsmart        │ 704bbc2f-aa9a-4068-84a2-fc31602ed553     │ 22.22.22.22 │        20 │ 20.9.2        │ vsmart         │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ vBond       │ vbond         │ abd5e9d7-9dee-4d00-98b5-fdc71de6ea63     │ 11.11.11.11 │        10 │ 20.9.2        │ vedge-cloud    │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ BR1-EDGE1   │ vedge         │ C8K-1EA287B0-B235-ABD9-A22E-07A3A75816EF │ 10.3.0.1    │       300 │ 17.09.02.0.48 │ vedge-C8000V   │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ BR1-EDGE22  │ vedge         │ C8K-1789220C-6036-338F-526A-94E545AB8272 │ 10.3.0.2    │       300 │ 17.09.02.0.48 │ vedge-C8000V   │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ BR2-EDGE11  │ vedge         │ C8K-6CA314A2-44A1-A49C-8E10-C36096E78608 │ 10.4.0.1    │       400 │ 17.09.02.0.48 │ vedge-C8000V   │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ DC-EDGE1    │ vedge         │ C8K-E75016E7-317F-9987-525B-11816F7A3155 │ 10.1.0.1    │       100 │ 17.09.02.0.48 │ vedge-C8000V   │
├─────────────┼───────────────┼──────────────────────────────────────────┼─────────────┼───────────┼───────────────┼────────────────┤
│ DC-EDGE2    │ vedge         │ C8K-2FC5E478-48EC-D7EF-3895-814AB5D2ECD6 │ 10.1.0.2    │       100 │ 17.09.02.0.48 │ vedge-C8000V   │
╘═════════════╧═══════════════╧══════════════════════════════════════════╧═════════════╧═══════════╧═══════════════╧════════════════╛
```

```
python3 get-device-template-list.py template-list
Retrieving the templates available.
╒═════════════════════════════════════════════════════╤═════════════════════╤══════════════════════════════════════╤════════════════════╤════════════════════╕
│ Template Name                                       │ Device Type         │ Template ID                          │   Attached devices │   Template version │
╞═════════════════════════════════════════════════════╪═════════════════════╪══════════════════════════════════════╪════════════════════╪════════════════════╡
│ Factory_Default_ISR_4331_V01                        │ vedge-ISR-4331      │ eeeaec50-6f1a-4b0a-9090-d4f0898dac02 │                  0 │                 14 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_SDBranch_C8000V_Template_V01                │ vedge-C8000V        │ 2e9cb06b-97a3-4ca1-8bc5-102c5b9fe258 │                  0 │                 16 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_AWS_TGW_C8000V_Template_V01                 │ vedge-C8000V        │ e7367e8d-c77e-4c17-8edd-112c4108e76f │                  0 │                 11 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Factory_Default_C1111_8PLTELA_V01                   │ vedge-C1111-8PLTELA │ 7612fa7c-5c80-4452-bd7b-2728e5089ad6 │                  0 │                 15 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Factory_Default_DC1_HUB                             │ vedge-C8000V        │ 14c99914-d45a-4c36-b5b0-21e2cb519371 │                  0 │                 19 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_SDBranch_vEdge_cloud_Template_V01           │ vedge-cloud         │ 60aa328a-cb42-458a-be5b-afa374f6622e │                  0 │                 14 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_AWS_TGW_CSR1000V_Template_V01               │ vedge-CSR-1000v     │ 490721c2-7926-48c5-916f-73a00d18a398 │                  0 │                 11 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Factory_Default_CSR_1000V_V01                       │ vedge-CSR-1000v     │ c1c10783-25d0-429f-86bb-086386ade67b │                  0 │                 22 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_GCP_C8000V_Template_V01                     │ vedge-C8000V        │ 6fb5350a-3047-411b-9cba-b76965fabd8f │                  0 │                 10 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Factory_Default_1_TLOC_Branch_Template              │ vedge-C8000V        │ 7441fb6e-76d6-4f59-8a0d-02a385e9d2a5 │                  0 │                 17 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_Azure_vWAN_C8000V_Template_V01              │ vedge-C8000V        │ 0e437ba8-a737-4ee8-b8a8-bc03d5f35793 │                  0 │                 11 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_BOOTSTRAP_DHCP_8000V_Template_V01           │ vedge-C8000V        │ c3ef69cb-6634-4d6f-9846-2103ac8e2e44 │                  0 │                 11 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_SDBranch_ISRv_Template_V01                  │ vedge-ISRv          │ d4f5bb5e-dd9b-47e4-bcc0-a5196a86bbf2 │                  0 │                 16 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_MEGAPORT_ICGW_C8000V_Template_V01           │ vedge-C8000V        │ ba6de3ef-47a8-4cd9-bac2-a6501ad5bd14 │                  0 │                  9 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_BOOTSTRAP_STATIC_8000V_Template_V01         │ vedge-C8000V        │ 09962a0a-bf7e-42c7-8f37-626bb4f71e1e │                  0 │                 10 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Default_EQUINIX_DHCP_DNS_ICGW_CSR1000V_Template_V02 │ vedge-CSR-1000v     │ f567d57c-3ca1-4ac6-bc2e-c4df2cce89f5 │                  0 │                 11 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ Factory_Default_C8000V_V01                          │ vedge-C8000V        │ 34dc64ff-cc98-463c-8f38-2cb7e804ac9d │                  0 │                 22 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ VSMART                                              │ vsmart              │ 43fb52ec-3a78-4223-beeb-51cc8bd315f2 │                  2 │                  8 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ DC                                                  │ vedge-C8000V        │ 9ae531dd-beac-4b21-be95-99abf6d19fe8 │                  2 │                 19 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ BRANCH-TYPE2                                        │ vedge-C8000V        │ d6231e3c-3613-499c-aabc-57c66999e38d │                  1 │                 16 │
├─────────────────────────────────────────────────────┼─────────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ BRANCH-TYPE1                                        │ vedge-C8000V        │ ed13d4b5-6059-4865-ab84-0e591b21e45f │                  2 │                 20 │
╘═════════════════════════════════════════════════════╧═════════════════════╧══════════════════════════════════════╧════════════════════╧════════════════════╛
``` 
 

### Get Template Variable List
The below script will give the list of all variable and their respective values for a particular template attached to a particular device. The script uses the same authentication class used earlier
This output can then used as payload when attaching the respective template to other devices 
Take the template Id and Edge id from the previous output if needed

```
cat get-template-variable.py 
```
```python
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

    # set variables
vmanage_host = os.environ.get("vManage_IP")
vmanage_port = os.environ.get("vManage_PORT")
username = os.environ.get("vManage_USERNAME") 
password = os.environ.get("vManage_PASSWORD")


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
``` 

```
python3 get-template-variable.py 
```
```json
<Response [200]>
[
    {
        "csv-status": "complete",
        "csv-deviceId": "C8K-6CA314A2-44A1-A49C-8E10-C36096E78608",
        "csv-deviceIP": "10.4.0.1",
        "csv-host-name": "BR2-EDGE1",
        "//system/host-name": "BR2-EDGE1",
        "//system/system-ip": "10.4.0.1",
        "//system/site-id": "400",
        "/10/vpn-instance/ip/route/vpn10_static_route1_ip_prefix/prefix": "10.4.11.0/24",
        "/10/vpn-instance/ip/route/vpn10_static_route1_ip_prefix/next-hop/vpn10_static_route1_next_hop/address": "10.4.10.65"
    }
]
```


## Step 3: POST with Python

### Change device hostname 

Using the outputs from the previous 2 calls, we have the below script which is used to modify any variables for this device.
To demonstrate we will modify the hostname of the router 
Observe the payload format for this request. The sample can be taken from the APIDOCS (swagger)

```Changing hostname to BR2-EDGE1-TEST```

modify-device-variable.py

```python
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
          "//system/host-name": "BR2-EDGE1-TEST",
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
```

### Add vMange Usergroup 

```
cat post_sdwan_add_group
```
```python
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
        "groupName": "pythongrp",
        "tasks": [
                {
                    "feature": "Manage Users",
                    "read": True,
                    "enabled": True,
                    "write": True
                }
                ]
    }

    payload = json.dumps(payload)
    mount_point = "/admin/usergroup"
    response = requests.post(url = f'{base_url}{mount_point}', data = payload, headers=headers, verify=False)
    print(response)
 
```

```
python3 post_sdwan_add_group.py 
<Response [200]>
Add vManage User
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

python3 post_sdwan_add_usr.py 
<Response [200]>
```

## Step 4: SDWAN Policies with Python

The below scripts again uses click to create the CLI component of the application.
We have 3 options defined
* Get  Policy List
* Activate Policy
* Deactivate Policy

The code again use the same authentication class to get the JSESSION ID and Token and then defined the above methods separately 
```
cat policy-list-activate-deactivate.py 
```
```python
#! /usr/bin/env python

import os
import tabulate
import requests
import click
import json
import sys

requests.packages.urllib3.disable_warnings()

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vManage_IP")
vmanage_port = os.environ.get("vManage_PORT")
vmanage_username = os.environ.get("vManage_USERNAME")
vmanage_password = os.environ.get("vManage_PASSWORD")

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("export vManage_IP=198.18.1.10")
    print("export vManage_PORT=443")
    print("export vManage_USERNAME=admin")
    print("export vManage_PASSWORD=C1sco12345")


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
            click.echo("No valid JSESSION ID returned\n")
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


Auth = Authentication()
jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)

if token is not None:
    header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json",'Cookie': jsessionid}

base_url = "https://%s:%s/dataservice"%(vmanage_host, vmanage_port)

###############################################################################################

@click.group()
def cli():
    """Command line tool for vManage Templates and Policy Configuration APIs.
    """
    pass

@click.command()
def policy_list():
    """ Retrieve and return centralized policies list.                              
        \nExample command: ./policy-list-activate-deactivate.py policy-list
    """
    click.secho("Retrieving the Centralized Policies available.")

    url = base_url + "/template/policy/vsmart"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of policies")
        exit()

    headers = ["Policy Name", "Policy Type", "Policy ID", "Active/Inactive"]
    table = list()

    for item in items:
        tr = [item['policyName'], item['policyType'], item['policyId'], item['isPolicyActivated']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
        


###############################################################################################
@click.command()
@click.option("--name", help="Name of the policy")
def activate_policy(name):
    """   Activate centralized policy.                              
        \nExample command: ./policy-list-activate-deactivate.py activate-policy --name MultiTopologyPlusAppRoute
    """

    policy_uuid = ""
    url = base_url + "/template/policy/vsmart"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
        for item in items:
            if item["policyName"] == name:
                policy_uuid = item['policyId']
                click.echo("Policy UUID for %s is %s"%(name,policy_uuid))
                break
    else:
        click.echo("Failed to get list of policies")
        exit()

    if policy_uuid == "":
        click.echo("Failed to find Policy UUID for %s, Please check if policy exists on vManage"%name)
        exit()

    url = base_url + "/template/policy/vsmart/activate/%s?confirm=true"%policy_uuid

    payload = {}

    response = requests.post(url=url, headers=header, data=json.dumps(payload),verify=False)
    if response.status_code == 200:
        process_id = response.json()['id']
        url = base_url + "/device/action/status/" + process_id
        while(1):
            policy_status_res = requests.get(url,headers=header,verify=False)
            if policy_status_res.status_code == 200:
                policy_push_status = policy_status_res.json()
                if policy_push_status['summary']['status'] == "done":
                    if 'Success' in policy_push_status['summary']['count']:
                        click.echo("\nSuccessfully activated vSmart Policy %s"%name)
                    elif 'Failure' in policy_push_status['summary']['count']:
                        click.echo("\nFailed to activate vSmart Policy %s"%name)
                    break
    else:
        click.echo("\nFailed to activate vSmart Policy %s"%name)



###############################################################################################
@click.command()
@click.option("--name", help="Name of the policy")
def deactivate_policy(name):
    """   Deactivate centralized policy.                              
        \nExample command: ./policy-list-activate-deactivate.py deactivate-policy --name MultiTopologyPlusAppRoute
    """

    policy_uuid = ""
    url = base_url + "/template/policy/vsmart"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
        for item in items:
            if item["policyName"] == name:
                policy_uuid = item['policyId']
                click.echo("Policy UUID for %s is %s"%(name,policy_uuid))
                break
    else:
        click.echo("Failed to get list of policies")
        exit()

    if policy_uuid == "":
        click.echo("Failed to find Policy UUID for %s, Please check if policy exists on vManage"%name)
        exit()

    url = base_url + "/template/policy/vsmart/deactivate/%s?confirm=true"%policy_uuid

    payload = {}

    response = requests.post(url=url, headers=header, data=json.dumps(payload),verify=False)
    if response.status_code == 200:
        process_id = response.json()['id']
        url = base_url + "/device/action/status/" + process_id
        while(1):
            policy_status_res = requests.get(url,headers=header,verify=False)
            if policy_status_res.status_code == 200:
                policy_push_status = policy_status_res.json()
                if policy_push_status['summary']['status'] == "done":
                    if 'Success' in policy_push_status['summary']['count']:
                        click.echo("\nSuccessfully deactivated vSmart Policy %s"%name)
                    elif 'Failure' in policy_push_status['summary']['count']:
                        click.echo("\nFailed to deactivate vSmart Policy %s"%name)
                    break
    else:
        click.echo("\nFailed to deactivate vSmart Policy %s"%name)

cli.add_command(policy_list)
cli.add_command(activate_policy)
cli.add_command(deactivate_policy)

if __name__ == "__main__":
    cli()
```

### Get  Policy List
```
python3 policy-list-activate-deactivate.py policy-list
Retrieving the Centralized Policies available.
╒══════════════════════════════╤═══════════════╤══════════════════════════════════════╤═══════════════════╕
│ Policy Name                  │ Policy Type   │ Policy ID                            │ Active/Inactive   │
╞══════════════════════════════╪═══════════════╪══════════════════════════════════════╪═══════════════════╡
│ StrictHub-n-Spoke            │ feature       │ f4a1dc95-8558-4400-bb46-fdbaadd99b7b │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPolicy          │ feature       │ 6ff80e3c-a8e8-4fbf-9b55-32568093440c │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusFWInsertion │ feature       │ be10f4fb-e866-465d-9f38-ade87fda33bc │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusACL         │ feature       │ 96240228-0192-4ea4-b48b-a192e9a45d80 │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusAppRoute    │ feature       │ cb279d4a-883c-476e-83e6-d1f80ab048c1 │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ cflowd_policy                │ cli           │ c310604e-8e93-46b7-9273-449e8b9b127f │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ Hub-Spoke-Policy-PCI         │ feature       │ 858b7a53-b54f-4927-b5b1-130e84287169 │ False             │
╘══════════════════════════════╧═══════════════╧══════════════════════════════════════╧═══════════════════╛
```
 

### Activate Policy

```
python3 policy-list-activate-deactivate.py activate-policy --name MultiTopologyPolicy
Policy UUID for MultiTopologyPolicy is 6ff80e3c-a8e8-4fbf-9b55-32568093440c

Successfully activated vSmart Policy MultiTopologyPolicy
```
```
python3 policy-list-activate-deactivate.py policy-list
Retrieving the Centralized Policies available.
╒══════════════════════════════╤═══════════════╤══════════════════════════════════════╤═══════════════════╕
│ Policy Name                  │ Policy Type   │ Policy ID                            │ Active/Inactive   │
╞══════════════════════════════╪═══════════════╪══════════════════════════════════════╪═══════════════════╡
│ StrictHub-n-Spoke            │ feature       │ f4a1dc95-8558-4400-bb46-fdbaadd99b7b │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPolicy          │ feature       │ 6ff80e3c-a8e8-4fbf-9b55-32568093440c │ True             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusFWInsertion │ feature       │ be10f4fb-e866-465d-9f38-ade87fda33bc │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusACL         │ feature       │ 96240228-0192-4ea4-b48b-a192e9a45d80 │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusAppRoute    │ feature       │ cb279d4a-883c-476e-83e6-d1f80ab048c1 │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ cflowd_policy                │ cli           │ c310604e-8e93-46b7-9273-449e8b9b127f │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ Hub-Spoke-Policy-PCI         │ feature       │ 858b7a53-b54f-4927-b5b1-130e84287169 │ False             │
╘══════════════════════════════╧═══════════════╧══════════════════════════════════════╧═══════════════════╛

```

### Deactivate Policy
```
python3 policy-list-activate-deactivate.py deactivate-policy --name MultiTopologyPolicy
Policy UUID for MultiTopologyPolicy is 6ff80e3c-a8e8-4fbf-9b55-32568093440c

Successfully deactivated vSmart Policy MultiTopologyPolicy
```

```
dcloud@ubuntu:~/lab/final_scripts$ python3 policy-list-activate-deactivate.py policy-list
Retrieving the Centralized Policies available.
╒══════════════════════════════╤═══════════════╤══════════════════════════════════════╤═══════════════════╕
│ Policy Name                  │ Policy Type   │ Policy ID                            │ Active/Inactive   │
╞══════════════════════════════╪═══════════════╪══════════════════════════════════════╪═══════════════════╡
│ StrictHub-n-Spoke            │ feature       │ f4a1dc95-8558-4400-bb46-fdbaadd99b7b │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPolicy          │ feature       │ 6ff80e3c-a8e8-4fbf-9b55-32568093440c │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusFWInsertion │ feature       │ be10f4fb-e866-465d-9f38-ade87fda33bc │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusACL         │ feature       │ 96240228-0192-4ea4-b48b-a192e9a45d80 │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ MultiTopologyPlusAppRoute    │ feature       │ cb279d4a-883c-476e-83e6-d1f80ab048c1 │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ cflowd_policy                │ cli           │ c310604e-8e93-46b7-9273-449e8b9b127f │ False             │
├──────────────────────────────┼───────────────┼──────────────────────────────────────┼───────────────────┤
│ Hub-Spoke-Policy-PCI         │ feature       │ 858b7a53-b54f-4927-b5b1-130e84287169 │ False             │
╘══════════════════════════════╧═══════════════╧══════════════════════════════════════╧═══════════════════╛
```


 
