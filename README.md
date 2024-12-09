# script.alexandria
Internet Archive downloader for XBMC. 

Requires the latest version of XBMC from Xbins (as it has crucial TLS/SSL updates that allow this script to work). Sources are NOT provided and must be input manually!

![1](screenshots/1.bmp)
![2](screenshots/2.bmp)
![3](screenshots/3.bmp)

## How To Use:
- Enter Internet Archive collection URL into the "COLLECTION_URL" part of default.py
- Copy "default.py" to a folder in Q:/scripts (ideally Q:/scripts/Alexandria)
- Create a "Downloads" folder in F:/
- Run the script and enjoy!
- (Optional) To make a launcher front-end for multiple sources, modify "launcher.py" with the names of sources that you'd like to add, modify "source1.py / source2.py / source3.py" to point at your Python script of choice (add or remove as many entries as needed), then rename "launcher.py" to "default.py"!

## Issues:
- The script will crash if a "Downloads" folder on F (or wherever you've pointed it) isn't present. Will add options to automatically detect and create a directory if unavailable later!
- The script blocks files over 4GB (downloading + individual files stored in .zip files) due to FATX limitations. I could possibly modify the script to download & extract files over 4GB in parts, but the performance penalties may not be worth it compared to using a PC.
- You tell me.

## TODO:
- Possibly add option to mount & launch .ISO files, ROM files and video files directly after downloading(?)
- Implement scanning from multiple collections at the same time.
- Implement some sort of login system so access-locked files can be downloaded.

## Disclaimer:
- The Internet Archive is a vast archive of many files, tons of which are legal to download! Make sure you follow the copyright laws of your region while downloading from Internet Archive sources. Support will not be given for anyone trying to use this utility for blatant piracy. 
