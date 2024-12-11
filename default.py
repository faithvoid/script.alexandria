import requests
import xbmc
import xbmcgui
import os
import zipfile
from urllib import quote

ADDON_NAME = "Alexandria - Public Domain Movies"
SAVE_PATH = "F:\\Downloads"  # Change this to your desired download location
COLLECTION_URL = "https://archive.org/details/mtvs-downtown_202209"  # Replace with your collection URL

MAX_FILENAME_LENGTH = 42
MAX_PATH_LENGTH = 250
MAX_FILE_SIZE = 4294967296  # 4GB in bytes
MEDIA_EXTENSIONS = {".mp4", ".mp3", ".avi", ".mkv", ".wav", ".flac", ".mov"}  # Add more as needed

def ensure_save_path_exists():
    """Ensure the SAVE_PATH directory exists, creating it if necessary."""
    if not os.path.exists(SAVE_PATH):
        try:
            os.makedirs(SAVE_PATH)
        except Exception as e:
            xbmcgui.Dialog().ok(ADDON_NAME, "Error creating directory: {}".format(SAVE_PATH))
            raise e

def fetch_collection_metadata():
    # Extract collection ID from the URL
    collection_id = COLLECTION_URL.split("/")[-1]
    api_url = "https://archive.org/metadata/{}".format(collection_id)
    
    # Fetch metadata
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        xbmcgui.Dialog().ok(ADDON_NAME, "Failed to fetch collection metadata.")
        return None

def truncate_file_name(file_name):
    # Split the file name into base name and extension
    base_name, ext = os.path.splitext(file_name)
    
    # Ensure the base name fits within the MAX_FILENAME_LENGTH, leaving room for the extension
    max_base_name_length = MAX_FILENAME_LENGTH - len(ext)
    if len(base_name) > max_base_name_length:
        base_name = base_name[:max_base_name_length]
    
    return base_name + ext

def get_safe_file_path(file_name):
    # Ensure the full file path doesn't exceed MAX_PATH_LENGTH
    truncated_file_name = truncate_file_name(file_name)
    file_path = os.path.join(SAVE_PATH, truncated_file_name)
    
    # If the full path exceeds MAX_PATH_LENGTH, truncate the file name further
    if len(file_path) > MAX_PATH_LENGTH:
        available_length = MAX_PATH_LENGTH - len(SAVE_PATH) - 1  # Reserve space for the separator
        base_name, ext = os.path.splitext(truncated_file_name)
        base_name = base_name[:available_length]
        truncated_file_name = base_name + ext
        file_path = os.path.join(SAVE_PATH, truncated_file_name)
    
    return file_path

def stream_file(file_url):
    """Play the file using XBMC's built-in player."""
    encoded_url = quote(file_url, safe=':/')
    xbmc.Player().play(encoded_url)

def download_file(item_url, save_path, file_size):
    if file_size > MAX_FILE_SIZE:
        xbmcgui.Dialog().ok(ADDON_NAME, "The file is too large to download ({} bytes).".format(file_size))
        return False

    response = requests.get(item_url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))

        # Convert total size to MB
        total_size_mb = total_size / (1024 * 1024)

        # Create progress dialog
        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create(ADDON_NAME, "Downloading...")  # Show in MB
        
        with open(save_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=2048*1024):  # Smaller chunks to update UI
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Convert downloaded size to MB
                    downloaded_mb = downloaded / (1024 * 1024)

                    # Update progress dialog to show downloaded/total in MB
                    percent = int((downloaded / total_size) * 100)
                    progress_dialog.update(percent, "Downloading: {:.2f} MB of {:.2f} MB".format(downloaded_mb, total_size_mb))

                    # Check if the user canceled the download
                    if progress_dialog.iscanceled():
                        progress_dialog.close()
                        xbmcgui.Dialog().ok(ADDON_NAME, "Download canceled.")
                        return False

        progress_dialog.close()  # Close progress dialog after download
        return True
    else:
        xbmcgui.Dialog().ok(ADDON_NAME, "Failed to download file.")
        return False

def unzip_file(file_path, extract_to):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Check if any individual file inside the ZIP exceeds 4GB
            for zip_info in zip_ref.infolist():
                if zip_info.file_size > MAX_FILE_SIZE:
                    xbmcgui.Dialog().ok(ADDON_NAME, "The file '{}' inside the ZIP archive is too large to extract ({} bytes).".format(zip_info.filename, zip_info.file_size))
                    return False
            
            # Extract all files if none exceed 4GB
            zip_ref.extractall(extract_to)
        
        return True
    except Exception as e:
        xbmcgui.Dialog().ok(ADDON_NAME, "Error extracting file: {}".format(str(e)))
        return False

def main():
    # Ensure the save path exists
    ensure_save_path_exists()

    # Fetch metadata for the collection
    metadata = fetch_collection_metadata()
    if not metadata:
        return

    # List available files
    files = metadata.get("files", [])
    if not files:
        xbmcgui.Dialog().ok(ADDON_NAME, "No files found in the collection.")
        return

    # Show a selection dialog
    file_names = [file["name"] for file in files if "name" in file]
    selected_index = xbmcgui.Dialog().select("Select a file", file_names)
    if selected_index == -1:
        return

    # Process the selected file
    selected_file = files[selected_index]
    file_name = selected_file["name"]
    file_url = "https://archive.org/download/{}/{}".format(metadata["metadata"]["identifier"], file_name)
    
    # Check if the file is a media file
    _, ext = os.path.splitext(file_name)
    if ext.lower() in MEDIA_EXTENSIONS:
        stream_choice = xbmcgui.Dialog().yesno(
            ADDON_NAME,
            "Would you like to stream this file instead of downloading it?",
            "File: {}".format(file_name)
        )
        if stream_choice:  # User selected "Yes"
            stream_file(file_url)
            return

    # Proceed to download the file
    save_path = get_safe_file_path(file_name)

    # Check file size before downloading
    file_size = int(selected_file.get("size", 0))  # Assuming "size" is in bytes
    if file_size > MAX_FILE_SIZE:
        xbmcgui.Dialog().ok(ADDON_NAME, "The file '{}' is too large to download ({} bytes).".format(file_name, file_size))
        return

    if download_file(file_url, save_path, file_size):
        xbmcgui.Dialog().ok(ADDON_NAME, "File downloaded successfully:\n{}".format(save_path))
        
        # Check if the file is a .zip and ask if the user wants to unzip
        if file_name.lower().endswith(".zip"):
            unzip_choice = xbmcgui.Dialog().yesno(
                ADDON_NAME, 
                "Do you want to unzip the file?", 
                "File: {}\nWould you like to extract it?".format(file_name)
            )
            
            if unzip_choice:  # User selected "Yes"
                if unzip_file(save_path, SAVE_PATH):
                    xbmcgui.Dialog().ok(ADDON_NAME, "File unzipped successfully!")
                else:
                    xbmcgui.Dialog().ok(ADDON_NAME, "Failed to unzip the file.")
    else:
        xbmcgui.Dialog().ok(ADDON_NAME, "Failed to download the file.")

if __name__ == "__main__":
    main()
