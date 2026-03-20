# Perhaps Counter - Audio Transcript

A Python app that listens to your microphone, converts speech to text, and counts how many times the word perhaps appears.

## Overview

The script runs a live listener and sends each captured phrase to speech-to-text. It then checks the transcript and counts whole-word, case-insensitive matches for perhaps.

## Features

- Live microphone listening
- Transcript-based matching (not acoustic similarity)
- Whole-word matching for perhaps
- Interactive commands: status, reset, quit
- Running session count and duration

## Requirements

- Python 3.7+
- Microphone access
- Internet connection (Google speech recognition API is used by SpeechRecognition)

## Install

```bash
python3 -m pip install SpeechRecognition
```

## Run

```bash
python3 audio_perhaps_counter.py
```

## Usage

After startup, the app listens continuously.

Commands:
- status: show total matches and session time
- reset: clear count and session timer
- quit: stop listener and exit

## Notes

- Matching uses a regex equivalent to whole-word perhaps, case-insensitive.
- Examples that match: perhaps, Perhaps, PERHAPS
- Examples that do not match: perhapsing, perhaps.

## Troubleshooting

### Microphone issues

- Check OS microphone permissions.
- Make sure no other app is exclusively using the mic.

### Speech recognition errors

- Confirm internet connectivity.
- Retry if the API is temporarily unavailable.

### Dependency errors

Reinstall package:

```bash
python3 -m pip install --upgrade SpeechRecognition
```

## File

- audio_perhaps_counter.py: main script
