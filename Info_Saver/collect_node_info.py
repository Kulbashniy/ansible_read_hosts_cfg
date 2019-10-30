from ansible.module_utils.basic import AnsibleModule
import yaml
import json

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path_to_yaml=dict(type='str', required=True, default=None),
        ),
        supports_check_mode=True
    )
    req_path = module.params['path_to_yaml']
    # Only read nothing to do, nothing to change
    result = dict({'changed': False, 'path_to_yaml': req_path})
    try:
        with open(req_path, 'r') as f:
            try:
                data = yaml.load(f.read(), Loader=yaml.Loader)
            except:
                module.fail_json(msg='File structure is invalid', **result)
            result.update({'data_list': data})
    except:
        module.fail_json(msg='File not found', **result)
        
    module.exit_json(**result)

if __name__ == '__main__':
    main()