import warnings
warnings.filterwarnings('ignore')

import speech_recognition as sr
import threading
from datetime import datetime
import librosa
import numpy as np
from scipy.spatial.distance import cosine

class AudioWhatCounter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.similarity_count = 0
        self.running = False
        self.lock = threading.Lock()
        self.session_start = datetime.now()
        self.similarity_matches = []
        
        # Adjust recognizer settings for better performance
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Load reference audio
        self.reference_features = None
        self.load_reference_audio("what.m4a")
    
    def load_reference_audio(self, audio_path):
        """Load and extract features from reference audio file"""
        try:
            # Load the audio file
            y, sr_rate = librosa.load(audio_path, sr=None)
            
            # Extract MFCC features (Mel-frequency cepstral coefficients)
            mfcc = librosa.feature.mfcc(y=y, sr=sr_rate, n_mfcc=13)
            
            # Calculate mean of the features
            self.reference_features = np.mean(mfcc, axis=1)
                        
        except Exception as e:
            print(f"❌ Could not load reference audio: {e}")
            print(f"   Make sure 'what.m4a' exists in the current directory")
            raise
    
    def calculate_audio_similarity(self, audio_data):
        """Compare audio features to reference audio"""
        if self.reference_features is None:
            return None
        
        try:
            # Convert audio data to numpy array
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16).astype(np.float32)
            
            # Normalize
            audio_array = audio_array / 32768.0
            
            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=audio_array, sr=audio_data.sample_rate, n_mfcc=13)
            current_features = np.mean(mfcc, axis=1)
            
            # Calculate cosine distance (0 = identical, 1 = completely different)
            similarity = 1 - cosine(self.reference_features, current_features)
            
            return similarity
            
        except Exception as e:
            return None
    
    def listen_and_process(self):
        """Continuously listen to microphone and process audio"""
        with sr.Microphone() as source:
            print("🎤 Audio listener started...")
            print("   (Calibrating microphone...)")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("   ✅ Calibration complete!\n")
            
            while self.running:
                try:
                    print("⏳ Listening...", end="", flush=True)
                    audio = self.recognizer.listen(
                        source, 
                        timeout=10,
                        phrase_time_limit=15
                    )
                    print(" ✓ Got audio!", flush=True)
                    
                    # Check audio similarity to reference
                    similarity_score = self.calculate_audio_similarity(audio)
                    
                    if similarity_score is not None and similarity_score >= 0.90:
                        with self.lock:
                            self.similarity_count += 1
                            self.similarity_matches.append({
                                'timestamp': datetime.now()
                            })
                        print(f"✅ What Identified! | Total: {self.similarity_count}\n")
                    else:
                        print("⚠️  No match\n")
                        
                except sr.WaitTimeoutError:
                    print(" ⏱️ (timeout)", flush=True)
                    pass
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"\n❌ Error: {e}")
    
    def start(self):
        """Start the listener in a background thread"""
        self.running = True
        listener_thread = threading.Thread(target=self.listen_and_process, daemon=True)
        listener_thread.start()
        
        # Main thread for user interaction
        try:
            while self.running:
                user_input = input("(Commands: 'status', 'reset', 'quit'): ").lower().strip()
                
                if user_input == 'status':
                    elapsed = datetime.now() - self.session_start
                    print(f"\n📊 Status:")
                    print(f"   Total matches: {self.similarity_count}")
                    print(f"   Session time: {elapsed}\n")
                    
                elif user_input == 'reset':
                    with self.lock:
                        self.similarity_count = 0
                        self.similarity_matches.clear()
                        self.session_start = datetime.now()
                    print("🔄 Counter reset!\n")
                    
                elif user_input == 'quit':
                    self.running = False
                    print("\n👋 Stopping listener...")
                    break
                    
        except KeyboardInterrupt:
            self.running = False
            print("\n👋 Stopping listener...")
    
    def get_stats(self):
        """Get current statistics"""
        with self.lock:
            elapsed = datetime.now() - self.session_start
            return {
                'total_matches': self.similarity_count,
                'session_duration': elapsed
            }


def main():
    print("🎙️  What Counter - Audio Listener")
    print("=" * 40)
    
    counter = AudioWhatCounter()
    
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
