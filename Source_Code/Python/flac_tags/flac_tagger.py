#!/usr/bin/env python

from struct import pack, unpack;                                                # Import pack function from struct module
from . import parse;
from extras.bit_funcs    import get_int_list, get_int, get_bit
from extras.getImageInfo import getImageInfo;                                   # Import the get image info function

class flac_tagger():
	'''
	Name:
		flac_tagger
	Purpose:
		A python program to write vorbis comments and embed picture(s) in a 
		FLAC audio file.
	Input:
		file : Path to the flac file to use.
	Outputs:
		None, newly tagged file undersame name as input.
	Keywords:
		key_dict    : A dictionary containing keywords and their associated value.
										If this is set, the data is parsed into kargs.
	 Possible optional inputs:
		artist      : Set to artist for the given track. Optional input!
		album       : Set to album for the given track. Optional input!
		albumartist : Set to album artist for the given track. Optional input!
		bpm         : Set to bpm for the given track. Optional input!
		composer    : Set to composer for the given track. Optional input!
		comment     : Set to comment for the given track. Optional input!
		discnumber  : Set to disc number for the given track. Optional input!
		disctotal   : Set to total discs for the given track. Optional input!
		genre       : Set to genre for the given track. Optional input!
		grouping    : Set to grouping for the given track. Optional input!
		conductor   : Set to conductor for the given track. Optional input!
		compilation : Set to compilation for the given track. Optional input!
		lyrics      : Set to lyrics for the given track. Optional input!
		picture     : Set to picture for the given track. Optional input!
		picturetype : Set to picture type for the given track. Optional input!
		rating      : Set to rating for the given track. Optional input!
		remove      : Set to remove for the given track. Optional input!
		song        : Set to song for the given track. Optional input!
		skip        : Set to skip for the given track. Optional input!
		tracknumber : Set to track count for the given track. Optional input!
		tracktotal  : Set to total tracks for the given track. Optional input!
		year        : year. Optional input!
	Author and History:
		Kyle R. Wodzicki     Created 22 May 2016

		Modified 18 Nov. 2016 by Kyle R. Wodzicki
			Fixed an issue with code that was ment to support multiple images in 
			the future. The file paths were to be separated by commas, however this
			created an issue for file paths that had commas in them. The code
			has been commented out and will (hopefully) be implemented in the future.
		Modified 02 Aug. 2017 by Kyle R. Wodzicki
			Converted to a class
	'''
	def __init__(self, file, key_dict = None, **kargs):
		self.file         = file;                                                   # Initialize file attribute
		self.stream_info  = None;                                                   # Initialize streaminfo information attribute
		self.stream_byte  = None;                                                   # Initialize streaminfo byte attribute
		self.padding_info = None;                                                   # Initialize padding information attribute
		self.padding_byte = None;                                                   # Initialize padding byte attribute
		self.app_id       = None;                                                   # Initialize application id attribute
		self.app_data     = None;                                                   # Initialize application data attribute
		self.app_byte     = None;                                                   # Initialize application byte attribute
		self.seek_info    = None;                                                   # Initialize seektable information attribute
		self.seek_byte    = None;                                                   # Initialize seektable byte attribute
		self.vorbis_info  = None;                                                   # Initialize vorbiscomment information attribute
		self.vorbis_byte  = None;                                                   # Initialize vorbiscomment byte attribute
		self.cue_info     = None;                                                   # Initialize cuesheet information attribute
		self.cue_byte     = None;                                                   # Initialize cuesheet byte attribute
		self.picture_info = None;                                                   # Initialize picture information attribute
		self.picture_byte = None;                                                   # Initialize picture byte attribute
		self.frame        = None;                                                   # Initialize frame attribute
		
		self.pictures     = None;
		self.picture_type = None;
		self.status       = 0;

		self._parse( );                                                             # Parse all data from the FLAC file
		for i in kargs:                                                             # Iterate overall keyword arguments in the kargs dictionary
			if kargs[i] is None: del kargs[i];                                        # If an argument is None, delete it from the dictionary
		if key_dict is not None:                                                    # If key_dict is not None
			for i in key_dict: kargs[i.lower()] = key_dict[i];                        # Iterate over all the entries in the key_dict dictionary and add/update them in kargs dictionary

		if 'remove' in kargs:                                                       # If the remove tag is in the kargs dictionary
			print 'Removing data...';                                                 # Verbose output
			for i in kargs['remove'].split(','):                                      # Iterate of the list of tags to remove after splitting the list on comma (,)
				if i.upper() == 'PICTURE':                                              # If the picture is to be removed
					self.picture_info = None;                                             # Set picture_info attribute to None
				elif i.upper() == 'ALL':                                                # If ALL is set
					self.vorbis_info = None;                                              # Set vorbis_info to None
				else:                                                                   # Else
					if self.vorbis_info is not None:                                      # If the vorbis_info attribute is not None 
						if i.upper() in self.vorbis_info:                                   # if the tag is in vorbis_info attribute
							del self.vorbis_info[i.upper()];                                  # Delete the tag from vorbis_info attribute
			del kargs['remove'];                                                      # Delete the remove tag from kargs
		
		if len(kargs) > 0:                                                          # If the kargs dictionary has entries
			if self.vorbis_info is None: self.vorbis_info = {};                       # If the vorbis_info attribute is None, set to empty dictionary
			for i in kargs:                                                           # Iterate over all entires in the kargs dictionary
			  if i.upper() != 'PICTURE': self.vorbis_info[i.upper()] = kargs[i];      # If the entry is NOT a picture then add/update information in the vorbis_info attribute
			self.VORBIS_TO_BYTES( );                                                  # Update vorbis comment in parsed data
	
		if 'picture' in kargs:                                                      # If picture is in the kargs dictionary
			self.pictures = kargs['picture'];                                         # Split list of pictures on comma
			if 'picturetype' in kargs: self.picture_type = kargs['picturetype'];      # Set picture art type to user defined
			self.PICTURE_TO_BYTES( );                                                 # Update the picture data in parsed data
################################################################################
	def VORBIS_TO_BYTES( self ):
		'''
		Name:
			VORBIS_TO_BYTES
		Purpose:
			A function to convert a dictionary of vorbis comments to
			a byte string
		Inputs:
			None.
		Outputs:
			Updates the vorbis_byte attribute of the class
		Keywords:
			None.
		Author and History:
			Kyle R. Wodzicki     Created 10 Aug. 2017
		'''
		if self.vorbis_info is None:
			self.vorbis_byte = None; return;
		ninfo   = len( self.vorbis_info );
		new_bytes = [];                                                             # Initialize list to place all comment info in
		if 'VENDER' not in self.vorbis_info:
			new_bytes.extend( pack('<L', 0) );                                        # If there is not a Vorbis comment section in the parsed data, skip past vender length and vender string
		else:
			tmp  = self.vorbis_info['VENDER'].encode('utf-8');                        # Encode the vender string from the info dictionary to utf-8
			ntmp = len(tmp);                                                          # Get length of the vender string
			new_bytes.extend( list( pack('<L', ntmp) ) );                             # Append vender length (little endian) to the new_bytes list
			new_bytes.extend( list( pack( str(ntmp)+'s', tmp ) ) );                   # Add the vender string to the new_bytes string; packed as string
		new_bytes.extend( list( pack('<L', ninfo) ) );                              # Append number of user comments length (little endian) to the new_bytes list
		keys, values = self.vorbis_info.keys(), self.vorbis_info.values();          # Get the keys and the values of the info dictionary
		for i in range(0, ninfo):
			if (keys[i].upper() == 'RATING'):
				tmp = comment( [keys[i], convert_rating(values[i]) ] );                 # Build the new comment using above lambda command with star rating converted to usable number
			else:
				tmp = comment( [keys[i], values[i]] );                                  # Build the new comment using above lambda command
			ntmp = len(tmp);                                                          # Get the length of the comment
			new_bytes.extend( list( pack('<L', ntmp) ) );                             # Append comment length (little endian) to the new_bytes list
			new_bytes.extend( pack(str(ntmp)+'s', tmp ) );	                          # Append user comment to the new_bytes string; packed as string
		self.vorbis_byte  = list( pack('>L', (4 << 24)+len(new_bytes)) )+new_bytes; # Generate the metadata block
################################################################################
	def PICTURE_TO_BYTES( self ):
		'''
		Name:
			PICTURE_TO_BYTES
		Purpose:
			A function to convert a dictionary of picture information to
			a byte string
		Inputs:
			None.
		Outputs:
			Updates the picture_byte attribute of the class
		Keywords:
			None.
		Author and History:
			Kyle R. Wodzicki     Created 10 Aug. 2017
		'''
		if self.pictures is None: return;                                           # If the pictures attribute is None, then return
		self.picture_info = {};                                                     # Initialize the picture_info attribute to a dictionary
		self.picture_byte = [];                                                     # Initialize the picture_byte attribute as a list
		pics = self.pictures.split(',');                                            # Set pics to the list of pictures split on comma (,)
		if self.picture_type is not None:                                           # If the pictype attribute is not None
			type = [int(i) for i in self.picture_type.split(',')];                    # Iterate over each picture type after splitting on comma (,) and convert each string to an integer
			if len(type) < len(pics): type += [3] * (len(pics) - len(type));          # If the length of type is less than that of pic, extend it with 3, i.e., front cover
		else:                                                                       # Else, the pictype attribute was NOT set                
			type = [3] * len(pics);                                                   # Set all types to 3, i.e., front cover

		for i in range( len(pics) ):		                                            # Iterate over all pictures
			img_info = getImageInfo(file = pics[i]);                                  # Get information about the image
			if (len(img_info) == 0): return;                                          # Return i.e., skip adding the image
			if (img_info['type'] == 'image/gif'):
				print 'GIF images are NOT currently supported! Returning...';           # Print message if picture is of type GIF!
				return parsed_data;                                                     # Return data without adding image
			elif (img_info['type'] == 'image/png'):
				if 'bit_depth' in img_info:
					bits = 3 * img_info['bit_depth'];                                     # Use bit depth from file
				else:
					bits = 24;                                                            # Default bit depth of 24
			else:
				bits = 24;                                                              # Default bit depth of 24

			bytes = list( pack('>L', type[i]) );                                      # Initialize bytes list with picture type
			n = len(img_info['type']);                                                # Length of the MIME type
			bytes.extend( list( pack('>L', n) ) );                                    # Append length of MIME type to bytes
			bytes.extend( list( pack( str(n)+'s', img_info['type']) ) );              # Append MIME type to bytes
	    
			pic_desc = picture_desc[ type[i] ];                                       # Get generic picture description. This will match the description of picture types given in the FLAC format specification
			n = len(pic_desc);                                                        # Length of the MIME type
			bytes.extend( list( pack('>L', n) ) );                                    # Append length of MIME type to bytes
			bytes.extend( list( pack( str(n)+'s', pic_desc) ) );                      # Append MIME type to bytes
	    
			bytes.extend( list( pack('>L', img_info['width']) ) );                    # Append image width to bytes
			bytes.extend( list( pack('>L', img_info['height']) ) );                   # Append image height to bytes
			bytes.extend( list( pack('>L', bits) ) );                                 # Append length of MIME type to bytes
			bytes.extend( list( pack('>L', 0) ) );                                    # Append number of colors used for indexed-color pictures. These are NOT supported in flac_tagger, so zero
    
			pic_data = open(pics[i], 'rb').read();
			n = len(pic_data);    
			bytes.extend( list( pack('>L', n) ) );                                    # Append length of the picture data to bytes
			bytes.extend( pic_data );                                                 # Append picture data to bytes
	    
			self.picture_info[i] = {'MIME_Type'   : img_info['type'], 
													    'Description' : pic_desc, 
													    'width'       : img_info['width'], 
													    'height'      : img_info['height'], 
													    'color_depth' : bits, 
													    'ncolors'     : 0};                               # Structure of all image information	
			self.picture_byte += list( pack('>L', (6 << 24)+len(bytes)) ) + bytes;    # Generate the metadata block
################################################################################
	def print_meta( self ):
		for i in ['stream_info','padding_info','app_id','seek_info','vorbis_info','cue_info','picture_info']:
			tmp = getattr(self, i);
			if tmp is None: continue;
			print i,':';
			for j in tmp: print '  {:<30}:{:<30}'.format(j, tmp[j]);                  # Print out all the info
			print '';                                                                 # Return an extra line between metadata types
################################################################################
	def write( self ):
		with open(self.file, 'wb') as f:                                            # Open file for writing
			f.write( bytearray('fLaC') );                                             # Write fLaC header to file
			if self.stream_byte is not None: 
				f.write( bytearray( self.stream_byte ) );
			if self.app_byte is not None:
				f.write( bytearray( self.app_byte ) );
			if self.seek_byte is not None: 
				f.write( bytearray( self.seek_byte ) );
			if self.vorbis_byte is not None:
				f.write( bytearray( self.vorbis_byte ) );
			if self.cue_byte is not None: 
				f.write( bytearray( self.cue_byte ) );
			if self.picture_byte is not None:
				f.write( bytearray( self.picture_byte ) );
			if self.padding_byte is not None:
				block = self.padding_byte;                                              # Get list of bytes from ith parsed data
				type = int( (unpack('B', block[0]))[0] );                               # If it is the padding block, this is the last metadata block before the frame(s)
				if type < 128:
					type+= 128;                                                           # If the type is less than 128, add 128 to signify last metadata block
					block[0] = str(type);                                                 # Replace first byte in block with new type
				f.write( bytearray(block) );                                            # Write the block to the file
			if self.frame is not None: 
				f.write( bytearray( self.frame ) );
################################################################################
	def _parse(self, meta_only = False):
		bytes  = open(self.file, 'rb').read();
		start  = 4;                                                                   # Skip first four bytes, i.e., 'fLaC' text
		final  = False
		while final is False:
			block_type = get_int( get_int_list( bytes[start] ) );		
			if (block_type >= 128):
				block_type -= 128;
				final       = True;
			size_list = get_int_list( bytes[start+1:start+4] ) ;
			size      = get_int( size_list );
			end = start + 4 + size
			if (block_type == 0):
				self.stream_info = parse.STREAMINFO( bytes[start+4:end] );
				self.stream_byte = bytes[start:end];                                   # Get Stream information and new offset
			elif (block_type == 1):
				self.padding_info = None;
				self.padding_byte = bytes[start:end];          # Get Padding offset and size
			elif (block_type == 2):
				self.app_info = bytes[start+4:start+8];
				self.app_data = bytes[start+8:end]; 
				self.app_byte = bytes[start:end];                        # Get Stream information and new offset
			elif (block_type == 3):
				self.seek_info = parse.SEEKTABLE(bytes[start+4:end]);
				self.seek_byte = bytes[start:end];
			elif (block_type == 4):
				self.vorbis_info = parse.VORBIS_COMMENT(bytes[start+4:end]);
				self.vorbis_byte = bytes[start:end];
			elif (block_type == 5):
				self.cue_info = None;
				self.cue_byte = bytes[start:end];
			elif (block_type == 6):
				self.picture_info = parse.PICTURE(bytes[start+4:end]);
				self.picture_byte = bytes[start:end];
			start = end;
		if (meta_only is False): self.frame = bytes[start:];            # Append actual song information
################################################################################
def comment( x ):
  return x[0].upper().encode('ascii')+'='+to_unicode(x[1]).encode('utf-8');     # Function to generate vorbis user fields
################################################################################
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
################################################################################
def to_unicode(obj, encoding = None):
	if (encoding is None):
		encoding = 'utf-8';                # Set the default encoding
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding);    # If the input is NOT unicode, convert it
	return obj;                          # Return the object
################################################################################
# A dictionary of picture descriptions for images
picture_desc = { 0 : 'Other'.encode('utf-8'),
                 1 : 'File Icon'.encode('utf-8'),
                 2 : 'Other file icon'.encode('utf-8'),
                 3 : 'Cover (front)'.encode('utf-8'),
                 4 : 'Cover (back)'.encode('utf-8'),
                 5 : 'Leaflet page'.encode('utf-8'),
                 6 : 'Media'.encode('utf-8'),
                 7 : 'Lead artist/lead performer/soloist'.encode('utf-8'),
                 8 : 'Artist/performer'.encode('utf-8'), 
                 9 : 'Conductor'.encode('utf-8'),
                10 : 'Band/Orchestra'.encode('utf-8'),
                11 : 'Composer'.encode('utf-8'),
                12 : 'Lyricist/text writer'.encode('utf-8'),
                13 : 'Recording Location'.encode('utf-8'),
                14 : 'During recording'.encode('utf-8'),
                15 : 'During performance'.encode('utf-8'),
                16 : 'Movie/video screen capture'.encode('utf-8'),
                17 : 'A bright coloured fish'.encode('utf-8'),
                18 : 'Illustration'.encode('utf-8'),
                19 : 'Band/artist logotype'.encode('utf-8'),
                20 : 'Publisher/Studio logotype'.encode('utf-8')}
                
################################################################################
# Set up command line arguments for the function
if __name__ == "__main__":
	import argparse;                                                              # Import library for parsing
	parser = argparse.ArgumentParser(description="Tagger for FLAC File");         # Set the description of the script to be printed in the help doc, i.e., ./script -h
	# Add all the command line arguments
	parser.add_argument("file",                metavar="file",         type=str, \
	  help="Full path to the FLAC file to edit.");                                # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-a", "--artist",      metavar="artist",       type=str, \
	  help="Artist/Performer for the track."); 
	parser.add_argument("-A", "--album",       metavar="album",        type=str, \
	  help="Album the track is from."); 
	parser.add_argument("-b", "--albumartist", metavar="albumartist",  type=str, \
	  help="Artist for the album."); 
	parser.add_argument("-B", "--bpm",         metavar="bpm",          type=str, \
	  help="Beats per minute for the track."); 
	parser.add_argument("-c", "--composer",    metavar="composer",     type=str, \
	  help="Composer of the track."); 
	parser.add_argument("-C", "--comment",     metavar="comment",      type=str, \
	  help="Comment for the track."); 
	parser.add_argument("-d", "--discnumber",  metavar="discnumber",   type=str, \
	  help="Number of the disk the trak is on."); 
	parser.add_argument("-D", "--disctotal",   metavar="disctotal",    type=str, \
	  help="Total number of disk in the album."); 
	parser.add_argument("-g", "--genre",       metavar="genre",        type=str, \
	  help="Genre of the track.");
	parser.add_argument("-G", "--grouping",    metavar="grouping",     type=str, \
	  help="Grouping for the track.");
	parser.add_argument("-k", "--conductor",   metavar="conductor",    type=str, \
	  help="Conductor for the track."); 
	parser.add_argument("-K", "--compilation", metavar="compilation",  type=str, \
	  help="If track is part of a compilation. 0 for no, 1 for yes.");  
	parser.add_argument("-l", "--lyrics",      metavar="lyrics",       type=str, \
	  help="Lyrics for the track."); 
	parser.add_argument("-n", "--tracktotal",  metavar="tracktotal",   type=str, \
	  help="Total number of tracks.");   
	parser.add_argument("-p", "--picture",     metavar="picture",      type=str, \
	  help="Comma separated list of picture file(s) for the track."); 
	parser.add_argument("-P", "--picturetype", metavar="picturetype",  type=str, \
	  help="Comma separated list of picture type(s) correspoding to the picture(s) for the track."); 
	parser.add_argument("-r", "--rating",      metavar="rating",       type=str, \
	  help="Rating for the track; 0-5 stars"); 
	parser.add_argument("-R", "--remove",      metavar="remove",       type=str, \
	  help="Comma separated list of tags to remove. Removing picture removes ALL pictures."); 
	parser.add_argument("-s", "--skip",        metavar="skip",         type=str, \
	  help="If the song is to be skipped when shuffling. 0 for no, 1 for yes.");
	parser.add_argument("-t", "--title",       metavar="title",        type=str, \
	  help="Name of the track."); 
	parser.add_argument("-T", "--tracknumber", metavar="tracknumber",  type=str, \
	  help="Track number.");
	parser.add_argument("-y", "--date",        metavar="date",         type=str, \
	  help="Year track was released.");   
	
	args = parser.parse_args();                                                   # Parse the arguments
	x = flac_tagger( args.file, \
	  artist      = args.artist, \
	  album       = args.album, \
	  albumartist = args.albumartist, \
	  bpm         = args.bpm, \
	  composer    = args.composer, \
	  comment     = args.comment, \
	  disccount   = args.discnumber, \
	  disctotal   = args.disctotal, \
	  genre       = args.genre, \
	  grouping    = args.grouping, \
	  conductor   = args.conductor, \
	  compilation = args.compilation, \
	  lyrics      = args.lyrics, \
	  picture     = args.picture, \
	  picturetype = args.picturetype, \
	  rating      = args.rating, \
	  remove      = args.remove, \
	  skip        = args.skip, \
	  title       = args.title, \
	  tracknumber = args.tracknumber, \
	  tracktotal  = args.tracktotal, \
	  date        = args.year);                                           # Call the tagger program
	x.write();
	exit( x.status );