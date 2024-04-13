from flask import Flask
from matplotlib import pyplot as plt
import numpy as np
import pyaudio
import threading
import time
import whisper

app = Flask(__name__)


class AudioRecordingThread(threading.Thread):
    RATE = 16000
    CHUNKSIZE = int(RATE * 0.5)
    MAX_SECONDS = 30

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
        for _ in range(int(AudioRecordingThread.MAX_SECONDS * AudioRecordingThread.RATE / AudioRecordingThread.CHUNKSIZE)):
            if self._stop_event.is_set():
                break
            chunks.append(record_audio_chunk())

        stream.stop_stream()
        stream.close()

        self.audio = np.concatenate(chunks)

    def get_audio(self):
        return self.audio[5000:]

    def stop(self):
        self._stop_event.set()


heartbeat_thread = None
model = whisper.load_model('base.en')


@app.route('/start')
def start():
    global heartbeat_thread
    heartbeat_thread = AudioRecordingThread()
    heartbeat_thread.start()
    return {'status': 'ok', 'msg': 'recording started'}


@app.route('/end')
def end():
    global heartbeat_thread
    if heartbeat_thread:
        heartbeat_thread.stop()
        heartbeat_thread.join()
        result = model.transcribe(heartbeat_thread.get_audio())
        return {'status': 'ok', 'result': result['text']}
    else:
        return {'status': 'error', 'msg': 'not recording, you have to call /start first'}


if __name__ == '__main__':
    app.run(debug=True)
