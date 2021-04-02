import tempfile
from typing import Dict

import yaml


def dump_recipe_in_file(recipe_json: Dict, recipe_file: tempfile):
    with open(recipe_file.name, 'r') as config_file:
        yaml.dump(recipe_json, recipe_file)
        config = yaml.safe_load(config_file)
    return config
