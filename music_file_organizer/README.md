# Music File Organizer
Separate music files with different frequency cutoff, result round to 1000.

## Usage
Simply `python3 {file_name}.py` Use `-h` for help!

## Requirements
### Windows OS
Could be expanded to Linux version, probably.
### Python 3
### librosa
### ffmpeg scripts
for librosa to load mp3 file correctly, can be downloaded from https://www.gyan.dev/ffmpeg/builds/

## detect_music_frequency_cutoff
Detect the frequency cutoff of a music file by the following method:
1. Load the file and get the frequency range from shape of amplitude. [code reference](https://www.kaggle.com/hamditarek/audio-data-analysis-using-librosa)
3. Use some heuristic to determine cutoff by the following method:
    1. Calculate the average amplitude for each frequency sampled
    2. Calculate the average of average amplitude for each thousand of hz (i.e. f=1000, 2000...)
    3. Find f such that 
       1. amplitude around f 1.25 times larger than that around f+1000
       2. amplitude around f larger than 0.001
    4. If no f satisfy the aforementioned condition, return 22000:
        - determine the average db for each thousand of hz
        - find a certain f (thousand of hz) where 
          the average db of f is greater than f+1000 and 
          less than the minimum of that of other f_0 less than f
    
    Other methods tried:
    1. ratio of time when the loudness of a frequency is smaller than a value close to the minimum of the entire file
        - Tried from 0 to max and max to 0, should always do this from max to 0
    2. change of slope greater than a bar
        - Tried bar=1, 0.1, 0.01, but not really reliable
        - Perhaps compare relatively works
    3. Idea from fakeFLAC: detect frequency f where
        - the average magnitude of f-200 is 1.25 times larger than that of f
        - the average magnitude of f is no larger than that of 1.1 times f_max
        - Reference: http://www.maurits.vdschee.nl/fakeflac/
        - Result in no cutoff many times with my files

## rearrange_music_file
Rearrange music files in a directory with `\d*1000` cutoff into child folders named as `(\d)k`. 
Files with cutoff greater than 20000 will be moved in to folder `20k+` 
Validate function can use to validate results done by other methods (such as by human + spectogram software).

## merge_music_file
Merge rearranged files from one folder to another, will keep one with larger kbps (detected by size) or 
smaller size if they have same freqeuncy sampled when there are two music files with same name and freqency cutoff.