# script.alexandria
Internet Archive downloader for XBMC. 

(sources not provided)
![1](screenshots/1.bmp)
![2](screenshots/2.bmp)
![3](screenshots/3.bmp)

## How To Use:
- Enter collection URL into the "COLLECTION_URL" part of default.py
- Copy "default.py" to a folder in Q:/scripts (ideally Q:/scripts/Alexandria)
- Create a "Downloads" folder in F:/
- Run the script and enjoy!
- (Optional) To make a launcher front-end for multiple sources, modify "launcher.py" with the names of sources that you'd like to add, modify "source1.py / source2.py / source3.py" to point at your Python script of choice (add or remove as many entries as needed), then rename "launcher.py" to "default.py"!

## Issues:
- The script will crash if a "Downloads" folder on F (or wherever you've pointed it) isn't present. Will add options to automatically detect and create a directory if unavailable later!
- You tell me.

## TODO:
- Possibly add option to mount & launch .ISO files, ROM files and video files directly after downloading(?)
