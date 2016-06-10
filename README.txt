To install the converting scripts to run in iTunes, first make sure that this 
directory is in a place you like, such as your documents folder. Then, simply 
double-click the `install_iTunes_Convert.command’ file to make the converting 
applications useable in iTunes. If the command says you do not have 
permissions, simply run:

chmod u+x [drag and drop the file here]

This should allow you to execute the file.

All the python scripts and source code for the AppleScript Application can be 
found in the Source_Code directory. The iTunes_music_convert.py file does the 
track info parsing and can be run at command line using iTunes track ids. 
However, if you would like to just convert a few songs or a playlist, I would 
recommend opening iTunes, selecting the songs you want to convert, and running 
the appropriate converting script under the script tab at the top.

Change any of the program files by the end-user is not recommended and any such 
changes may cause the scripts to fail.

This code is distributed under the GNU General Public License Version 3.
