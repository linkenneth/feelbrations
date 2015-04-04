import argparse
from pylab import *
from scipy.io import wavfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='file', type=str,
                        help='file to play')
    args = parser.parse_args()

    sampFreq, snd = wavfile.read(args.filename)
    snd = snd / (2.0**15)
    s1 = snd[:,0]               # pick first channel out of the two
    
    n = len(s1)
    p = fft(s1)
    
    
    import code
    code.interact(local=locals())
    

if __name__ == '__main__':
    main()
