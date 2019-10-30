# ansible_read_hosts_cfg
This rep include files to setup, start, stop project. Read hosts project-data and save localy in sqlite db.

# Pre-requirements
You need already install Ansible>=2.8, configure it and have configure hosts. Ansible should work on Python 3.

# Setup
Run bash-script ***setup.sh*** it should run from the dir with this script and as sudo-user.
By default path to roles dir - **/etc/ansible/roles**
> Ex. ***sudo ./setup.sh***
 > Ex. ***sudo ./setup.sh /path/to/roles/dir***
It will be create a role in roles dir. Role name - **manage_build_data**

# Configure

# Usage
