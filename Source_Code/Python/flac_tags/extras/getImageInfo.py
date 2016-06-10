#!/usr/bin/env python
#+
# Name:
#   getImageInfo
# Purpose:
#   A function to get information about GIF, PNG, and JPEG files using python
#   with no non-standard libraries. The code was originally obtained from
#   http://code.google.com/p/bfg-pages/source/browse/trunk/pages/getimageinfo.py
#   with some modifications to extract extra information from the files.
# Inputs:
#   None.
# Outputs:
#   Returns image type, width, height
# Keywords:
#   file    : Path to the file to get information about
#   data    : input data from file in lieu of file name.
# Author and History:
#   Originally by bfg-pages.
#   Modified by Kyle R. Wodzicki    21 May 2016
#-
def getImageInfo(file = None, data = None):
	import StringIO
	from struct import unpack;
	if (data is None) and (file is None):
		print 'NO file or image data input!';
		return None;
	elif (data is None):
		data = open(file, 'rb').read();
	data = str(data);
	size = len(data);
	height = -1;
	width = -1;
	content_type = '';
	info = {'ext' : ''};
	# handle GIFs
	if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
			# Check to see if content_type is correct
			w, h = unpack("<HH", data[6:10]);
			info['ext']    = 'gif';
			info['type']   = 'image/gif'.encode('ascii');
			info['width']  = int( (unpack("<H", data[6: 8]))[0] );
			info['height'] = int( (unpack("<H", data[8:10]))[0] );
			
	# See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
	# Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
	# and finally the 4-byte width, height
	elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
				and (data[12:16] == 'IHDR')):
			info['ext']         = 'png';
			info['type']        = 'image/png'.encode('ascii');
			info['width']       = int( (unpack(">L", data[16:20]))[0] );
			info['height']      = int( (unpack(">L", data[20:24]))[0] );
			info['bit_depth']   = int( (unpack("B",  data[24:25]))[0] );
			info['color_type']  = int( (unpack("B",  data[25:26]))[0] );
			info['compression'] = int( (unpack("B",  data[26:27]))[0] );
			info['filter']      = int( (unpack("B",  data[27:28]))[0] );
			info['interlace']   = int( (unpack("B",  data[28:29]))[0] );
	# Maybe this is for an older PNG version.
	elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
			# Check to see if we have the right content type
			info['ext']    = 'png';
			info['type']   = 'image/png'.encode('ascii');
			info['width']  = int( (unpack(">L", data[ 8:12]))[0] );
			info['height'] = int( (unpack(">L", data[12:16]))[0] );

	# handle JPEGs
	elif (size >= 2) and data.startswith('\377\330'):
			info['ext']  = 'jpeg';
			info['type'] = 'image/jpeg'.encode('ascii');
			jpeg = StringIO.StringIO(data);
			jpeg.read(2);
			b = jpeg.read(1);
			try:
					while (b and ord(b) != 0xDA):
							while (ord(b) != 0xFF): b = jpeg.read(1);
							while (ord(b) == 0xFF): b = jpeg.read(1);
							if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
									jpeg.read(3);
									h, w = unpack(">HH", jpeg.read(4));
									break;
							else:
									jpeg.read(int(unpack(">H", jpeg.read(2))[0])-2);
							b = jpeg.read(1);
					info['width']  = int(w);
					info['height'] = int(h);
			except struct.error:
					pass;
			except ValueError:
					pass;

	return info;#content_type, width, height;