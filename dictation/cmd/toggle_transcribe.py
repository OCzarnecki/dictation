import requests
import logging

import dictation.cmd.transcribe as transcribe
import dictation.cmd.record as record


def fetch_state(args) -> str:
    base_url = f"http://{args.host}:{args.port}/"
    result = requests.get(base_url + 'state')
    if not result.ok:
        return 1

    json_response = result.json()
    if 'status' not in json_response or json_response['status'] != 'ok':
        logging.error(f"Response status was not ok. Response: {json_response}")
        return 1
    return json_response['state']


def run(args):
    state = fetch_state(args)
    if state == 'waiting':
        record.run(args)
    elif state == 'recording':
        transcribe.run(args)
    else:
        raise ValueError(f"Unexpected state: {state}")
