import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def read_config(location = 'components.yaml'):
    f = open(location)
    data = yaml.load(f, Loader)
    return data
