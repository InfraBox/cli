import json

from os.path import expanduser
from infraboxcli.log import logger
from pyinfrabox.utils import safe_open_w

config_file_path = '/.infrabox/config.json'
home = expanduser("~")


def set_current_project_name(args):
    from infraboxcli.dashboard import project
    all_projects = project.get_projects(args).json()

    project_exists = False
    for project in all_projects:
        if args.project_name == project['name']:
            project_exists = True
            break

    if not project_exists:
        logger.error('Project with such a name does not exist.')
        exit(1)

    try:
        config = get_config()

        config['remotes'][get_current_remote_url()]['current_project'] = args.project_name
        save_config(config)

        return True
    except:
        return False


def get_current_project_name(args):
    try:
        return get_config()['remotes'][get_current_remote_url()]['current_project']
    except:
        return None


def get_current_remote_url():
    try:
        return get_config()['current_remote']
    except:
        return None


def get_all_remotes():
    try:
        config = get_config()

        remotes = config['remotes'].keys()
        if not remotes:
            raise

        return remotes
    except:
        logger.error('No available remotes. Please, log in.')
        exit(1)


def get_config():
    try:
        with open(home + config_file_path, 'r') as config_file:
            config = json.load(config_file)

        return config
    except:
        return None


def save_config(config):
    try:
        with safe_open_w(home + config_file_path) as config_file:
            json.dump(config, config_file)

        return True
    except:
        return False
