import warnings
warnings.filterwarnings('ignore')

import re
import speech_recognition as sr
import threading
from datetime import datetime

class AudioTranscriptPerhapsCounter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.perhaps_count = 0
        self.running = False
        self.lock = threading.Lock()
        self.session_start = datetime.now()
        self.match_timestamps = []

        # Recognition tuning for better mic behavior in noisy environments.
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def count_perhaps_in_text(self, text):
        """Count case-insensitive whole-word matches of 'perhaps' in text."""
        return len(re.findall(r"\bperhaps\b", text, flags=re.IGNORECASE))

    def listen_and_process(self):
        """Continuously listen to microphone, transcribe, and count 'perhaps'."""
        with sr.Microphone() as source:
            print("🎤 Audio listener started...")
            print("   (Calibrating microphone...)")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("   ✅ Calibration complete!\n")

            while self.running:
                try:
                    print("⏳ Listening...", end="", flush=True)
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    print(" ✓ Got audio!", flush=True)

                    try:
                        transcript = self.recognizer.recognize_google(audio)
                    except sr.UnknownValueError:
                        print("⚠️  Could not understand speech\n")
                        continue
                    except sr.RequestError as e:
                        print(f"❌ Speech service error: {e}\n")
                        continue

                    print(f"📝 Transcript: {transcript}")
                    matches = self.count_perhaps_in_text(transcript)

                    if matches:
                        with self.lock:
                            self.perhaps_count += matches
                            for _ in range(matches):
                                self.match_timestamps.append({'timestamp': datetime.now()})
                        print(f"✅ Found {matches} match(es). Total: {self.perhaps_count}\n")
                    else:
                        print("⚠️  No match\n")

                except sr.WaitTimeoutError:
                    print(" ⏱️ (timeout)", flush=True)
                except Exception as e:
                    print(f"\n❌ Listener error: {e}")
    
    def start(self):
        """Start audio transcription listener and handle commands."""
        self.running = True
        listener_thread = threading.Thread(target=self.listen_and_process, daemon=True)
        listener_thread.start()

        print("🎙️  Transcript mode started.")
        print("   Speak into your microphone.")
        print("   Commands: 'status', 'reset', 'quit'\n")

        try:
            while self.running:
                user_input = input("(Commands: 'status', 'reset', 'quit'): ").strip()
                command = user_input.lower()
                
                if command == 'status':
                    elapsed = datetime.now() - self.session_start
                    print(f"\n📊 Status:")
                    print(f"   Total matches: {self.perhaps_count}")
                    print(f"   Session time: {elapsed}\n")
                    
                elif command == 'reset':
                    with self.lock:
                        self.perhaps_count = 0
                        self.match_timestamps.clear()
                        self.session_start = datetime.now()
                    print("🔄 Counter reset!\n")
                    
                elif command == 'quit':
                    self.running = False
                    print("\n👋 Stopping listener...")
                    break
                elif command:
                    print("⚠️  Unknown command. Use 'status', 'reset', or 'quit'.\n")
                    
        except KeyboardInterrupt:
            self.running = False
            print("\n👋 Stopping listener...")
    
    def get_stats(self):
        """Get current statistics"""
        with self.lock:
            elapsed = datetime.now() - self.session_start
            return {
                'total_matches': self.perhaps_count,
                'session_duration': elapsed
            }


def main():
    print("🎙️  Perhaps Counter - Audio Transcript")
    print("=" * 40)
    
    counter = AudioTranscriptPerhapsCounter()
    
    try:
        counter.start()
    finally:
        stats = counter.get_stats()
        print("\n" + "=" * 40)
        print(f"📈 Final Count: {stats['total_matches']}")
        print(f"   Session duration: {stats['session_duration']}")
        print("=" * 40)


if __name__ == "__main__":
    main()
