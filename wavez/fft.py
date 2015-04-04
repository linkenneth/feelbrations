import argparse
from pydub import AudioSegment

from pylab import *
from scipy.io import wavfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='file', type=str,
                        help='file to play')
    args = parser.parse_args()

    # if .mp3, convert to .wav
    s = args.filename.split('.')
    prefix, ext = '.'.join(s[:-1]), s[-1]
    if ext == 'wav':
        song = AudioSegment.from_wav(args.filename)
    elif ext == 'mp3':
        song = AudioSegment.from_mp3(args.filename)
    else:
        raise SyntaxError('SHIeeeT wrong file type')
    song_name = '{}_converted.wav'.format(prefix)
    song.export(song_name, format='wav')

    # administer fft
    sampFreq, snd = wavfile.read(song_name) # default int16 values
    snd = snd / (2.0**15)     # normalize into -1.0 to 1.0 value range
    s1 = snd[:, 0]            # only use first channel out of the two

    n = len(s1)
    p = fft(s1)
    
    
    import code
    code.interact(local=locals())
    

if __name__ == '__main__':
    main()
