#!/usr/bin/env python
#+
# Name:
#   parse_SEEKTABLE
# Purpose:
#   A function to parse out all the information from the seekpoint block of a 
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
#-
def parse_SEEKTABLE(block):
	from flac_tags.extras.bit_funcs import get_int
	info = {};                                                                    # Initialize dictionary
	for i in range(0, len(block)/18):
		tag = 'SeekPoint_'+str(i);                                                  # Set tag name for ith seek point
		tmp = get_int_list( block[i*18:(i+1)*18] );                                 # Get bit string for current seek point info
		info[tag] = {'firstSample' : get_int( tmp[ 0: 8] ),
	               'offset'      : get_int( tmp[ 8:16] ),
	               'nSamples'    : get_int( tmp[16: 2] )};                        # Append seek point info to dictionary
	return info;                                                                  # Return the dictionary