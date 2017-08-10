#!/usr/bin/env python
#+
# Name:
#   parse
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
from to_unicode import to_unicode
from struct import unpack
from flac_tags.extras.bit_funcs import get_int, get_last_bits

################################################################################
def SEEKTABLE(block):
	info = {};                                                                    # Initialize dictionary
	for i in range(0, len(block)/18):
		tag = 'SeekPoint_'+str(i);                                                  # Set tag name for ith seek point
		tmp = get_int_list( block[i*18:(i+1)*18] );                                 # Get bit string for current seek point info
		info[tag] = {'firstSample' : get_int( tmp[ 0: 8] ),
	               'offset'      : get_int( tmp[ 8:16] ),
	               'nSamples'    : get_int( tmp[16: 2] )};                        # Append seek point info to dictionary
	return info;                                                                  # Return the dictionary
################################################################################
def PICTURE(block):
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
################################################################################
def VORBIS_COMMENT(block):
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
################################################################################
def STREAMINFO(block):
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