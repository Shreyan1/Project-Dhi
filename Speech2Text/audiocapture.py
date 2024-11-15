import sounddevice as sd
import numpy as np
import wave
import tempfile
from transformers import pipeline
import threading
import time
import os
import warnings

warnings.filterwarnings('ignore')  # Suppress all other warnings
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'  # Suppress transformer warnings

MODELNAME_WHISPER = "openai/whisper-tiny.en"
SAMPLE_RATE = 16000

class LiveTranscriber:
    def __init__(self, model_name=MODELNAME_WHISPER, sample_rate=SAMPLE_RATE):
        self.model = pipeline("automatic-speech-recognition", model=model_name)
        self.sample_rate = sample_rate
        self.temp_dir = tempfile.mkdtemp()
        self.is_recording = False

    def record_audio(self, duration=10):
        """Record audio for a fixed duration with an option to stop early."""
        print(f"Recording for up to {duration} seconds... Press Enter to stop early.")
        audio_data = []
        self.is_recording = True
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(f'Status: {status}')
            audio_data.append(indata.copy())

        # Separate thread to listen for "Enter" key to stop early
        def stop_recording():
            input()  # Wait for Enter
            print("\nRecording stopped early by user.")
            self.is_recording = False

        # Start the stop-recording thread
        stop_thread = threading.Thread(target=stop_recording)
        stop_thread.start()

        # Begin audio recording
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=self.sample_rate, dtype=np.float32):
            start_time = time.time()
            while self.is_recording and time.time() - start_time < duration:
                time.sleep(0.1)  # Giving a small sleep to prevent high CPU usage

        stop_thread.join()  # Ensure stop thread has completed

        # Concatenate audio data if recording was successful
        if audio_data:
            audio_data = np.concatenate(audio_data, axis=0)
            temp_file = os.path.join(self.temp_dir, "temp_audio.wav")
            self.save_audio(audio_data, temp_file)
            return temp_file
        else:
            print("No audio recorded.")
            return None

    def save_audio(self, audio_data, filename):
        """Save audio data to WAV format."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # Set sample width for int16 format
            wf.setframerate(self.sample_rate)
            wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

    def transcribe_audio(self, audio_file):
        """Transcribe audio and clean up temporary file."""
        if audio_file:
            print("Transcribing...")
            result = self.model(audio_file)
            print("Transcription:", result["text"])
            # Clean up temporary file after transcription
            os.remove(audio_file)

    def cleanup(self):
        """Clean up temporary directory."""
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)

    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup()

def main():
    transcriber = LiveTranscriber()
    
    try:
        while True:
            # Record audio with the option to stop # Clean up temporary file after transcription
            audio_file = transcriber.record_audio(duration=10)
            
            # Transcribe the recorded audio in a separate thread
            if audio_file:
                transcription_thread = threading.Thread(target=transcriber.transcribe_audio, args=(audio_file,))
                transcription_thread.start()
                transcription_thread.join()
            
            # Ask user if they want to record again
            choice = input("\nPress Enter to record again or 'q' to quit: ")
            if choice.lower() == 'q':
                break

    finally:
        transcriber.cleanup()

if __name__ == "__main__":
    main()
