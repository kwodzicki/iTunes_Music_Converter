#!/usr/bin/env python
#+
# Name:
#   parse_STREAMINFO
# Purpose:
#   A function to parse out all the information from the stream information
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
def parse_STREAMINFO(block):
	from struct import unpack
	from flac_tags.extras.bit_funcs import get_int, get_last_bits
	info = {};                                                                    # Initialize dictionary
	info['minBlock'] = (unpack('>H', block[0: 2]))[0];                            # Add minimum block size to dictionary
	info['maxBlock'] = (unpack('>H', block[2: 4]))[0];                            # Add maximum block size to dictionary
	info['minFrame'] = get_int( unpack('3B', block[4: 7]) );                      # Add minimum frame size to dictionary
	info['maxFrame'] = get_int( unpack('3B', block[7:10]) );                      # Add maximum frame size to dictionary
	tmp = list( unpack('8B', block[10:18]) );                                     # Get next 8 bytes as bit strings for parsing as they are not clean, i.e., bytes are split
	info['sampleRate']    = get_int( tmp[0:3] ) >> 4;                             # Combine the first 3 bytes into one 24 bit number, then shift to right so only 20 bits        
	info['nChannels']     = get_last_bits(tmp[2], 3, offset=1) + 1;               # Get three bits, starting one in from the right, from the third byte. This will extract the 2^1, 2^2, and 2^3 bits from the 3 byte
	info['bitsPerSample'] = (get_last_bits(tmp[2], 1) << 4) + (tmp[3] >> 4) + 1;  # Get last bit, starting from the right, from the third byte and combine with first 4 bits of fourth byte to create 5 bit integer
	info['totSamples']    = get_int( [get_last_bits(tmp[3], 4)] + tmp[4:] );      # Get last four bits, starting from the right, from the fourth byte and combine with next 4 bytes.
# 	info['MD5']           = block[18:];                                           # All remaining bytes
	return info;                                                                  # Return the info