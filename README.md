# Dictation
Utilities for AI-based dictation.

# Installation

Pull this repository & install the requirements. This will be some version of:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Usage
Start the server with

```
python -m dictation serve
```

You might want to make sure this happens at startup.

To start/stop recording, run

```
python -m dictation toggle_transcribe
```

I have bound this to Mod4+BackSpace using i3:

```
bindsym $mod+BackSpace exec "bash -c 'cd $HOME/develop/dictation ; ./.venv/bin/python -m dictation toggle_transcribe'"
```

The `cd` is important because the voice model will be cached in the installation directory.

# Acknowledgements

This project uses [whisper](https://github.com/openai/whisper) by OpenAI for language transcription.

Sound effects created by user `neuzai` of [freesound.org](https://freesound.org/people/nezuai/).
