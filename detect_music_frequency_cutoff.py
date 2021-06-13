import argparse
import librosa
import math
import numpy as np


def get_frequencies(n, sr):
    n_fft = 2 * (n - 1)
    basis = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    fmax = basis[-1]
    basis -= 0.5 * (basis[1] - basis[0])
    basis = np.append(np.maximum(0, basis), [fmax])
    return basis


def detect_mp3_frequency_cutoff(file, ratio_bar=0.995, ceilling=True):
    y, sr = librosa.load(file, sr=44100)
    x = librosa.stft(y)
    dbs = librosa.amplitude_to_db(abs(x))
    frequencies = get_frequencies(dbs.shape[0], sr)
    min_db = min([min(db) for db in dbs])
    min_db_bar = math.ceil(min_db)

    for i, x in enumerate(dbs):
        if len([f for f in x if f <= min_db_bar]) / len(x) >= ratio_bar:
            return int(math.ceil(frequencies[i] / 1000.0)) * 1000 if ceilling else frequencies[i]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='F', type=str, help='Path of music file to be compute')
    parser.add_argument('--ratio', type=float, required=False, default=0.995,
                        help='Ratio used to determine cutoff')
    args = parser.parse_args()
    print(detect_mp3_frequency_cutoff(args.file, args.ratio))
    print(detect_mp3_frequency_cutoff(args.file, args.ratio, False))


if __name__ == "__main__":
    main()
