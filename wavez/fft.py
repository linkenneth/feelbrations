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

    # TODO HOW TO SYNC MUSIC TO THIS?!?
    # TODO negatives
    for i in xrange(0, sample_count, window_scount):
        now = time.time()
        print(chr(27) + "[2J")

        slice_ = ch1[i:i + window_scount]
        if len(slice_) < window_scount:
            break
        coeff = np.fft.fft(slice_)
        coeff = np.abs(coeff)  # only use magnitude of FFT coeffs

        SHIT_TO_MAP = [0, 10, 20, 33, 44, 50, 68, 79, 88, 100,
                       120, 132, 152, 178, 189, 200, 220, 250, 270, 290,
                       305, 315, 325, 338, 350, 370, 390, 410, 425, 440]  # up to 441 is positive
        for point in SHIT_TO_MAP:
            print '{: .3f}'.format(freqs[point]),
            bars = int(coeff[point] * 10)
            if bars > 30: bars = 30
            print '>' * bars

        elapsed = time.time() - now
        sleep_time = WINDOW_LEN - elapsed
        if sleep_time > 0:
            time.sleep(WINDOW_LEN - elapsed)
        else:
            # TODO incur sleep debt to catch up?
            pass

    # import code
    # code.interact(local=locals())

if __name__ == '__main__':
    main()
