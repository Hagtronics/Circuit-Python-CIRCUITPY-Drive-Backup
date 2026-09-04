"""
Version 1.0 - 11Aug26

# At command prompt run: clone_circuitpy.py
# Automatically makes a copy of 'CIRCUITPY' drive to a zip file on the Windows desktop.

# Output zip files will look like: "CIRCUITPY_Backup_20260811-185127.zip", where the numbers are a time stamp.
# Each backup zip file gets a unique time stamp, so that they will not overwrite one another.

Written By: Steve Hageman - August 2026.
The Unlicense - https://github.com/Hagtronics/Circuit-Python-CIRCUITPY-Drive-Backup?tab=Unlicense-1-ov-file
Repository: https://github.com/Hagtronics/Circuit-Python-CIRCUITPY-Drive-Backup
"""

# You can choose to ignore files and folders with these lists,
ignore_folders = []  # Or something like: ['.fseventsd', '__pycache__', '.mypy_cache', '.vscode']
ignore_files = []  # Or something like: ['.metadata_never_index', '.Trash-1000', '.Trashes']


# ===== Program Start =====

import ctypes
import os
import sys
import string
import time
import zipfile
from ctypes import wintypes
from tkinter import messagebox


def find_circuitpy_drive():
    GetVolumeInformationW = ctypes.windll.kernel32.GetVolumeInformationW
    volume_name_buf = ctypes.create_unicode_buffer(1024)

    for letter in string.ascii_uppercase:
        path = f"{letter}:\\"
        if os.path.exists(path):
            # Query volume label
            rc = GetVolumeInformationW(
                ctypes.c_wchar_p(path),
                volume_name_buf,
                ctypes.sizeof(volume_name_buf),
                None, None, None,
                None, 0
            )
            if rc and volume_name_buf.value == "CIRCUITPY":
                return path.replace("\\", "/")  # -> 'D:/'

    return None


# Find the desktop even if it is remapped.
# https://stackoverflow.com/questions/33179365/python-finding-user-id-and-moving-directories-windows
# https://stackoverflow.com/questions/78097730/calling-shgetknownfolderpath-from-python

# Define GUID structure
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8)
    ]

# Desktop GUID: {B4BFCC3A-DB2C-424C-B029-7FE99A87C641}
FOLDERID_Desktop = GUID(
    0xB4BFCC3A,
    0xDB2C,
    0x424C,
    (0xB0, 0x29, 0x7F, 0xE9, 0x9A, 0x87, 0xC6, 0x41)
)

def get_desktop_path():
    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID),
        wintypes.DWORD,
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_wchar_p)
    ]

    path_ptr = ctypes.c_wchar_p()
    result = SHGetKnownFolderPath(ctypes.byref(FOLDERID_Desktop), 0, None, ctypes.byref(path_ptr))

    if result != 0:
        #raise OSError(f"Failed to retrieve Desktop path, error code: {result}")
        return None

    return path_ptr.value + '/'


def zip_folder(in_path, zip_file_name, ignore_folders=None, ignore_files=None):
    if ignore_folders is None:
        ignore_folders = []
    if ignore_files is None:
        ignore_files = []

    try:
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(in_path):

                # --- Skip folders entirely ---
                dirs[:] = [d for d in dirs if d not in ignore_folders]

                for file in files:

                    # Skip files by extension or exact match
                    if any(file.endswith(ext) for ext in ignore_files):
                        continue

                    file_path = os.path.join(root, file)

                    # FIX: compute arcname relative to folder_path
                    arcname = os.path.relpath(file_path, in_path)

                    zipf.write(file_path, arcname)
                    print(f"Added: {arcname}")
    except Exception as e:
        messagebox.showwarning(title='ERROR!!!', message=f'The ZIP routine failed because: {e}.\nNo Backup Created!')


# ===== Control Guts =====
circuitpy_path = find_circuitpy_drive()
if circuitpy_path is None:
    messagebox.showwarning(title='ERROR!!!', message='The "CIRCUITPY" drive could not be found.\nNo Backup Created!')
    sys.exit()

print("CIRCUITPY drive: ", circuitpy_path)


desktop_path = get_desktop_path()
if desktop_path is None:
    messagebox.showwarning(title='ERROR!!!', message='The "Desktop" path could not be found.\nNo Backup Created!')
    sys.exit()

print("Desktop folder: ", desktop_path)

archive_name = desktop_path + 'CIRCUITPY_Backup_' + time.strftime("%Y%m%d-%H%M%S") + '.zip'

zip_folder(circuitpy_path, archive_name, ignore_folders, ignore_files)

# fini
