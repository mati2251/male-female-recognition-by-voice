import sys
from matplotlib import pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
# import warnings
# warnings.filterwarnings("ignore")
human = [85, 255]
woman = [165, 255]
men = [85, 180]


def read_signal():
    file_path = sys.argv[1]
    # file_path = "train/006_K.wav"
    F, signal = wav.read(file_path)
    if signal.ndim > 1:
        signal = signal.mean(axis=1)
    return F, signal


def window_signal(signal):
    return signal.copy() * np.hamming(len(signal))


def get_spectrum(signal):
    spectrum = np.fft.fft(signal)[: len(signal) // 2]
    spectrum = np.abs(spectrum)
    return spectrum


def get_freqs(F, n):
    TW = 1 / F
    freqs = np.fft.fftfreq(n, TW)[: n // 2]
    return freqs


def resample_signal(F, signal, new_F):
    new_signal = signal.copy()[:: int(F / new_F)]
    return new_signal


fig, axs = plt.subplots(4, 1, figsize=(10, 10))
current_plt_index = 0


def draw_spectrum(freqs, spectrum):
    global current_plt_index
    axs[current_plt_index].plot(freqs, spectrum)
    axs[current_plt_index].set_xlabel("Częstotliwość [Hz]")
    axs[current_plt_index].set_xlim([0.01, 23000])
    axs[current_plt_index].set_xscale("log")
    current_plt_index += 1





F, signal = read_signal()
draw_spectrum(range(len(signal)), signal)
signal = window_signal(signal)
draw_spectrum(range(len(signal)), signal)
spectrum = get_spectrum(signal)
freqs = get_freqs(F, len(signal))
draw_spectrum(freqs, spectrum)

final_spectrum = spectrum.copy()
for i in range(2, 5):
    new_F = F / i
    resample = resample_signal(F, spectrum, new_F)
    final_spectrum[:len(resample)] *=  resample
draw_spectrum(freqs[:len(final_spectrum)], final_spectrum)
tone = freqs[np.argmax(final_spectrum)]
if tone > human[0] and tone < human[1]:
    if tone > woman[0] and tone < woman[1]:
        print("K")
    elif tone > men[0] and tone < men[1]:
        print("M")
print(tone)
plt.savefig("spectrum.png")