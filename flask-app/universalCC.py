from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import json

from threading import Lock
from threading import Thread
from queue import Queue

import speech_recognition as sr
import pyaudio as pa

app = Flask(__name__)
async_mode = None

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()



# Audio/Recognizer vars/objects
p = pa.PyAudio()
r = sr.Recognizer()
audio_queue = Queue()

recognizer_on = True


# Recognizer Thread
def recognize_worker():
    # this runs in a background thread
    while recognizer_on or audio_queue.not_empty:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: break  # stop processing if the main thread is done

        # received audio data, now we'll recognize it using your choice of recogonizer (in this case VOSK)
        res = json.loads(r.recognize_vosk(audio))['text']
        socketio.emit('my_response',
                    {'data': res})

        audio_queue.task_done()  # mark the audio processing job as completed in the queue


# Listener Thread
def listen_worker(dev_index):
    # this runs in a background thread
    with sr.Microphone(device_index=dev_index) as source:
        while recognizer_on:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            audio_queue.put(r.listen(source, phrase_time_limit=3))

    audio_queue.join()  # block until all current audio processing jobs are done
    audio_queue.put(None)  # tell the recognize_thread to stop



# Finds Stereo Mix device id by name
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
        dev_index = dev['index']

Thread(target=listen_worker, args=(dev_index,), daemon=True).start()
Thread(target=recognize_worker, daemon=True).start()


@app.route("/")
def hello_world():
    return render_template('index.html',async_mode=socketio.async_mode)


@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

if __name__ == '__main__':
    socketio.run(app)