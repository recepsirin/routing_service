import logging

import yaml


def config_parser():
    config = dict()
    with open("config.yml", 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            logging.error(exc)
    return config
