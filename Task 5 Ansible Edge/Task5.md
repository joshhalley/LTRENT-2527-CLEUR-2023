# Table of Content

* [Task 5: Using Ansible with SDWAN C-EDGEs](#task-5-using-ansible-with-sdwan-c-edges)
  * [Step 1: Verify the status of the Ansible Installation](#step-1-verify-the-status-of-the-ansible-installation)
  * [Step 2: Create a new ansible.cfg file for your automation](#step-2-create-a-new-ansiblecfg-file-for-your-automation)
    * [Configuration selection order:](#configuration-selection-order)
    * [Configuration file format:](#configuration-file-format)
    * [Navigate to the directory:](#navigate-to-the-directory)
  * [Step 3: Creating your Inventory](#step-3-creating-your-inventory)
    * [INI File Format](#ini-file-format)
    * [Creating an INI Inventory File for the Lab](#creating-an-ini-inventory-file-for-the-lab)
  * [Step 4: Node Variables](#step-4-node-variables)
    * [Inline within Inventory File](#inline-within-inventory-file)
    * [Group Based Variables in Inventory](#group-based-variables-in-inventory)
  * [Step 5: Executing an Ad-Hoc Task](#step-5-executing-an-ad-hoc-task)
  * [Step 6: Deploying your first playbook](#step-6-deploying-your-first-playbook)
    * [Create Directory Structure For Playbooks](#create-directory-structure-for-playbooks)
    * [Creating your first Playbook](#creating-your-first-playbook)
    * [Adding your first Plays](#adding-your-first-plays)

## Task 5: Using Ansible with SDWAN C-EDGEs  

Ansible has become synonymous with automation in modern companies, providing a means to simplify complex tasks without the need for the network operator to be an expert in programming or scripting languages.
This section is going to explore the use of Ansible to achieve a number of actions within the SDWAN architecture.

* Use Ansible to connect directly to a c-edge and verify control plane state
* Use Ansible to connect directly to a c-edge and verify the dataplane state
* Use Ansible to execute API calls against vManage to push a template

## Step 1: Verify the status of the Ansible Installation

To verify the installation state of Ansible, the execution of ansible –version is performed:

```code
ansible --version
```

```code
ansible [core 2.13.7]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/lab/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/lab/.local/lib/python3.8/site-packages/ansible
  ansible collection location = /home/lab/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/lab/.local/bin/ansible
  python version = 3.8.10 (default, Nov 14 2022, 12:59:47) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
```

Interesting points to observe from the above output, is the location of the ansible.cfg file – this file is responsible for defining key charateristics for your Ansible automation activities, and the subsequent execution of ad-hoc tasks and playbooks.  
It is also good to note the version of ansible which is running, and the version of python.
Ansible modules are written in the python scripting language.

## Step 2: Create a new ansible.cfg file for your automation

Creating an ansible configuration file is the first step that a new operator should perform when getting started.
By default, there is a vast array of options and configuration knobs which are active in Ansible, way too many to cover in the course of this lab.
That said, to get a sneak preview of what the defaults look like, you can execute the command:

```code
ansible-config init --disabled > ansible.full_config
```

This command will generate a complete configuration for Ansible, including all the default parameters.
To get an idea of what this default configuration looks like, you can execute the command:

```code
cat ansible.full_config | head
```

Which will print the first lines of the created default configuration:

```yml
[defaults]
# (boolean) By default Ansible will issue a warning when received from a task action (module or action plugin)
# These warnings can be silenced by adjusting this setting to False.
;action_warnings=True

# (list) Accept list of cowsay templates that are 'safe' to use, set to empty list if you want to enable all installed templates.
;cowsay_enabled_stencils=bud-frogs, bunny, cheese, daemon, default, dragon, elephant-in-snake, elephant, eyes, hellokitty, kitty, luke-koala, meow, milk, moofasa, moose, ren, sheep, small, stegosaurus, stimpy, supermilker, three-eyes, turkey, turtle, tux, udder, vader-koala, vader, www

# (string) Specify a custom cowsay path or swap in your cowsay implementation of choice
;cowpath=
```

Since there are way more parameters in the full default configuration file than will be needed for the purpose of this lab, the above information is only informational.
We will create a much more simplistic configuration for the purpose of our exercise.

### Configuration selection order

By default Ansible will attempt to use a configuration file in the following locations:

* 1. Environment variable ANSIBLE_CONFIG if not set it will continue to attempt to find a file with the below precedence:
* 2. ./ansible.cfg
* 3. ~/.ansible.cfg
* 4. /etc/ansible/ansible.cfg

Looking at our default –version output, we can see that we are presently pointing to the fourth option.

### Configuration file format

The format of the configuration file is key value pairs, with the section titles being enclosed in square brackets.
Lets start our lab execise by creating a directory, and in that directory creating the ansible.cfg file:
Directory creation:

```code
mkdir Ansible-Lab
```

### Navigate to the directory

```code
cd Ansible-Lab
```

Create your ansible.cfg file (using your favorite unix text editor):

```code
vim ansible.cfg
```

Inside the ansible.cfg file, we are going to add the following information:

```yml
[defaults]
inventory: ./inventory
host_key_checking=False

[privilege_escalation]
become=False
become_method=sudo
```

The configuration added defines a number of actions:

[defaults]  is the expected and initial section for the configuration file, within this section we are defining the inventory location, which will provide the list for hosts which will be communicated with for the execution of ansible playbooks.

[privilege_escalation] is used for scenarios where system tasks may be executed on a remote unix host, often the use of su or sudo may be used for operations such as processes to be restarted or new packages to be installed.

For our purposes today, this is the extent of the configuration which we will adding into the ansible.cfg file.
Once the above content has been added, save the file and close it.
Once in the Ansible-Lab directory, you should now be able to see the change in prioritization for the ansible.cfg file, by once again executing

```code
ansible –-version
```

Now upon executing that command the outputs should no longer point to the former location of /etc/ansible/ansible.cfg but rather to the new file which you created in the Ansible-Lab directory:

```code
ansible [core 2.13.7]
  config file = /home/lab/Ansible-Lab/ansible.cfg
  configured module search path = ['/home/lab/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/lab/.local/lib/python3.8/site-packages/ansible
  ansible collection location = /home/lab/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/lab/.local/bin/ansible
  python version = 3.8.10 (default, Nov 14 2022, 12:59:47) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
```

## Step 3: Creating your Inventory

Since the Ansible configuration file has now been created, our first step towards building our first playbook has been concluded.
The next action which needs to happen is the definition of our inventory needs to take place. The inventory can be created through the use of YAML format or the more user friendly INI format.
For the purpose of this lab – we will use the INI format to initially create the configuration.

### INI File Format

The INI format is very straight forward, and can be as simple as created a numbered list of systems or DNS names, ie:

```yml
10.20.30.40
40.50.60.70
80.90.100.110
www.cisco.com
www.meraki.com
www.thousandeyes.com
```

The above is the easiest possible form of deploying your inventory.

### Creating an INI Inventory File for the Lab

As we want to better understand the power of Ansible, we are going to take a slightly more complex approach to the generation of the INI Inventory, which lets us perform more targeted automation execution.
Within the same directory that you placed your ansible.cfg file, please create a file called inventory using your favorite text editor. Within this file we are going to create location headings which match up with the Cisco Live Locations for 2023, closing the location definition within [ square brackets ].  
Within those location headings we will populate the nodes which we will be working with through the course of this lab.

```code
vim inventory
```

``` yml
#format INI

[RiodeJaneiro]
198.18.1.10

[LasVegas]
198.18.3.100   #DC-EDGE1
198.18.3.101   #DC-EDGE2

[Melbourne]
198.18.3.104   #BR1-EDGE1
198.18.3.105   #BR1-EDGE2

[Amsterdam]
198.18.3.106   #BR2-EDGE1

[CiscoLive:children]
Amsterdam
LasVegas
Melbourne
```

Once the file has been completed, close and save the file, checking that the file has been properly created by using the below command:

```code
cat /home/lab/Ansible-Lab/inventory
```

To further confirm that Ansible recognizes the inventory is present, you can use the command:

```code
ansible-inventory --list -y
```

```code
ansible-inventory --list -y
all:
  children:
    CiscoLive:
      children:
        Amsterdam:
          hosts:
            198.18.3.106: {}
        LasVegas:
          hosts:
            198.18.3.100: {}
            198.18.3.101: {}
        Melbourne:
          hosts:
            198.18.3.104: {}
            198.18.3.105: {}
    RiodeJaneiro:
      hosts:
        198.18.1.10: {}
    ungrouped: {}
```

The result of this command should show you the list which you just created in INI format.
Now one thing which you may be thinking is that the formatting is different.
The reason for the change in formatting is that the -y flag prints the inventory our in YAML format for you.
This can be helpful for you when trying to become more familiar with the syntax usage with YAML.
One further action that can be performed to confirm if ansible is reading the inventory correctly, is the ability to search for a specific host, this is particularly useful in large environments, where ansible may be managing 1000s of systems.
To search for a specific node in the inventory the below syntax can be used:

```code
 ansible 198.18.3.106 --list-hosts
 ```

 ```code
  hosts (1):
    198.18.3.106
```

The resulting output confirms if there is an inventory file match for the selected host or not.

## Step 4: Node Variables

When automating systems in Ansible it is not uncommon to have different usernames, passwords, or even network protocol ports that should be used when trying to connect.
In this exercise we are going to explore the different methods that variables can be allocated to systems.

### Inline within Inventory File

In the previous section the method which was used or variable assignment allows for the operator to control a broad range of variables that may be specific to a specific host.
Directly next to the host the variables which are desired for that host should be populated in.
As we just observed, we only have three variables which we intend to deploy, which isn’t a significant amount.
Therefore we are going to look at other options to allocate these parameters fo your systems, one of which is inline variable allocation within your inventory file itself.
For this part of the configuration we are going to be focusing on DC-EDGE2 (198.18.3.101).
Using your favorite editor, open up the inventory file again.
This time editing the line where DC-EDGE2 is located, before the # symbol

IMPORTANT!! Please note, that although the example below shows multiple lines being used, this is wordwrapped, do not press carriage return when entering variables, all content must remain on the one line.

```yml
<OTHER LINES REDACTED FOR BREVITY>
[LasVegas]
198.18.3.100   #DC-EDGE1
198.18.3.101 ansible_user=admin ansible_ssh_pass=admin ansible_network_os=ios   #DC-EDGE2
<OTHER LINES REDACTED FOR BREVITY>
```

### Group Based Variables in Inventory

The former two methods which were showcased were very host specifc, making use of the inline configuration in the inventory and the host_vars configurations.
If however you have common parameters which should be used for numerous hosts at once, you can vastly simplify the applied variables by allocating them directly to a group in the inventory.

Using your editor, open up the inventory file again, and add the following content to the bottom of the file:

```code
vim inventory
```

```yml
[Melbourne:vars]
ansible_user=admin
ansible_ssh_pass=admin
ansible_network_os=ios
```

These variables will now be used for access to systems which are located under the Melbourne portion of the hierarchy upon execution, assuming that there is no more specific variable to override them.

## Step 5: Executing an Ad-Hoc Task

Sometimes in Ansible you want to do some basic verifications without the need to execute a complete playbook. To achieve this we execute what is referred to as an ad-hoc tasks.
Using the syntax below, walk through your inventory sections and attempt execution of a single CLI command:

```code
ansible LasVegas --limit 198.18.3.101 -m raw -a 'show ver | i Cisco IOS Software'
```

In the above example, we are choosing to select hosts from the inventory file under the section [LasVegas] whilst limiting the selection of hosts to a single device “198.18.3.101”.
The execution is leveraging one of the bulit-in modules from ansible called ‘raw’, this module provides limited feedback and error checking, hence usually more useful for interaction with embedded systems.

```code
198.18.3.101 | CHANGED | rc=0 >>
Restricted Use
Cisco IOS Software [Cupertino], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.9.2a, RELEASE SOFTWARE (fc4)
Un authorised Logins trackedShared connection to 198.18.3.100 closed.
```

## Step 6: Deploying your first playbook  

Make sure that you are in your Ansible-Lab root directory (the directory which has your ansible.cfg file):

```code
cd /home/lab/Ansible-Lab/
```

### Create Directory Structure For Playbooks

From this location, go ahead and create a new directory called tasks
After creating the new directory, navigate into that portion of the hierarchy and create a new file called cedge_verify.yml :

```code
mkdir tasks
```

```code
cd /home/lab/Ansible-Lab/tasks/
```

```code
touch cedge_verify.yml
```

### Creating your first Playbook

The tasks directory which you just created is where we are going to place your playbooks which are written in the YAML format.
Using an editor open up the cedge_verify.yml file which you created in the tasks directory and add the below content into the file.
YAML format has a strict requirement in terms of hierarchy and spacing, so please be mindful of the indentations when adding the content:

```code
vim cedge_verify.yml
```

```yml
- name: C-Edge Verifications
  hosts: CiscoLive
  connection: network_cli
  gather_facts: no
```

After configuring the playbook file, go back to your Ansible-Lab directory and execute the below command:

```code
cd ..
```

```code
ansible-playbook tasks/cedge_verify.yml
```

Upon execution you should see the following output:

```code
PLAY [C-Edge Verifications] ********************************************************************

PLAY RECAP *********************************************************************
```

Congratulations!!!
You successfully executed an Ansible Playbook, now… this is a great first step, but actually you didn’t really do anything, aside from verify that the syntax was valid.
Now, time to start doing more elaborate steps by adding your first play.

### Adding your first Plays

Open up the existing cedge_verify.yml file and under the existing content, APPEND a new section called tasks:  
This is where we configure our different routines which are referred to as plays.
Looking below you can see that individual plays are listed: tasks:

```code
cd tasks
```

```code
vim cedge_verify.yml
```

```Ensure the paste the below from the start of a new line to maintain the indentation```

```yml
  tasks:

    - name: GATHERING FACTS
      ios_facts:
        gather_subset: min

    - name: run show sdwan control connections
      ios_command:
        commands: show sdwan control connections
      register: sdwanctlcon

    - name: display Connections
      debug:
        var: sdwanctlcon["stdout_lines"][0]

    - name: run show sdwan bfd session
      ios_command:
        commands: show sdwan bfd session
      register: bfdsessions

    - name: display bfd session status
      debug:
        var: bfdsessions["stdout_lines"][0]
```

After saving the above configurations, it is time to go ahead and execute your playbook again.
This time, with the added tasks present, you should observe a more extensive output, sharing the results of the commands which were executed on each system.

```code
cd ..
```

```code
ansible-playbook tasks/cedge_verify.yml
```

![postman](/images/an.png)

Looking above – we can see a mix of failed and successful sessions.
For the sessions which have failed, the credentials and the network operating system was missing.
Please go ahead and edit the inventory file to actualize these parameters and run the playbook again.
With that task complete, we have concluded the section of using Ansible for IOS-XE CLI interaction. Feel free to adjust the plays present to match up with further commands which may be relevant to your operational landscape and test them out.

* [Main Menu](/README.md/#table-of-content)
