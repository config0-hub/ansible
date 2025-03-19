def default():
    """
    Define a default task for writing Ansible hosts.

    Returns:
        dict: A task configuration for shelloutconfig method.
    """
    task = {
        'method': 'shelloutconfig',
        'metadata': {
            'env_vars': [],
            'shelloutconfigs': ['config0-publish:::ansible::write_hosts']
        }
    }

    return task

