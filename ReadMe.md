
# Universal VR Closed Captions

## Authors

- [@maryharebear, UI/UX Design](https://github.com/maryharebear)
- [@BelaJatt, Frontend](https://github.com/BelaJatt)
- [@chrisandrade15, Frontend/API](https://github.com/chrisandrade15)
- [@Sean-OCallaghan, Frontend/Backend](https://github.com/Sean-OCallaghan)
- [@TheBeerex, Backend](https://github.com/TheBeerex)

## Features

- Live transcription of desktop audio
- Light/dark mode toggle
- Font type/size options

## Usage/Installation

Note: Requires RealTek Audio drivers to be installed in a Windows machine. Program specifically uses the RealTek Audio Stereo Mix recording device. Desktop audio should be routed to the RealTek Audio playback device to function.

1. Clone the repo

2. Install Python3 and the necessary libraries (via pip): PyAudio, SpeechRecognition, Vosk, Flask, and SocketIO

3. Run the project

```bash
  cd flask-app
  flask run
```

4. Open the frontend from the IP given by flask or with <http://localhost:3000/>.
