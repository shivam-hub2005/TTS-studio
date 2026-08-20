# Simple TTS Studio

A beginner-friendly Text-to-Speech web app using Flask + Edge TTS.

## Features
- Hindi, English and Chinese voices
- Speed control
- MP3 generation
- Audio preview
- MP3 download
- Mobile-friendly UI

## 1. Install Python
Use Python 3.10+.

## 2. Create a virtual environment

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install packages

```bash
pip install -r requirements.txt
```

## 4. Start the app

```bash
python app.py
```

Open:
http://127.0.0.1:5000

## Notes
Edge TTS uses Microsoft's online speech service. It is convenient for a personal/demo project, but check the service's current terms before using it commercially or at large scale.

For a production app, add authentication, rate limits, text quotas, cleanup of old audio files, and a proper cloud TTS provider or self-hosted TTS engine.
