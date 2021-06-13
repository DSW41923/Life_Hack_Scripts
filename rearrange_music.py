import argparse
import os
import shutil
import re

from detect_music_frequency_cutoff import detect_mp3_frequency_cutoff


def rearrange_music_files_by_freq_cutoff(directory, ratio=0.995):
    pass


def validate_rearrangement_result(result_dir, ratio=0.995):
    directory_contents = os.listdir(result_dir)
    validating_directories = [d for d in directory_contents if os.path.isdir("{}\\{}".format(result_dir, d))]
    for directory in validating_directories:
        directory_path = "{}\\{}".format(result_dir, directory)
        validating_bar, validating_condition = re.match(r'(\d+)k(\+)?', directory).groups()
        validating_bar *= 1000
        validating_files = os.listdir(directory_path)
        for music_file in validating_files:
            music_file_path = "{}\\{}".format(directory_path, music_file)
            frequency_cutoff = detect_mp3_frequency_cutoff(music_file_path, ratio)
            if validating_bar == 20 and validating_condition:
                if frequency_cutoff < validating_bar:
                    print(music_file_path)
                    print(frequency_cutoff)
            else:
                if frequency_cutoff != validating_bar:
                    print(music_file_path)
                    print(frequency_cutoff)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', metavar='D', type=str, help='Directory cotains music files to be rearrange')
    parser.add_argument('--ratio', type=float, required=False, default=0.995,
                        help='Ratio used to determine cutoff')
    parser.add_argument('--validate_only', type=bool, required=False, default=False,
                        help='Only validate result or not. False by default.')
    args = parser.parse_args()
    if not os.path.exists(args.directory):
        raise
    # rearrange_music_files_by_freq_cutoff(args.directory, args.ratio)
    validate_rearrangement_result(args.directory, args.ratio)


if __name__ == "__main__":
    main()
