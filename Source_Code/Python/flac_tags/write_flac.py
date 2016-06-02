#!/usr/bin/env python
#+
# Name:
#   write_flac
# Purpose:
#   A function to create a flac file based on parsed data from a flac file.
# Inputs:
#   parsed_data : A dictionary of information from a flac file. This information
#                 can be obtained using flac_parse/parse_file_file.py
#   file        : Full path to the file to create.
# Outputs:
#   Creates a flac file at 'file'
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 17 May 2016
#-

def write_flac(parsed_data, file):
	from struct import unpack;                                                    # Import unpack from struct module
	f = open(file, 'wb');                                                         # Open file for writing
	f.write( bytearray('fLaC') );                                                 # Write fLaC header to file
	order = ['STREAMINFO',  'APPLICATION', 'SEEKTABLE', 'VORBIS_COMMENT', \
	         'CUESHEET',    'PICTURE',     'PADDING',   'FRAME'];                 # Set the order in which to write the various metadata blocks
	for i in order:
		if i in parsed_data:
			block = parsed_data[i]['bytes'];                                          # Get list of bytes from ith parsed data
			if i == 'PADDING':
				type = int( (unpack('B', block[0]))[0] );                               # If it is the padding block, this is the last metadata block before the frame(s)
				if type < 128:
					type+= 128;                                                           # If the type is less than 128, add 128 to signify last metadata block
					block[0] = str(type);                                                 # Replace first byte in block with new type
			f.write( bytearray(block) );                                              # Write the block to the file
	f.close();                                                                    # Close the file
	return 0;                                                                     # Return zero for clean exit