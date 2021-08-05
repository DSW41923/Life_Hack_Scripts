import argparse
import librosa
import os

from rearrange_music_file import SUPPORT_FORMAT, move_music_files


def has_same_freq(music_file_1, music_file_2):
    if os.path.exists(music_file_1) and os.path.exists(music_file_2):
        y_1, sr_1 = librosa.load(music_file_1, sr=44100)
        x_1 = librosa.stft(y_1)
        y_2, sr_2 = librosa.load(music_file_2, sr=44100)
        x_2 = librosa.stft(y_2)
        if all([all([x == y for x, y in zip(a, b)]) for a, b in zip(x_1, x_2)]):
            return True
    return False


def get_smaller_file_index(file_1, file_2):
    if os.stat(file_1).st_size < os.stat(file_2).st_size:
        return 1
    if os.stat(file_1).st_size > os.stat(file_2).st_size:
        return 2
    return None


def merge_music_files(source_directories, dest_directory, overwrite_only=False):
    music_files_per_dir = {}
    for index, directory in enumerate(source_directories):
        directory_contents = os.listdir(directory)
        sub_directories = [d for d in directory_contents if os.path.isdir("{}\\{}".format(directory, d))]
        for sub_directory in sub_directories:
            sub_directory_path = "{}\\{}".format(directory, sub_directory)
            music_files = [d for d in os.listdir(sub_directory_path) if d.split('.')[-1] in SUPPORT_FORMAT]
            music_file_paths = ["{}\\{}".format(sub_directory, mf) for mf in music_files]
            if not music_files_per_dir.get(directory):
                music_files_per_dir[directory] = music_file_paths
            else:
                music_files_per_dir[directory].extend(music_file_paths)
        print("Found {} music files to be merged".format(len(music_files_per_dir[directory])))

    moved_files = []
    if os.path.exists(dest_directory):
        dest_dir_content = os.listdir(dest_directory)
        music_files = [d for d in dest_dir_content if d.split('.')[-1] in SUPPORT_FORMAT]
        moved_files.extend(music_files)

    for other_dir in [d for d in music_files_per_dir]:
        for music_file in music_files_per_dir[other_dir]:
            music_file_freq, music_file_name = music_file.split("\\")
            music_file_dir = "{}\\{}".format(other_dir, music_file_freq)
            if music_file_name in moved_files:
                smaller_file_index = get_smaller_file_index("{}\\{}".format(music_file_dir, music_file_name),
                                                            "{}\\{}".format(dest_directory, music_file_name))
                music_file_1 = "{}\\{}".format(music_file_dir, music_file_name)
                music_file_2 = "{}\\{}".format(dest_directory, music_file_name)
                if has_same_freq(music_file_1, music_file_2):
                    # If two files have same frequency amplitude, choose the smaller one
                    if smaller_file_index == 1:
                        move_music_files(music_file_name, music_file_dir, dest_directory)
                    else:
                        os.remove("{}\\{}".format(music_file_dir, music_file_name))
                else:
                    # If not, choose bigger one with larger kbps
                    if smaller_file_index == 2:
                        move_music_files(music_file_name, music_file_dir, dest_directory)
                    else:
                        os.remove("{}\\{}".format(music_file_dir, music_file_name))
            else:
                if not overwrite_only:
                    move_music_files(music_file_name, music_file_dir, dest_directory)
                    moved_files.append(music_file_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', metavar='D', type=str, nargs='+',
                        help='Directory cotains music files to be rearrange')
    parser.add_argument('--merge_destination', type=str, required=True, default='',
                        help='Path of directories contains merged music files from directories')
    parser.add_argument('--overwrite_only', type=bool, required=False, default=False,
                        help='Only move files has same name in merge_dsetination. False by default.')
    args = parser.parse_args()

    for directory in args.directories:
        if not os.path.exists(directory):
            raise

    merge_music_files(args.directories, args.merge_destination, args.overwrite_only)


if __name__ == "__main__":
    main()
