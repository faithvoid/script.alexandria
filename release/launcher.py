# Alexandria - Internet Archive parser / download manager for XBMC by faithvoid
# Edit "Source #X" to whatever you'd like your source name to be, and rename your modified "default.py" to whatever you'd like, as long as "Source #X" points to that Python file. Then rename this script to default.py.

import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("Source #1", "RunScript(Q:\\scripts\\Alexandria\\source1.py)"),
        ("Source #2", "RunScript(Q:\\scripts\\Alexandria\\source2.py)"),
        ("Source #2", "RunScript(Q:\\scripts\\Alexandria\\source3.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Alexandria - Internet Archive Downloader", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
