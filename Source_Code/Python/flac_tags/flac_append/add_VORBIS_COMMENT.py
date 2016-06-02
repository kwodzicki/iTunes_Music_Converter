#!/usr/bin/env python
#+
# Name:
#   add_VORBIS_COMMENT
# Purpose:
#   A function to add or update information in the Vorbis comment of a flac file
# Inputs:
#   info        : Dictionary containing comments to add/update. Keys in the 
#                 dictionary should be the field tag for that data with the 
#                 value being the actual comment.
#   parsed_data : Dictionary of parsed data from the flac file, i.e., dictionary
#                 returned by parse_flac_file function.
# Outputs:
#   Returns an updated dictionary of parsed information.
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 17 May 2016
#-

def convert_rating(rating):
	# A function to convert the number of stars for the rating into usable number.
	# This numbering is based on the numbering used by the Yate tagging program.
	if (rating == '0'):
		return '0';
	elif (rating == '1'):
		return '9';
	elif (rating == '2'):
		return '50';
	elif (rating == '3'):
		return '114';
	elif (rating == '4'):
		return '160';
	elif (rating == '5'):
		return '219';

def add_VORBIS_COMMENT(info, parsed_data):
	from to_unicode import to_unicode;
	from struct import pack;
	comment = lambda x: x[0].upper().encode('ascii')+'='+to_unicode(x[1]).encode('utf-8'); # Function to generate vorbis user fields
	new_bytes = [];                                                               # Initialize list to place all comment info in
	if 'VENDER' not in info:
		new_bytes.extend( pack('<L', 0) );                                          # If there is not a Vorbis comment section in the parsed data, skip past vender length and vender string
	else:
		tmp  = info['VENDER'].encode('utf-8');                                      # Encode the vender string from the info dictionary to utf-8
		ntmp = len(tmp);                                                            # Get length of the vender string
		new_bytes.extend( list( pack('<L', ntmp) ) );                               # Append vender length (little endian) to the new_bytes list
		new_bytes.extend( list( pack( str(ntmp)+'s', tmp ) ) );                     # Add the vender string to the new_bytes string; packed as string

	new_bytes.extend( list( pack('<L', len(info)) ) );                            # Append number of user comments length (little endian) to the new_bytes list
	keys, values = info.keys(), info.values();                                    # Get the keys and the values of the info dictionary
	for i in range(0, len(info)):
		if (keys[i].upper() == 'RATING'):
			tmp = comment( [keys[i], convert_rating(values[i]) ] );                   # Build the new comment using above lambda command with star rating converted to usable number
		else:
			tmp  = comment( [keys[i], values[i]] );                                   # Build the new comment using above lambda command
		ntmp = len(tmp);                                                            # Get the length of the comment
		new_bytes.extend( list( pack('<L', ntmp) ) );                               # Append comment length (little endian) to the new_bytes list
		new_bytes.extend( pack(str(ntmp)+'s', tmp ) );	                            # Append user comment to the new_bytes string; packed as string
	metablock = pack('>L', (4 << 24) + len(new_bytes) );                          # Generate the metadata block
	new_bytes = list(metablock) + new_bytes;                                      # Prepend metadata block to bytes list
	parsed_data['VORBIS_COMMENT'] = {'info' : info, 'bytes' : new_bytes};         # Update the dictionary
	return parsed_data;                                                           # Return the dictionary