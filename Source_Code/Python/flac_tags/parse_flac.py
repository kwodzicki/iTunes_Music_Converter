#!/usr/bin/env python
#+
# Name:
#   parse_flac
# Purpose:
#   A function to parse apart a FLAC audio file. This function iterates over
#   the file, determining the type of metadata block to be parsed, calling the
#   proper function to parse that block.
# Inputs:
#   file  : Full path tot the file to parse.
# Outputs:
#   Returns a dictionary containing the parsed information as well as the
#   corresponding bytes from the file.
# Keywords:
#   meta_only : Set to true to only return metadata. Setting to false will
#               return all frame information as well. Default is false.
# Author and History:
#   Kyle R. Wodzicki     Created 23 May 2016
#-

def parse_flac(file, meta_only = False):
	from flac_tags.extras.bit_funcs import get_int_list, get_int, get_bit
	import flac_tags.flac_parse as fp
	parsed = {}
	bytes  = open(file, 'rb').read();
	start  = 4;                                                                   # Skip first four bytes, i.e., 'fLaC' text
	final  = False
	while final is False:
		block_type = get_int( get_int_list( bytes[start] ) );
# 		print block_type
		
		if (block_type >= 128):
			block_type-=128
			final = True;
		size_list = get_int_list(bytes[start+1:start+4]) 
		size      = get_int( size_list )
		end = start + 4 + size
# 		print block_type, start, start+4, size, end
		if (block_type == 0):
			parsed['STREAMINFO'] = \
			  {'info'         : fp.parse_STREAMINFO(bytes[start+4:end]),
         'bytes'        : bytes[start:end]};                                    # Get Stream information and new offset
		elif (block_type == 1):
			parsed['PADDING'] = \
			  {'info'         : None,
			   'bytes'        : bytes[start:end]};          # Get Padding offset and size
		elif (block_type == 2):
			parsed['APPLICATION'] = \
			  {'info'         : {'appID'   : bytes[start+4:start+8], 
			                     'appData' : bytes[start+8:end]}, 
         'bytes'        : bytes[start:end]};                                    # Get Stream information and new offset
		elif (block_type == 3):
			parsed['SEEKTABLE'] = \
			  {'info'         : fp.parse_SEEKTABLE(bytes[start+4:end]),
         'bytes'        : bytes[start:end]};
		elif (block_type == 4):
			parsed['VORBIS_COMMENT'] = \
			  {'info'         : fp.parse_VORBIS_COMMENT(bytes[start+4:end]), 
         'bytes'        : bytes[start:end]};
		elif (block_type == 5):
			parsed['CUESHEET'] = \
			  {'info'         : None,
			   'bytes'        : bytes[start:end]};
		elif (block_type == 6):
			parsed['PICTURE'] = \
			  {'info'         : fp.parse_PICTURE(bytes[start+4:end]), 
         'bytes'        : bytes[start:end]};
		start = end;
	if (meta_only is False):
		parsed['FRAME'] = {'bytes' : bytes[start:]};                                # Append actual song information
	return parsed;