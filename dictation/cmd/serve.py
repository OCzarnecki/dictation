from flask import Flask
import numpy as np
import pyaudio
import threading
import whisper
import logging
import os

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame  # noqa

app = Flask(__name__)
audio_recording_thread = None
model = None


class AudioRecordingThread(threading.Thread):
    RATE = 16000
    CHUNKSIZE = int(RATE * 0.5)
    MAX_SECONDS = 120

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        def record_audio_chunk():
            data = stream.read(AudioRecordingThread.CHUNKSIZE)
            return np.frombuffer(data, dtype=np.float32)

        chunks = []
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=AudioRecordingThread.RATE,
            input=True,
            frames_per_buffer=AudioRecordingThread.CHUNKSIZE,
        )
        logging.info("Stared recording")
        for _ in range(int(AudioRecordingThread.MAX_SECONDS * AudioRecordingThread.RATE / AudioRecordingThread.CHUNKSIZE)):
            if self._stop_event.is_set():
                break
            chunks.append(record_audio_chunk())
        logging.info("Finished recording")

        stream.stop_stream()
        stream.close()

        self.audio = np.concatenate(chunks)

    def get_audio(self):
        return self.audio[int(AudioRecordingThread.RATE * 0.25):]

    def stop(self):
        self._stop_event.set()


def init_audio():
    pygame.init()
    pygame.mixer.init()


def play_mp3(file_name, block=False):
    resource_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../data/sfx/',
            file_name,
        )
    )
    pygame.mixer.music.load(resource_path)
    pygame.mixer.music.play()

    if block:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


@app.route('/start')
def start():
    global audio_recording_thread
    play_mp3('start.mp3', block=True)
    audio_recording_thread = AudioRecordingThread()
    audio_recording_thread.start()
    return {'status': 'ok', 'msg': 'recording started'}


@app.route('/end')
def end():
    global audio_recording_thread
    if audio_recording_thread:
        audio_recording_thread.stop()
        audio_recording_thread.join()
        result = model.transcribe(audio_recording_thread.get_audio())

        play_mp3('end.mp3', block=False)

        return {'status': 'ok', 'result': result['text']}
    else:
        return {'status': 'error', 'msg': 'not recording, you have to call /start first'}


@app.route('/state')
def state():
    global audio_recording_thread
    if audio_recording_thread is not None and not audio_recording_thread._stop_event.is_set():
        return {'status': 'ok', 'state': 'recording'}
    else:
        return {'status': 'ok', 'state': 'waiting'}


def run(args):
    global model
    model = whisper.load_model('base.en')
    init_audio()
    app.run(debug=args.debug)
