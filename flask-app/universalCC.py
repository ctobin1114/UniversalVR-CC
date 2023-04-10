from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r'model')
recognizer = KaldiRecognizer(model,16000)
app = Flask(__name__)


cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels = 1, rate = 16000, input=True,frames_per_buffer=8192)
stream.start_stream()
async_mode = None

socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
import json



def background_thread():
    cap = pyaudio.PyAudio()
    stream = cap.open(format=pyaudio.paInt16, channels = 1, rate = 16000, input=True,frames_per_buffer=8192)
    stream.start_stream()

    def check(data):
        if recognizer.AcceptWaveform(data):
            res = json.loads(recognizer.Result())['text']
            socketio.emit('my_response',
                      {'data': res})
        
    while True:
        data = stream.read(10000)
        check(data)
            


@app.route("/")
def hello_world():
    return render_template('index.html',async_mode=socketio.async_mode)


@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('test_response', {'data': 'Test response sent'})

@socketio.on('broadcast_message')
def handle_broadcast(data):
    print('received: ' + str(data))
    emit('broadcast_response', {'data': 'Broadcast sent'}, broadcast=True)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    # emit('my_response', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
    socketio.run(app)