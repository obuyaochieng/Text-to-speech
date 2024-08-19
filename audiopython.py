import pyttsx3
import tkinter as tk
from tkinter import ttk, filedialog
import pyaudio
import wave

# Initialize the TTS engine
engine = pyttsx3.init()

# Get available voices and ensure there are seven distinct voices
all_voices = engine.getProperty('voices')
selected_voices = all_voices[:7]
voice_names = [voice.name for voice in selected_voices]

# Available emotions (we'll use rate and volume to simulate different emotions)
emotions = ["Neutral", "Happy", "Sad", "Angry", "Calm", "Excited", "Tired"]

# Function to speak the text with the selected voice, speed, and emotion
def speak_text():
    text = text_entry.get("1.0", tk.END).strip()
    selected_voice_name = voice_combobox.get()
    selected_emotion = emotion_combobox.get()
    speed = speed_scale.get()
    
    for voice in selected_voices:
        if voice.name == selected_voice_name:
            engine.setProperty('voice', voice.id)
            break
    
    # Set speech rate and volume based on emotion
    if selected_emotion == "Happy":
        engine.setProperty('rate', speed + 50)
        engine.setProperty('volume', 1.0)
    elif selected_emotion == "Sad":
        engine.setProperty('rate', speed - 50)
        engine.setProperty('volume', 0.5)
    elif selected_emotion == "Angry":
        engine.setProperty('rate', speed + 70)
        engine.setProperty('volume', 1.0)
    elif selected_emotion == "Calm":
        engine.setProperty('rate', speed - 30)
        engine.setProperty('volume', 0.7)
    elif selected_emotion == "Excited":
        engine.setProperty('rate', speed + 100)
        engine.setProperty('volume', 1.0)
    elif selected_emotion == "Tired":
        engine.setProperty('rate', speed - 70)
        engine.setProperty('volume', 0.3)
    else:
        engine.setProperty('rate', speed)
        engine.setProperty('volume', 1.0)
    
    engine.say(text)
    engine.runAndWait()

# Function to save the audio to a file
def save_audio():
    text = text_entry.get("1.0", tk.END).strip()
    selected_voice_name = voice_combobox.get()
    selected_emotion = emotion_combobox.get()
    speed = speed_scale.get()
    
    for voice in selected_voices:
        if voice.name == selected_voice_name:
            engine.setProperty('voice', voice.id)
            break
    
    # Set speech rate and volume based on emotion
    if selected_emotion == "Happy":
        engine.setProperty('rate', speed + 50)
        engine.setProperty('volume', 1.0)
    elif selected_emotion == "Sad":
        engine.setProperty('rate', speed - 50)
        engine.setProperty('volume', 0.5)
    elif selected_emotion == "Angry":
        engine.setProperty('rate', speed + 70)
        engine.setProperty('volume', 1.0)
    elif selected_emotion == "Calm":
        engine.setProperty('rate', speed - 30)
        engine.setProperty('volume', 0.7)
    elif selected_emotion == "Excited":
        engine.setProperty('rate', speed + 100)
        engine.setProperty('volume', 1.0)
    elif selected_emotion == "Tired":
        engine.setProperty('rate', speed - 70)
        engine.setProperty('volume', 0.3)
    else:
        engine.setProperty('rate', speed)
        engine.setProperty('volume', 1.0)

    # Save to file
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        engine.save_to_file(text, file_path)
        engine.runAndWait()

# Function to record voice
def record_voice():
    # Record audio from the microphone
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

    if not filename:
        return

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for the duration of the recording
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Create the main window
root = tk.Tk()
root.title("Text to Speech")

# Create a text entry widget
text_label = tk.Label(root, text="Enter text:")
text_label.pack(pady=5)
text_entry = tk.Text(root, height=10, width=50)
text_entry.pack(pady=5)

# Create a dropdown for voice selection
voice_label = tk.Label(root, text="Select voice:")
voice_label.pack(pady=5)
voice_combobox = ttk.Combobox(root, values=voice_names)
voice_combobox.current(0)  # Set the default selection to the first voice
voice_combobox.pack(pady=5)

# Create a scale for voice speed
speed_label = tk.Label(root, text="Voice speed:")
speed_label.pack(pady=5)
speed_scale = tk.Scale(root, from_=50, to_=300, orient=tk.HORIZONTAL)
speed_scale.set(150)  # Set default speed
speed_scale.pack(pady=5)

# Create a dropdown for emotion selection
emotion_label = tk.Label(root, text="Select emotion:")
emotion_label.pack(pady=5)
emotion_combobox = ttk.Combobox(root, values=emotions)
emotion_combobox.current(0)  # Set the default selection to neutral emotion
emotion_combobox.pack(pady=5)

# Create a button to trigger speech
speak_button = tk.Button(root, text="Speak", command=speak_text)
speak_button.pack(pady=5)

# Create a button to save the audio
save_button = tk.Button(root, text="Save Audio", command=save_audio)
save_button.pack(pady=5)

# Button to record voice
record_button = tk.Button(root, text="Record Voice", command=record_voice)
record_button.pack(pady=5)

# Run the main loop
root.mainloop()
