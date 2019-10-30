#!/bin/bash
# Default paths
current_path=$(pwd)
roles_path='/etc/ansible/roles'
role_name='manage_build_data'
db_path=$roles_path/$role_name'/support_files/db'
db_name='buildinfo.db'



# Copy Ansible modules to dir with Ansible modules
if [ -z "$1" ]
then
	echo 'used default roles path: '$roles_path
	echo 'used default role name: '$role_name
	echo 'used default database path: '$db_path
else
	echo 'used default role name: '$role_name
	roles_path=$1
	# role_name=X
	# db_name=X
	db_path=$roles_path/$role_name'/support_files/db'
	echo 'used user roles path: '$roles_path
fi
# Create roles dir
mkdir -p $roles_path

# Create role with dir struct
ansible-galaxy init $role_name --init-path=$roles_path

# Copying custom modules to library dir
mkdir -p $roles_path/$role_name/library
cp $current_path/collect_node_info.py $roles_path/$role_name/library
cp $current_path/save_json_to_db.py $roles_path/$role_name/library
cp $current_path/find_builds.py $roles_path/$role_name/library
cp $current_path/find_hash.py $roles_path/$role_name/library

# Create config file key=value with paths and names
mkdir -p $roles_path/$role_name/support_files
touch $roles_path/$role_name/support_files/config.txt
chmod 664 $roles_path/$role_name/support_files/config.txt
config_file=$roles_path/$role_name'/support_files/config.txt'

# Adding tasks
sed '/path_to_cfg:/c\    path_to_cfg: '$config_file main.yml > $roles_path/$role_name/tasks/main.yml

# Copy support files (python scripts DB, DB file, config file) to dir support_files
# in Ansible role dir. Create an empty DB
mkdir -p $db_path
python3 $current_path/create_db.py $db_path $db_name
echo "db_path=$db_path" >> $config_file
echo "db_name=$db_name" >> $config_file
echo "roles_path=$roles_path" >> $config_file
echo "role_name=$role_name" >> $config_file
cp $current_path/sql_params.py $roles_path/$role_name/support_files
cp $current_path/db_module.py $roles_path/$role_name/support_files

chmod -R 777 $roles_path