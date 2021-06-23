# Music File Organizer
Separate music files with different frequency cutoff, result round to 1000

## Requirements
### librosa
### ffmpeg scripts
for librosa to load mp3 file correctly

## detect_music_frequency_cutoff
1. Load the file and get the dbs from amplitude 
   [code reference](https://www.kaggle.com/hamditarek/audio-data-analysis-using-librosa)
2. Use some heuristic to determine cutoff. Tried many methods, currently combining the followings:
    1. Idea from fakeFLAC: detect frequency f where
        - the average magnitude of f-200 is 1.25 times larger than that of f
        - the average magnitude of f is no larger than that of 1.1 times f_max
        - Reference: http://www.maurits.vdschee.nl/fakeflac/
    2. If no f satisfy the aforementioned condition:
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