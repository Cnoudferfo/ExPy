import pyaudio
import whisper
import numpy as np
import threading
import tkinter as tk
from tkinter import scrolledtext

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Load Whisper model
model = whisper.load_model("base")

# Function to transcribe audio
def transcribe_audio(audio_data):
    audio_array = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
    result = model.transcribe(audio_array)
    return result['text']

# Function to record and transcribe audio in real-time
def record_and_transcribe():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording and transcribing...")

    try:
        while running:
            # Capture audio chunk
            data = stream.read(CHUNK)
            # Transcribe audio chunk
            transcription = transcribe_audio(data)
            # Update the GUI with the transcription
            text_area.insert(tk.END, transcription + '\n')
            text_area.see(tk.END)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Function to start the ASR thread
def start_asr():
    global running
    running = True
    thread = threading.Thread(target=record_and_transcribe)
    thread.start()

# Function to stop the ASR thread
def stop_asr():
    global running
    running = False
    root.quit()

# Create the GUI
root = tk.Tk()
root.title("Real-Time ASR with Whisper")

# Create a text area to display transcriptions
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
text_area.pack(padx=10, pady=10)

# Create a quit button
quit_button = tk.Button(root, text="Quit", command=stop_asr)
quit_button.pack(pady=10)

# Start the ASR when the GUI starts
start_asr()

# Run the GUI event loop
root.mainloop()
