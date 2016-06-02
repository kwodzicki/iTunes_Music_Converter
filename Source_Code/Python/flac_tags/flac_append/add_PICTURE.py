#!/usr/bin/env python
#+
# Name:
#   add_PICTURE
# Purpose:
#   A function to add picture information to a dictionary containing parsed_data 
#   information of a FLAC file.
# Inputs:
#   picture_file : Full path to the picture file
#   parsed_data       : Dictionary of parsed_data FLAC information
# Outputs:
#   Returns a dictionary of parsed_data information.
# Keywords:
#   picture_type : Type of picture to add as laid out in the FLAC specification.
#                    Default is 3 - Cover (front)
# Author and History:
#   Kyle R. Wodzicki     Created 24 May 2016
#-
def add_PICTURE(picture_file, parsed_data, picture_type = None):
	from struct import pack;                                                      # Import pack function from struct module
	from flac_tags.extras.getImageInfo import getImageInfo;                       # Import the get image info function
	from flac_tags.extras.picture_desc import picture_desc;                       # Import function to return description of picture
	
	img_info = getImageInfo (picture_file);                                       # Get information about the image
	if (img_info['type'] == 'image/gif'):
		print 'GIF images are NOT currently supported! Returning...';               # Print message if picture is of type GIF!
		return parsed_data;                                                         # Return data without adding image
	elif (img_info['type'] == 'image/png'):
		if 'bit_depth' in img_info:
			bits = 3 * img_info['bit_depth'];                                         # Use bit depth from file
		else:
			bits = 24;                                                                # Default bit depth of 24
	else:
		bits = 24;                                                                  # Default bit depth of 24
	
	if (picture_type is None):
		picture_type = 3;                                                           # Set default picture type if no type input
	else:
		picture_type = int(picture_type);                                           # Ensure that picture type is of type int
	new_bytes = list( pack('>L', picture_type) );                                 # Initialize new_bytes list with picture type
	
	n = len(img_info['type']);                                                    # Length of the MIME type
	new_bytes.extend( list( pack('>L', n) ) );                                    # Append length of MIME type to new_bytes
	new_bytes.extend( list( pack( str(n)+'s', img_info['type']) ) );              # Append MIME type to new_bytes
	
	pic_desc = picture_desc(picture_type);                                        # Get generic picture description. This will match the description of picture types given in the FLAC format specification
	n = len(pic_desc);                                                            # Length of the MIME type
	new_bytes.extend( list( pack('>L', n) ) );                                    # Append length of MIME type to new_bytes
	new_bytes.extend( list( pack( str(n)+'s', pic_desc) ) );                      # Append MIME type to new_bytes
	
	new_bytes.extend( list( pack('>L', img_info['width']) ) );                    # Append image width to new_bytes
	new_bytes.extend( list( pack('>L', img_info['height']) ) );                   # Append image height to new_bytes
	new_bytes.extend( list( pack('>L', bits) ) );                                 # Append length of MIME type to new_bytes
	new_bytes.extend( list( pack('>L', 0) ) );                                    # Append number of colors used for indexed-color pictures. These are NOT supported in flac_tagger, so zero

	pic_data = open(picture_file, 'rb').read()
	n = len(pic_data)
	new_bytes.extend( list( pack('>L', n) ) );                                    # Append length of the picture data to new_bytes
	new_bytes.extend( pic_data );                                                 # Append picture data to new_bytes
	
	metablock = pack('>L', (6 << 24) + len(new_bytes) );                          # Generate the metadata block
	new_bytes = list(metablock) + new_bytes;                                      # Prepend metadata block to bytes list
	
	info = {'MIME_Type'    : img_info['type'], 
	        'Description' : pic_desc, 
	        'width'       : img_info['width'], 
	        'height'      : img_info['height'], 
	        'color_depth' : bits, 
	        'ncolors'     : 0};                                                   # Structure of all image information
	parsed_data['PICTURE'] = {'info' : info, 'bytes' : new_bytes};                # Update the dictionary
	return parsed_data;                                                           # Return updated parsed data