import json
from typing import Dict


def _dump_mce_in_file(mce_json: Dict, mce_file_path: str):
    with open(mce_file_path, 'w') as file:
        json.dump(mce_json, file)
