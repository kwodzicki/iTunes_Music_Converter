#!/usr/bin/env python
#+
# Name:
#   parse_PICTURE
# Purpose:
#   A function to parse out all the information from the picture block of a 
#   FLAC file.
# Inputs:
#   block : Only the data for the block. NO metadata block header information
#           should be passed
# Outputs:
#   Returns a dictionary of parsed information.
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 17 May 2016
#
#  Modified 21 May 2016
#    Using unpack from the struct package to get information
#-
def parse_PICTURE(block):
	from struct import unpack
	info = {};                                                                    # Initialize dictionary
	info['type'] = (unpack('>L', block[0:4]))[0];                                 # Get the type of picture
	start, end = 4, 8;                                                            # Set start and end postions for MIME length (32 bits)
	for i in ['MIME_Type', 'Description']:
		len = (unpack('>L', block[start:end]))[0];                                  # Iterate to get MIME description and image description. First get length of descripter
		start, end = end, end+len;                                                  # Set new start and end points based on the length
		info[i] = block[start:end];                                                 # Add the description to the dictionary
		start, end = end, end+4;                                                    # Set new start and end points based for reading the next length
	for i in ['width', 'height', 'color_depth', 'ncolors']:
		info[i] = (unpack('>L', block[start:end]))[0];                              # Iterate to get image information. These are all 32 bits. Get the values for given info
		start, end = end, end+4;                                                    # Set new start and end points
		len = (unpack('>L', block[start:end]))[0];                                  # Iterate to get image information. These are all 32 bits. Get the values for given info
	return info;                                                                  # Return the dictionary