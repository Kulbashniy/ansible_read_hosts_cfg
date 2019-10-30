from ansible.module_utils.basic import AnsibleModule
import yaml
import json
from db_module import Sqlite_DB

def main():
    module = AnsibleModule(
        argument_spec=dict(
            hash=dict(type='str', required=True),
            path_to_cfg=dict(type='str', required=True)
        ),
        supports_check_mode=True
    )
    req_path = module.params['path_to_cfg']
    req_hash = module.params['hash']
    result = dict({'changed': False, 'hash': req_hash, 'path_to_cfg': req_path})
    # No changes only find
    try:
        db = Sqlite_DB(req_path)
        # return dict of all_data by hash
        result = db.find_hash(req_hash) # kwargs: start=x, end=y; args: [start, end]
        # db.find_build(start=build_range[0], end=build_range[1])
        db.disconnect()
    except:
        module.fail_json(msg='Database connection failed', **result)
    module.exit_json(**result)

if __name__ == '__main__':
    main()