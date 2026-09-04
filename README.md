# Circuit-Python-CIRCUITPY-Drive-Backup
Backup all files / folders from your CIRCUITPY drive to a desktop zip file.
  
Unfortunately, it is very easy to crash a Circuit Python CIRCUITPY drive and loose critical work.    
  
Unlike most development environments where the source code is on your PC and you only transfer a compiled BIN file to your development board, with Circuit Python your source code is on the board itself. If anything goes wrong on with a Circuit Python project you can easily loose all the source code.  
    
Enter this Python 3.12 project. When run it will search for the first drive it finds named "CIRCUITPY', then it will find your Desktop location, and make a zip file copy of the contents of the CIRCUITPY drive to the desktop.    
   
The name of the resulting zip file is of the form: "CIRCUITPY_Backup_20260811-185127.zip", where the numbers are a time stamp.  
Each backup zip file gets a unique time stamp, so that they will not overwrite one another, even if created in rapid succession.     
  
Usage: I have the source code in with my Python projects folders, then I put a shortcut to this program on the desktop. A double click will start the backup process which takes only a second and requires no options, etc.    
  
If you look at the source code, you will see two types of 'Ignore' lists that you can optionally specify. One is to ignore specific files, another is to ignore specific folders. But realistically the Circuit Python drive is pretty small, and I just backup everything. A typical backup for me is around 30 kBytes.

Tested on: Windows 7, 10 & 11.  
  
