import time
import argparse
import numpy as np

from scipy.io import wavfile
from pydub import AudioSegment

WINDOW_LEN = 0.02  # seconds

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
    chosen_indices = np.linspace(0, len(freqs) - 1, 20).astype(int)
    chosen_freqs = freqs[chosen_indices]
    return chosen_indices, chosen_freqs

def display_visualizer(data, chosen_freqs):
    print(chr(27) + "[2J")
    for freq, intensity in zip(chosen_freqs, data):
        print '{: .3f}'.format(freq),
        bars = int(intensity * 10)
        if bars > 30: bars = 30
        print '>' * bars

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
    freqs = np.fft.fftfreq(window_scount)
    chosen_indices, chosen_freqs = choose_freqs(freqs)

    stored = []

    start = time.time()
    # process: fft to analyze frequency, and arrange for motor outputs
    for i in xrange(0, sample_count, window_scount):
        slice_ = ch1[i:i + window_scount]
        if len(slice_) < window_scount:
            break
        coeff = np.fft.fft(slice_)
        coeff = np.abs(coeff)  # only use magnitude of FFT coeffs
        stored.append(coeff[chosen_indices])
    print 'Pre-processing complete.'
    print 'Time taken: {:.2f} seconds.'.format(time.time() - start)

    raw_input('Press ENTER to begin display.')
    # display: read from processed results and play in sync with music
    start = time.time()
    for i, data in enumerate(stored):
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
    main()
