import time
import serial
import pygame
import argparse
import numpy as np

from scipy.io import wavfile
from pydub import AudioSegment

WINDOW_LEN = 0.02  # seconds
PORT = '/dev/cu.usbserial-AH01KY7M'

def make_wav(fname):
    s = fname.split('.')
    prefix, ext = '.'.join(s[:-1]), s[-1]
    if ext == 'wav':
        song = AudioSegment.from_wav(fname)
    elif ext == 'mp3':
        song = AudioSegment.from_mp3(fname)
    else:
        raise SyntaxError('SHIeeeT wrong file type')
    song_name = '{}_CONVERTED.wav'.format(prefix)
    song.export(song_name, format='wav')
    return song_name

def choose_freqs(freqs):
    freqs = freqs[freqs >= 0]
    chosen_freqs = np.linspace(0, 1000, 40).astype(int)
    chosen_indices = np.searchsorted(freqs, chosen_freqs)
    # chosen_freqs = np.logspace(2., np.log(5000) / np.log(7),
    #                            num=40, base=7)
    # chosen_indices = np.searchsorted(freqs, chosen_freqs)
    # print(freqs)
    # raise Exception
    return chosen_indices, chosen_freqs

def choose_hand_freqs(freqs):
    freqs = freqs[freqs >= 0]
    chosen_freqs = [50, 100, 250, 350, 450, 50, 100, 250]
    chosen_indices = np.searchsorted(freqs, chosen_freqs)
    return chosen_indices, chosen_freqs

def display_visualizer(data, chosen_freqs):
    return
    print(chr(27) + "[2J")
    for freq, intensity in zip(chosen_freqs, data):
        print '{: 6.0f}'.format(freq),
        bars = int(intensity)
        if bars > 150: bars = 150
        print '>' * bars

def display_hand(data, chosen_freqs, thresh):
    print(chr(27) + "[2J")
    for freq, intensity, t in zip(chosen_freqs, data, thresh):
        print '{: 6.0f}'.format(freq),
        bars = 0 if int(intensity) < t else 80
        print '>' * bars
        ser.write('{:02d}'.format(bars))
    ser.flush()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='file', type=str,
                        help='file to play')
    args = parser.parse_args()

    # if .mp3, convert to .wav
    song_name = make_wav(args.filename)

    # clean up and prepare signal
    sample_freq, signal = wavfile.read(song_name) # default int16
    signal = signal / (2.0 ** 15)       # normalize into -1.0 to 1.0 range
    ch1 = signal[:, 0]                  # only use first channel / 2

    sample_count = len(signal)
    window_scount = int(sample_freq * WINDOW_LEN)  # of samples in each window
    freqs = np.fft.fftfreq(window_scount, 1. / sample_freq)
    chosen_hand_indices, chosen_hand_freqs = choose_hand_freqs(freqs)
    chosen_indices, chosen_freqs = choose_freqs(freqs)

    pygame.mixer.init(frequency=sample_freq)
    stored = []

    start = time.time()
    # process: fft to analyze frequency, and arrange for motor outputs
    for i in xrange(0, sample_count, window_scount):
        slice_ = ch1[i:i + window_scount]
        if len(slice_) < window_scount:
            break
        coeff = np.fft.fft(slice_)
        coeff = np.abs(coeff)  # only use magnitude of FFT coeffs
        # stored.append(
        #     np.maximum.reduce([coeff[chosen_indices - 1], coeff[chosen_indices],
        #                        coeff[chosen_indices + 1]]))
        stored.append(coeff[chosen_indices])

    stored = np.array(stored)
    med = np.median(stored, axis=0)
    mad = 1.4826 * np.median(np.abs(stored - med), axis=0)
    thresh = 0.7 * mad + med

    print 'Pre-processing complete.'
    print 'Time taken: {:.2f} seconds.'.format(time.time() - start)

    # display: read from processed results and play in sync with music
    sound = pygame.mixer.Sound(song_name)
    sound.play()
    start = time.time()
    for i, data in enumerate(stored):
        display_hand(data, chosen_hand_freqs, thresh)
        display_visualizer(data, chosen_freqs)

        elapsed = time.time() - start
        sleep_time = WINDOW_LEN * (i + 1) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            # TODO incur sleep debt to catch up?
            pass


    # import code
    # code.interact(local=locals())

if __name__ == '__main__':
    ser = serial.Serial(port=PORT, baudrate=9600)

    main()
