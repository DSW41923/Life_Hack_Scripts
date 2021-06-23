import argparse
import os
import re

from detect_music_frequency_cutoff import detect_mp3_frequency_cutoff


SUPPORT_FORMAT = ["mp3", "wav"]


def move_music_files(file, source_directory, destination_directory):
    music_file_source_path = "{}\\{}".format(source_directory, file)
    music_file_dest_path = "{}\\{}".format(destination_directory, file)
    if os.path.exists(music_file_source_path):
        if not os.path.isdir(destination_directory):
            os.mkdir(destination_directory)
        os.rename(music_file_source_path, music_file_dest_path)


def rearrange_music_files_by_freq_cutoff(directory):
    directory_contents = os.listdir(directory)
    music_files = [d for d in directory_contents if d.split('.')[-1] in SUPPORT_FORMAT]
    print("Found {} music files to be rearranged".format(len(music_files)))
    for music_file in music_files:
        music_file_path = "{}\\{}".format(directory, music_file)
        frequency_cutoff = detect_mp3_frequency_cutoff(music_file_path)
        destination_dir = directory + '\\{}k'.format(frequency_cutoff // 1000)
        if frequency_cutoff > 20000:
            destination_dir = directory + '\\20k+'
        print("Moving {} to {}".format(music_file, destination_dir))
        move_music_files(music_file, directory, destination_dir)


def validate_existed_result(result_dir):
    directory_contents = os.listdir(result_dir)
    validating_directories = [d for d in directory_contents if os.path.isdir("{}\\{}".format(result_dir, d))]
    invalid_results = []
    for directory in validating_directories:
        directory_path = "{}\\{}".format(result_dir, directory)
        validating_bar, validating_condition = re.match(r'(\d+)k(\+)?', directory).groups()
        validating_bar = int(validating_bar) * 1000
        validating_files = os.listdir(directory_path)
        for music_file in validating_files:
            music_file_path = "{}\\{}".format(directory_path, music_file)
            frequency_cutoff = detect_mp3_frequency_cutoff(music_file_path)
            if frequency_cutoff != validating_bar \
                    or (validating_bar == 20000 and validating_condition and frequency_cutoff < validating_bar):
                if abs(frequency_cutoff - validating_bar) > 1000:
                    invalid_results.append((music_file_path, validating_bar, frequency_cutoff))
    print("Invalid music file number is {}".format(len(invalid_results)))
    print("Invalid music files are:")
    for r in invalid_results:
        print(r)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', metavar='D', type=str, help='Directory cotains music files to be rearrange')
    parser.add_argument('--validate_only', type=bool, required=False, default=False,
                        help='Only validate result or not. False by default.')
    args = parser.parse_args()
    if not os.path.exists(args.directory):
        raise

    if args.validate_only:
        validate_existed_result(args.directory)
        return

    rearrange_music_files_by_freq_cutoff(args.directory)


if __name__ == "__main__":
    main()
