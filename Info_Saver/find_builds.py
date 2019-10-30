from ansible.module_utils.basic import AnsibleModule
import yaml
import json
from db_module import Sqlite_DB

def main():
    module = AnsibleModule(
        argument_spec=dict(
            builds_range=dict(type='str', required=True),
            path_to_cfg=dict(type='str', required=True)
        ),
        supports_check_mode=True
    )
    req_path = module.params['path_to_cfg']
    req_builds = module.params['builds_range']
    result = dict({'changed': False, 'builds_range': req_builds, 'path_to_cfg': req_path})
    # No changes only find
    try:
        db = Sqlite_DB(req_path)
        build_range = req_builds.split('-')
        # return dict of all_data by builds
        result = db.find_build(build_range) # kwargs: start=x, end=y; args: [start, end]
        # db.find_build(start=build_range[0], end=build_range[1])
        db.disconnect()
    except:
        module.fail_json(msg='Database connection failed', **result)
    module.exit_json(**result)

if __name__ == '__main__':
    main()