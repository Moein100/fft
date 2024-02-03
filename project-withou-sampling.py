import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to load a WAV file
def load_wav():
    file_path = filedialog.askopenfilename()
    if file_path:
        sampling_rate, data = wavfile.read(file_path)
        entry_sampling_rate.delete(0, tk.END)
        entry_sampling_rate.insert(0, str(sampling_rate))
        entry_signal.delete(0, tk.END)
        entry_signal.insert(0, str(file_path))

# Function to compute and plot FFT
def compute_and_plot_fft():
    file_path = entry_signal.get()
    if file_path:
        sampling_rate, data = wavfile.read(file_path)
        # If stereo, just use one channel
        if data.ndim > 1:
            data = data[:, 0]
        
        # Compute FFT
        fft_result = np.fft.fft(data)
        freq = np.fft.fftfreq(data.size, d=1/sampling_rate)

        # Plot
        fig, ax = plt.subplots()
        ax.plot(freq, np.abs(fft_result))
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude')
        ax.set_title('FFT of the Signal')
        
        # Display plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(column=0, row=4, columnspan=3, sticky=(tk.W, tk.E))
        canvas.draw()

# Set up the GUI
root = tk.Tk()
root.title("FFT Calculator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# File path input
ttk.Label(frame, text="WAV File:").grid(column=0, row=0, sticky=tk.W)
entry_signal = ttk.Entry(frame, width=50)
entry_signal.grid(column=1, row=0, sticky=(tk.W, tk.E))
button_load = ttk.Button(frame, text="Load WAV", command=load_wav)
button_load.grid(column=2, row=0)

# Sampling rate display
ttk.Label(frame, text="Sampling Rate:").grid(column=0, row=1, sticky=tk.W)
entry_sampling_rate = ttk.Entry(frame, width=50)
entry_sampling_rate.grid(column=1, row=1, sticky=(tk.W, tk.E))
entry_sampling_rate.config(state='readonly')

# Button to compute and plot FFT
compute_button = ttk.Button(frame, text="Compute and Plot FFT", command=compute_and_plot_fft)
compute_button.grid(column=0, row=2, columnspan=3)

root.mainloop()
