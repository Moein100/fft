import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import wave

# Function to open a file dialog and read a WAV file
def load_wav():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        with wave.open(file_path, 'r') as wav_file:
            # Extract audio data
            n_frames = wav_file.getnframes()
            audio_data = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)
            sampling_rate = wav_file.getframerate()
            entry_file_path.delete(0, tk.END)
            entry_file_path.insert(0, file_path)
            return audio_data, sampling_rate
    return None, None

# Function to compute and display FFT
def compute_fft():
    audio_data, sampling_rate = load_wav()
    if audio_data is not None:
        # Compute FFT
        fft_result = np.fft.fft(audio_data)
        freq = np.fft.fftfreq(len(audio_data), d=1/sampling_rate)

        # Display result
        text_result.delete(1.0, tk.END) # Clear previous results
        for i, (f, fft) in enumerate(zip(freq, fft_result)):
            if f >= 0:  # Display only positive frequencies
                text_result.insert(tk.END, f'{f:.2f} Hz: {fft.real:.2f} + {fft.imag:.2f}j\n')

# Set up the GUI
root = tk.Tk()
root.title("FFT Calculator for WAV Files")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# File path input
ttk.Label(frame, text="WAV File Path:").grid(column=0, row=0, sticky=tk.W)
entry_file_path = ttk.Entry(frame, width=50)
entry_file_path.grid(column=1, row=0, sticky=(tk.W, tk.E))
browse_button = ttk.Button(frame, text="Browse", command=lambda: load_wav())
browse_button.grid(column=2, row=0)

# Button to compute FFT
compute_button = ttk.Button(frame, text="Compute FFT", command=compute_fft)
compute_button.grid(column=0, row=2, columnspan=3)

# Text box for FFT result
text_result = tk.Text(frame, height=10, width=75)
text_result.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E))

root.mainloop()
