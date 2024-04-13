import requests
import logging
import pyperclip


def fetch_transcription(args) -> str:
    base_url = f"http://{args.host}:{args.port}/"
    result = requests.get(base_url + 'end')
    if not result.ok:
        return 1

    json_response = result.json()
    if 'status' not in json_response or json_response['status'] != 'ok':
        logging.error(f"Response status was not ok. Response: {json_response}")
        return 1
    return json_response['result']


def run(args):
    transcription = fetch_transcription(args)
    logging.info(f"Heard {transcription}")
    pyperclip.copy(transcription)
    logging.info("Transcription copied into clipboard")
