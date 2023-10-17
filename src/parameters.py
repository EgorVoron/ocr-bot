import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config_path", type=str, help=".txt file with token", default="config.json"
)
args = parser.parse_args()

config_path = args.config_path
with open(config_path, "r+") as config_file:
    parameters: dict = json.loads(config_file.read())
