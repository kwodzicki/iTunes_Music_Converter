#!/usr/bin/env python
#+
# Name:
#   print_flac_meta
# Purpose:
#   A function to print meta data from a flac file.
# Inputs:
#   file  : Full path to the file print metadata for
# Outputs:
#   Prints output to command line.
# Author and History:
#   Kyle R. Wodzicki    Created 22 May 2016.
#-

def print_flac_meta( file ):
	from flac_tags.parse_flac import parse_flac;                                  # Load the flac parser
	dict = parse_flac( file, meta_only=True );                                    # Parse only the metadata blocks in the file
	for i in dict:
		if i != 'FRAME' and dict[i]['info'] is not None:
			print i;                                                                  # Print out type of info
			for j in dict[i]['info']:
				print '  ','{:<30}'.format(j),':','{:<30}'.format(dict[i]['info'][j]);  # Print out all the info
			print '';                                                                 # Return an extra line between metadata types
	return 0;                                                                     # Return zero for finished cleanly