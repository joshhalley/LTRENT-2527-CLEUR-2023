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