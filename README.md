# 🎙️ What Counter - Audio Listener

A Python application that listens to live audio and counts instances of spoken words that sound similar to a reference text.

## Overview

This program continuously monitors your microphone and compares incoming audio against a reference text. When it detects audio that matches the text input, it increments a counter and logs the match.

### Key Features

- 🎤 **Real-time audio listening** from your microphone
- 📊 **Live counter** displaying matches as they occur
- 💾 **Session statistics** with total match count and duration
- 🔧 **Interactive commands** for status, reset, and quit

## Prerequisites

- Python 3.7 or higher
- A microphone connected to your computer

## Installation

### 1. Install Python 3

Make sure you have Python 3 installed. Check your version:

```bash
python3 --version
```

### 2. Install Required Dependencies

Run the following command to install all required Python packages:

```bash
python3 -m pip install SpeechRecognition
```

Breaking down the packages:
- **SpeechRecognition** - For audio recording from microphone

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tanyaeveritt/what_counter.git
cd what_counter
```

### 2. Install Dependencies

```bash
python3 -m pip install SpeechRecognition
```

### 3. Run the Program

```bash
python3 audio_what_counter.py
```

## Usage

### Interactive Commands

Once the program is running, use these commands at the prompt:

- **`status`** - Display current match count and session duration
- **`reset`** - Clear the counter and start fresh
- **`quit`** - Stop listening and exit the program

### Example Session

```
🎙️  What Counter - Audio Listener
========================================
✅ Reference audio loaded from: what.m4a

⏳ Listening... ✓ Got audio!
✅ MATCH! | Total: 1

⏳ Listening... ✓ Got audio!
⚠️  No match

(Commands: 'status', 'reset', 'quit'): status

📊 Status:
   Total matches: 1
   Session time: 0:00:15.234567

(Commands: 'status', 'reset', 'quit'): quit

👋 Stopping listener...
========================================
📈 Final Count: 1
   Session duration: 0:00:20.456789
========================================
```

## How It Works

3. **Listening**: Continuously listens for text input from your microphone in real-time
5. **Counting**: If trascribe finds text input, increments the counter and logs the match
6. **Feedback**: Displays real-time feedback about matches and no-matches

## Troubleshooting

### "ModuleNotFoundError" when running the script

Make sure all dependencies are installed:
```bash
python3 -m pip install SpeechRecognition
```

Verify installation:
```bash
python3 -m pip list
```

### Microphone not detected

- Check that your microphone is connected and working
- Verify microphone permissions:
  - **macOS**: System Preferences → Security & Privacy → Microphone
  - **Windows**: Settings → Privacy & security → Microphone
  - **Linux**: Check ALSA or PulseAudio settings
- Try using a different microphone or USB audio device

### WaitTimeoutError or listening issues

- Move closer to your microphone
- Reduce background noise in your environment
- The app will automatically retry on timeout
- Adjust microphone sensitivity in your OS settings

### Program crashes or hangs

- Make sure you have enough free RAM
- Close other applications using the microphone
- Try restarting the program
- Check for updates to Python and dependencies

## File Structure

```
what_counter/
├── audio_what_counter.py    # Main program
├── README.md                # This file
└── .gitignore               # (optional) Git ignore file
```

## System Requirements

| Requirement | Specification |
|-----------|---------------|
| **OS** | macOS, Windows, or Linux |
| **Python** | 3.7 or higher |
| **RAM** | 512 MB minimum |
| **Storage** | 100 MB for dependencies |
| **Microphone** | Any standard audio input device |

## Performance Notes

- The first run may take a few seconds to load and calibrate the microphone
- Accuracy depends on microphone quality and environment noise levels
- Processing happens in real-time with minimal latency

## License

This project is open source and available for personal use.

## Author

Created by Tanya Everitt

## Support

If you encounter issues:

1. Verify all dependencies are installed:
   ```bash
   python3 -m pip list
   ```
   
2. Check microphone permissions and connectivity

3. Try running with a quieter environment

4. Check the [Troubleshooting](#troubleshooting) section above

5. Open an issue on GitHub if the problem persists

## Contributing

Feel free to fork this repository and submit pull requests with improvements!

