import yaml


class Config(object):
    def __init__(self, config_data):
        for key, value in config_data.items():
            setattr(self, key, value)


def get_config(config_path: str):

    with open(config_path, 'r') as c:
        config = yaml.safe_load(c)

    config_obj = Config(config)
    return config_obj
