import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq

SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds

def generate_sine_wave(freq, sample_rate, duration):
    # endpoint must be false because the fft works on periodic
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
# nois is really high so we reduce its power by mult by 0.3
noise_tone = noise_tone * 0.3

mixed_tone = nice_tone + noise_tone
# scaling the signal to fit into the target format:

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

# Number of samples in normalized_tone
N = SAMPLE_RATE * DURATION

# Note the extra 'r' at the front
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.show()