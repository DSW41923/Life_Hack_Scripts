import argparse
import librosa
import math
import sys


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def get_frequencies(n, sr):
    n_fft = 2 * (n - 1)
    basis = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    basis -= 0.5 * (basis[1] - basis[0])
    return basis


def detect_mp3_frequency_cutoff(file, debugging=False):
    y, sr = librosa.load(file, sr=44100)
    x = librosa.stft(y)
    frequencies = get_frequencies(x.shape[0], sr)

    avg_amp = [sum(abs(amp)) / len(amp) for amp in x]
    frequency_amp_pairs = []
    f = 1000
    for j in range(len(frequencies) - 1):
        if frequencies[j] <= f <= frequencies[j + 1]:
            frequency_amp_pairs.append((f, sum(avg_amp[j-2:j+3]) / 6))
            f += 1000

    for i in range(len(frequency_amp_pairs) - 2, -1, -1):
        if frequency_amp_pairs[i][1] > frequency_amp_pairs[i + 1][1] * 1.25 and frequency_amp_pairs[i][1] > 0.001:
            if debugging:
                print(frequency_amp_pairs[i + 1][1],
                      frequency_amp_pairs[i][1],
                      frequency_amp_pairs[i][0])
            return int(math.ceil(frequency_amp_pairs[i][0] / 1000.0)) * 1000

    return 22000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='F', type=str, help='Path of music file to be compute')
    args = parser.parse_args()
    print(detect_mp3_frequency_cutoff(args.file))


if __name__ == "__main__":
    main()
