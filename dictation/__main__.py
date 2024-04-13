import argparse
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', default=5000, type=int)
    ap.add_argument('--host', default='localhost', type=str)

    subcommands = ap.add_subparsers(required=True)
    serve = subcommands.add_parser('serve', help='Start the transcription server')
    serve.set_defaults(cmd='serve')
    serve.add_argument('--debug', action='store_true')

    record = subcommands.add_parser('record', help='Start recording')
    record.set_defaults(cmd='record')

    transcribe = subcommands.add_parser('transcribe', help='Stop the current recording and transcribe it to the clipboard')
    transcribe.set_defaults(cmd='transcribe')

    toggle_transcribe = subcommands.add_parser('toggle_transcribe', help='Transcribe if recording, record if idle.')
    toggle_transcribe.set_defaults(cmd='toggle_transcribe')

    args = ap.parse_args()

    # Using local imports here so we don't import all of machine learning just to make web requests.
    match args.cmd:
        case 'serve':
            from dictation.cmd.serve import run
            return run(args)
        case 'record':
            from dictation.cmd.record import run
            return run(args)
        case 'transcribe':
            from dictation.cmd.transcribe import run
            return run(args)
        case 'toggle_transcribe':
            from dictation.cmd.toggle_transcribe import run
            return run(args)


if __name__ == '__main__':
    sys.exit(main())
