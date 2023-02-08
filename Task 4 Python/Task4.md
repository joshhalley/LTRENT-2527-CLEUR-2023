[Task 4: Rest API with Python](#task-4-rest-api-with-python)
* [ Step 1: Authenticate](#step-1-authenticate)
* [ Step 2: GET with Python](#step-2-get-with-python)
    * [  GET Edge List](#get-edge-list)
    * [  GET Device and Template List ](#get-device-and-template-list)
    * [  Get Template Variable List](#get-template-variable-list)
* [ Step 3: POST with Python](#step-3-post-with-python)
    * [  Change device hostname ](#change-device-hostname)
    * [Add vMange Usergroup ](#add-vmange-usergroup)
    * [Add vMange User ](#add-vmanage-user)
* [Step 4: SDWAN Policies with Python](#step-4-sdwan-policies-with-python)
    * [Get Policy List](#get-policy-list)
    * [Activate Policy](#activate-policy)
    * [Deactivate Policy](#deactivate-policy)
   * [Optional Task](#optional-task)


# Task 4: Rest API with Python

Postman is great to start interacting with and discovering APIs, but to automate and program the infrastructure, you need to build code that can be reused
We will now explore the APIs using python.

## Step 1: Authenticate

Below is the script for authentication, in which we have the following: 
•	A class named Authenticaton
•	Under the class we have defined 2 functions 
o	get_jsessionid
o	get_token

```
cat vmanage_auth.py 
```
```python
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


### GET Edge List
```
cat get_sdwan_edges_1.py
```
```python
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
        header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        header = {'Content-Type': "application/json",'Cookie': jsessionid}

    # base dataservice URL
    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

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
            ./get-device-template-list.py device_list
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
            ./get-device-template-list.py template_list
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
The below script will give the list of all the feature template variables and their respective values for a particular template attached to a particular device. The script uses the same authentication class used earlier
This output can then used as payload when attaching the respective template to other devices 
Take the template Id and Edge id from the previous output if needed

```
cat get-template-variable.py 
```
```python
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
```Change the template id and device id to get the same for other edges```

## Step 3: POST with Python

### Change device hostname 

Using the outputs from the previous call, we have the below script which is used to modify any variables for this device.
To demonstrate we will modify the hostname of the BR2 Edge 1 to BR2-EDGE-TEST 
Observe the payload format for this request. The sample can be taken from the APIDOCS (swagger)

```Changing hostname to BR2-EDGE1-TEST```

modify-device-variable.py

```python
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
```
### Add vManage User

```
cat post_sdwan_add_usr.py
```

```python
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
```

```
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
        header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        header = {'Content-Type': "application/json",'Cookie': jsessionid}

    # base dataservice URL
    base_url = "https://%s:%s/dataservice"%(vmanage_host,vmanage_port)

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


## Optional Task

Create another CLI Application with more functions like the created above for template and device list

```
cat vmanage_apis.py
```

```python
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


@click.group()
def cli():
    """Command line tool for monitoring Cisco SD-WAN solution components.
    """
    pass

@click.command()
def device_list():
    """ Retrieve and return network devices list.                                           
        Returns information about each device that is part of the fabric.                          
        \n Example command: ./vmanage_apis.py device-list
    """
    click.echo("\nRetrieving the devices.")

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
        tr = [item.get('host-name'), item.get('device-type'), item.get('uuid'), item.get('system-ip'), item.get('site-id'), item.get('version'), item.get('device-model')]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

#############################################################################################################

@click.command()
@click.option("--system_ip", help="System IP address of the device")
def system_status(system_ip):
    """ Retrieve and return information about System status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py system-status --system_ip 10.3.0.1
    """

    click.secho("\nRetrieving the System Status")

    url = base_url + "/device/system/status?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get system status " + str(response.text))
        exit()

    print("\nSystem status for Device:",system_ip)

    headers = ["Host name", "Up time", "Version", "Memory Used", "CPU system"]
    table = list()

    for item in items:
        tr = [item['vdevice-host-name'], item['uptime'], item['version'], item['mem_used'], item['cpu_system']]
        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

#############################################################################################################

@click.command()
@click.option("--system_ip", help="System IP address of the device")
def interface_status(system_ip):
    """ Retrieve and return information about Interface status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py interface-status --system_ip 10.3.0.1
    """

    click.secho("\nRetrieving the Interface Status")

    url = base_url + "/device/interface/synced?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of interface " + str(response.text))
        exit()

    print("\nInterfaces status for Device = ",system_ip)

    headers = ["Interface Name", "IP address", "VPN ID", "Operational status"]
    table = list()

    for item in items:
        if item.get('ip-address') != "-":
            tr = [item.get('ifname'), item.get('ip-address'),item.get('vpn-id'), item.get('if-oper-status')]
            table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

#############################################################################################################

@click.command()
@click.option("--system_ip", help="System IP address of the device")
def control_status(system_ip):
    """ Retrieve and return information about Control status of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py control-status --system_ip 10.3.0.1
    """

    click.secho("Retrieving the Control Status")

    url = base_url + "/device/control/synced/connections?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        click.echo("Failed to get list of devices " + str(response.text))
        exit()

    click.echo("\nControl Connection status for Device = %s"%system_ip)

    headers = ["Peer Type", "Peer System IP", "state", "Last Updated (UTC)"]
    table = list()

    for item in items:
        tr = [item['peer-type'], item['system-ip'], item['state'], time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(item['lastupdated']/1000.))]
        table.append(tr)

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

#############################################################################################################

@click.command()
@click.option("--system_ip", help="System IP address of the device")
def device_counters(system_ip):
    """ Retrieve information about Device Counters of network device in SD-WAN fabric

        Example command:
            ./vmanage_apis.py device-counters --system_ip 10.3.0.1
    """

    click.secho("Retrieving the Device Counters")

    url = base_url + "/device/counters?deviceId={0}".format(system_ip)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get device Counters " + str(response.text))
        exit()

    print("\nDevice Counters for device = ",system_ip)


    headers = ["OMP Peers Up", "OMP Peers Down", "vSmart connections", "BFD Sessions Up", "BFD Sessions Down"]
    table = list()

    for item in items:
        try:
            tr = [item['ompPeersUp'], item['ompPeersDown'], item['number-vsmart-control-connections'], item['bfdSessionsUp'], item['bfdSessionsDown']]
            table.append(tr)
        except KeyError:
            pass

    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))

#############################################################################################################

@click.command()
@click.option("--template", help="Template UUID value")
def attached_devices(template):
    """Retrieve and return devices associated to a template.
        Example command:
            ./vmanage_apis.py attached-devices --template 6c7d22bc-73d5-4877-9402-26c75a22bd08
    """

    url = base_url + "/template/device/config/attached/{0}".format(template)

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get template details")
        exit()

    headers = ["Host Name", "Device IP", "Site ID", "Host ID", "Host Type"]
    table = list()

    for item in items:
        tr = [item['host-name'], item['deviceIP'], item['site-id'], item['uuid'], item['personality']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
        
#############################################################################################################

@click.command()
def template_list():
    """ Retrieve and return templates list.                      
        \nExample command: ./vmanage_config_apis.py template-list
    """
    click.secho("Retrieving the templates available.")

    url = base_url + "/template/device"

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        print("Failed to get list of templates")
        exit()

    headers = ["Template Name", "Device Type", "Template ID", "Attached devices"]
    table = list()

    for item in items:
        tr = [item['templateName'], item['deviceType'], item['templateId'], item['devicesAttached']]
        table.append(tr)
    try:
        click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
    except UnicodeEncodeError:
        click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
        
#############################################################################################################

@click.command()
@click.option("--target", help="ID of the device to detach")
@click.option("--sysip", help="System IP of the system to detach")
def detach(target, sysip):
    """ Detach a device template.
        Provide all template parameters and their values as arguments.
        Example command:
          ./vmanage_apis.py detach --target TargetID --sysip 1.1.1.1
    """
    click.secho("Attempting to detach template.")

    payload = {
        "deviceType":"vedge",
        "devices":[  
            {
                "deviceId":str(target),
                "deviceIP":str(sysip)
            }
        ]
    }

    url = base_url + "/template/config/device/mode/cli"

    response = requests.post(url=url, data=json.dumps(payload), headers=header, verify=False)
    if response.status_code == 200:
        id = response.json()["id"]
        url = base_url + "/device/action/status/" + str(id)
        while(1):
            status_res = requests.get(url,headers=header,verify=False)
            if status_res.status_code == 200:
                push_status = status_res.json()
                if push_status['summary']['status'] == "done":
                    if 'Success' in push_status['summary']['count']:
                        print("Changed configuration mode to CLI")
                    elif 'Failure' in push_status['summary']['count']:
                        print("Failed to change configuration mode to CLI")
                        exit()
                    break
    else:
        print("Failed to detach template with error " + response.text)
        exit()

cli.add_command(detach)
cli.add_command(device_list)
cli.add_command(system_status)
cli.add_command(interface_status)
cli.add_command(control_status)
cli.add_command(device_counters)
cli.add_command(attached_devices)

if __name__ == "__main__":
    cli()
   
```