import json
import sys


def get_command_folder():
    folder = ""
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    return folder


def get_json_str(obj):
    jsonStr = json.dumps(obj, indent=4, sort_keys=True)
    return jsonStr
