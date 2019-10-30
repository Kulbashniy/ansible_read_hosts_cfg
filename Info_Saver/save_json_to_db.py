from ansible.module_utils.basic import AnsibleModule
import yaml
import json
import sys
from db_module import Sqlite_DB

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path_to_cfg=dict(type='str', required=True, default=None),
            node_inf=dict(type='dict', required=True)
        ),
        supports_check_mode=True
    )
    req_path = module.params['path_to_cfg']
    req_inf = module.params['node_inf']
    result = dict({'changed': False, 'path_to_cfg': req_path, 'node_json': req_inf})
    # Probably change the db-file
    try:
        db = Sqlite_DB(req_path)
        for record in req_inf['data_list']:
            record_status = db.status(record)
            if record_status == 'update':
                db.update(record)
                result.update({'changed': True})
            elif record_status == 'insert':
                db.insert(record)
                result.update({'changed': True})
            elif record_status == 'ok':
                pass
            else:
                module.fail_json(msg='Fail when save/update record', **result)
        db.disconnect()
    except:
        module.fail_json(msg='Database connection failed', **result)
    module.exit_json(**result)

if __name__ == '__main__':
    main()