# /backend/app/utils/data_formatting.py

import json


def format_json(data):

    return json.dumps(data, indent=4, sort_keys=True)