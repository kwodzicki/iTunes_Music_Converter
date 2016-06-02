#!/usr/bin/env python
#+
# Name:
#   copy_file
# Purpose:
#   A function to copy a file, checking if it exists first, and attempting
#   to copy it three times if it does NOT exist, or is not the same size
#   as the source file after copying.
# Inputs:
#   source : Full path to the source file.
#   destination : Full path to the destination file.
# Outputs
#   Returns 0 on successful copy, 1 on a failure.
# Keywords:
#   verbose : Set to increase verbosity.
# Author and History:
#   Kyle R. Wodzicki     Created 12 May 2016
#-

def copy_file(source, destination, verbose=None):
	import os, sys, shutil;
	if os.path.isfile(destination):
		if os.path.getsize(source) == os.path.getsize(destination):                 # If the file EXISTS on the receiver and is correct size, print that it exists
			if (verbose is not None):
				print 'File EXISTS on receiver: '+'/'.join(destination.split('/')[-3:]);# Message that the file ALREADY exists on the receiver
			return 0;
		else:
			os.remove(destination);                                                   # Remove the file if it is not same size as source
	elif not os.path.isdir(os.path.dirname(destination)):
		os.makedirs(os.path.dirname(destination));                                  # Create the destination directory
	if (verbose is not None):
		sys.stdout.write('Copying file: '+'/'.join(destination.split('/')[-3:]));   # Print information that the file is copying
		sys.stdout.flush();                                                         # Push it to the screen
	shutil.copyfile(source, destination);                                         # Attempt to copy the file
	for i in range(1,4):                                                          # Checks file size and tries to copy 3 times if sizes don't match
		if os.path.getsize(source) == os.path.getsize(destination):                 # IF the file sizes match
			if (verbose is not None):
				print 'Copy Successful!';                                               # Message that the file copy was successful
			return 0;                                                                 # Break out of the loop
		elif (i < 3):                                                               # ELIF the files do NOT match and it was the 3rd try, print error message
			os.remove(destination);                                                   # Delete the file on the receiver
			shutil.copyfile(source, destination);                                     # Recopy the file
		else:
			if (verbose is not None):
				print 'Copy FAILED after 3 attempts';                                   # Print copy failed message
			return 1;