import requests
import logging


def run(args):
    base_url = f"http://{args.host}:{args.port}/"
    result = requests.get(base_url + 'start')
    if not result.ok:
        return 1

    json_response = result.json()
    if 'status' not in json_response or json_response['status'] != 'ok':
        logging.error(f"Response status was not ok. Response: {json_response}")
        return 1
