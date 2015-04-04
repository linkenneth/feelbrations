import argparse
from pydub import AudioSegment

def make_song(fname):
    if fname.split('.')[-1] == 'wav':
        song = AudioSegment.from_wav(fname)
    elif fname.split('.')[-1] == 'mp3':
        song = AudioSegment.from_mp3(fname)
    else:
        raise SyntaxError('SHIT')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='file', type=str,
                        help='file to play')
    args = parser.parse_args()
    print(args.filename)

    song = make_song(args.filename)

if __name__ == '__main__':
    main()
