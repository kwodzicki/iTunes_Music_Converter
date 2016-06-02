#!/usr/bin/env python
#+
# Name:
#   parse_VORBIS_COMMENT
# Purpose:
#   A function to parse out all the information from the vorbis comment
#   block of a FLAC file.
# Inputs:
#   block : Only the data for the block. NO metadata block header information
#           should be passed
# Outputs:
#   Returns a dictionary of parsed information.
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 17 May 2016
#-
def parse_VORBIS_COMMENT(block):
	from to_unicode import to_unicode
	from struct import unpack
	info = {};                                                                    # Initialize dictionary
	start, end = 0, 4;                                                            # Set the start and end points to get the vender length - a 32 bit integer
	length = (unpack('<L', block[start:end]))[0];                                 # Get the vender length - little endian encoding
	start, end  = end, end+length;                                                # Set new start and end points for the vendor string
	info['VENDER'] = block[start:end];                                            # Get the vendor string
	start, end = end, end+4;                                                      # Set new start and end points for the number of user comments
	length = (unpack('<L', block[start:end]))[0];                                 # Get the number of user comments - little endian
	start, end = end, end+4                                                       # Set new start and end points for the length of the first user comment
	for i in range(0, length):
		length = (unpack('<L', block[start:end]))[0];                               # Get length of the user comment
		start, end = end, end+length;                                               # Set new start and end points for the user comment
		comment = block[start:end].split('=');                                      # Get the user comment
		tag     = to_unicode(comment[0], encoding='ascii').encode('ascii');         # Get the field name for the comment
		value   = to_unicode(comment[1], encoding='utf-8').encode('utf-8');         # Get the value for the comment
		info[tag ] = value;                                                         # Add the comment to the dictionary
		start, end = end, end+4;                                                    # Set new start and end points for the length of the first user comment
	return info;                                                                  # Return the dictionary