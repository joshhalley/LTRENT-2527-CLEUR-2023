# Table of Content

* [Task 6: Using Ansible with SDWAN vManage](#task-6-using-ansible-with-sdwan-vmanage)
  * [Step 1: Download Custom Ansible SDWAN Modules](#step-1-download-custom-ansible-sdwan-modules)
    * [Instructing Ansible to use custom Modules](#instructing-ansible-to-use-custom-modules)
  * [Step 2: Prepare a the inventory for vManage](#step-2-prepare-a-the-inventory-for-vmanage)
    * [vManage Variables](#vmanage-variables)
  * [Step 3: Create a Playbook for vManage](#step-3-create-a-playbook-for-vmanage)
    * [Executing the playbook](#executing-the-playbook)

## Task 6: Using Ansible with SDWAN vManage  

Having executed our first playbooks against an IOS XE device in the last section, we have begun to scratch the surface on how ansible can be used to simplify automation in a network. Clearly, for a single router or switch, it is usually overkill to create such logic for a one off activity. If however, the objective is to repeat a task, or deploy and/or execute a job across a broad array of network nodes or systems, Ansible can clearly simplify things.

Using Ansible to execute API calls against vManage to push a template

In this section we are going to shift gears a little bit, and move away from the earlier SDWAN C-Edge executions which Ansible was performing using the SSH protocol.
Instead, we are going to be looking at having Ansible directly interface with the API’s which exist within vManage to perform command and control tasks on the system.

## Step 1: Download Custom Ansible SDWAN Modules

Many modules which exist within Ansible can be downloaded directly via ansible-galaxy which acts as a package manager for hosted modules. Other modules, which……

In this section we are going to be using the programming logic and frameworks which exist in the below CiscoDevNet page:
<https://github.com/CiscoDevNet/python-viptela>
To retrive this project, in your Ansible-Lab directory execute the following command:

```code
git clone 
https://github.com/CiscoDevNet/python-viptela
Executing the above command will download the code repository and create a new directory with its contents.
Cloning into 'python-viptela'...
remote: Enumerating objects: 2093, done.
remote: Counting objects: 100% (450/450), done.
remote: Compressing objects: 100% (203/203), done.
remote: Total 2093 (delta 294), reused 367 (delta 235), pack-reused 1643
Receiving objects: 100% (2093/2093), 549.23 KiB | 2.03 MiB/s, done.
Resolving deltas: 100% (1345/1345), done.
dcloud@ubuntu:~/Ansible-Lab$
Cloned repository which was downloaded: 
```

```code
ls -tlr
total 16
-rw-rw-r-- 1 dcloud dcloud  114 Jan 29 18:13 ansible.cfg
drwxrwxr-x 2 dcloud dcloud 4096 Jan 30 10:54 tasks
-rw-rw-r-- 1 dcloud dcloud  525 Jan 30 11:07 inventory
drwxrwxr-x 9 dcloud dcloud 4096 Jan 30 11:38 python-viptela
```

### Instructing Ansible to use custom Modules

To allow for the new modules which are part of the cloned repository to be used, some further lines need to be added into the existing ansible.cfg file which is located in the Ansible-Lab directory (the new additions being highlighted in Yellow):

```yml
[defaults]
inventory: ./inventory
host_key_checking=False
library = python-viptella/ansible/modules
module_utils = python-viptella/ansible/module_utils
remote_tmp = /home/dcloud/Ansible-Lab/tmp

[privilege_escalation]
become=False
become_method=sudo
```

Once adding the content, save the file again, and we can move onto the next step of preparing the inventory for vManage.

## Step 2: Prepare a the inventory for vManage

The existing inventory which is configured at the moment has been focusing on our C-Edge locations which are using locations from Cisco Live 2023 venues.
In addition to these locations, we also have the location [RiodeJaneiro] which is pointing to a different host. This specific host is your vManage instance.
To allow for this host to be communicated with, we will need to populate the inventory file with some new credentials and information.

### vManage Variables

Opening up the inventory file, please proceed in adding a new section called [RiodeJaneiro:vars] .
The end output should look like what we have below with the new additions highlighted in Yellow:

```code
cat inventory
```

```yml
#format INI

[RiodeJaneiro]
198.18.1.10
<SNIP – REDACTED FOR BREVITY>
[RiodeJaneiro:vars]
ansible_user = admin
ansible_password = C1sco12345
vmanage_ip = 198.18.1.10
```

## Step 3: Create a Playbook for vManage

Now that the inventory has been updated with the requisite credentials, and the ansible.cfg file is pointing to the modules which we need for interacting with vManage. We can begin creation of the playbook.
Once again, in the tasks directory, create a file this time called vManage_ft_facts.yml populating the file with the following content:

```yml
---
- name: Verify SDWAN Deployment
  hosts: localhost

  tasks:
    - vmanage_feature_template_facts:
        user: "admin"
        host: "198.18.1.10"
        password: "C1sco12345"
        factory_default: no
```

An interesting observation to note is that the hosts: which are listed in the YAML file, instead of the entry pointing directly to an external system, it is actually pointing to the local system itself. The reason for this is that the Ubuntu server is responsible for executing API calls directly to vManage.

### Executing the playbook

After being configured, navigate back to the Ansible-Lab directory and execute the playbook using the below syntax:

```code
ansible-playbook tasks/vManage_ft_facts.yml
```

When launched you can see that Ansible shows that the playbook was executed with the status ‘ok’ however no output was visible:

```code
ansible-playbook tasks/vManage_ft_facts.yml
PLAY [Verify SDWAN Deployment] ****************************************************************************
TASK [Gathering Facts] ****************************************************************************
ok: [localhost]
TASK [vmanage_feature_template_facts] ****************************************************************************
[WARNING]: Module did not set no_log for password
ok: [localhost]
PLAY RECAP ****************************************************************************
localhost: ok=2 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

Unlike the other examples there was no configuration in the playbook indicating that the outputs should be written to standard out (stdout).
One method that can be used to view what return data is being written, is the activation of the verbose flags when executing the playbook, as seen in the example below:

```code
ansible-playbook   -vv tasks/vManage_ft_facts.yml
<SNIP>
PLAYBOOK: vManage_ft_facts.yml **********************************************************************************************************************************************
1 plays in tasks/vManage_ft_facts.yml

PLAY [Verify SDWAN Deployment] **********************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
task path: /home/dcloud/Ansible-Lab/tasks/vManage_ft_facts.yml:2
ok: [localhost]
META: ran handlers

TASK [vmanage_feature_template_facts] ***************************************************************************************************************************************
task path: /home/dcloud/Ansible-Lab/tasks/vManage_ft_facts.yml:6
[WARNING]: Module did not set no_log for password
ok: [localhost] => {"changed": false, "feature_templates": [{"attachedMastersCount": 1, "configType": "xml", "createdBy": "admin", "createdOn": 1669643778965, "deviceType": ["vedge-C8000V"], "devicesAttached": 2, "factoryDefault": false, "lastUpdatedBy": "admin", "lastUpdatedOn": 1669653516653, "resourceGroup": "global", "templateDefinition": {
```
