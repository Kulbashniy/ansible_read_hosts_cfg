# ansible_read_hosts_cfg
This rep include files to setup, start, stop project. Read hosts project-data and save localy in sqlite db.

# Pre-requirements
You need already install Ansible>=2.8, configure it and have configure hosts. Ansible should work on Python 3.

# Setup
Run bash-script ***setup.sh*** it should run from the dir with this script and as sudo-user.
*setup.sh* have one optional positional argument - ansible roles dir
By default path to roles dir - **/etc/ansible/roles**
> Ex. ***sudo ./setup.sh /path/to/roles/dir***
It will be create a role in roles dir with all needed files. 
By defaults:
- Role name - **manage_build_data**
- DB path - **.../"role_name"/support_files/db**
- DB name - **buildinfo.db**

# Configure
First if you setup not default role dir - change **tasks/main.yml**
> Replace all lines **path_to_cfg: '_your/path_/manage_build_data/support_files/config.txt'**

You can use **start.yml** file in repo to start project or create new **.yml** file.

Basic *start.yml* looks:
- hosts: ***your_host_group***
  environment:
    PYTHONPATH: ***"/path/to/roles/manage_build_data/support_files"***
  roles:
    - role: manage_build_data
      path_yml: ***path/to/yml/files/on/hosts/name.yml***

> You dont need to change PYTHONPATH in *start.yml* if you setup with default roles path (setup without argument)

# Usage
Run:
> *ansible-playbook start.yml*
Its save configurations current hosts in DB.

To recieve all data by *build range* use **-e "build=11-14"**
> Ex. *ansible-playbook start.yml -e "build=11-14"*

To recieve all data by *hash sha1* use **-e "hash=6ac7653bd0a0a09d"**
> Ex. *ansible-playbook start.yml -e "hash=6ac7653bd0a0a09d"*

You can use the both *extra-vars*
> Ex. *ansible-playbook start.yml -e "build=11-14 hash=6ac7653bd0a0a09d"*
