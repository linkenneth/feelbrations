import argparse
from pydub import AudioSegment

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='file', type=str,
                        help='file to play')
    args = parser.parse_args()

    s = args.filename.split('.')
    prefix, ext = ''.join(s[:-1]), s[-1]
    if ext == 'wav':
        song = AudioSegment.from_wav(args.filename)
    elif ext == 'mp3':
        song = AudioSegment.from_mp3(args.filename)
    else:
        raise SyntaxError('SHIT wrong file type')
    song.export('{}_converted.wav'.format(prefix), format='wav')

if __name__ == '__main__':
    main()
