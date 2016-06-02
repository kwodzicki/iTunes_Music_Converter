#!/usr/bin/env python
#+
# Name:
#   flac_tagger
# Purpose:
#   A python program to write vorbis comments and embed picture(s) in a 
#   FLAC audio file.
# Input:
#   file : Path to the flac file to use.
# Outputs:
#   None, newly tagged file undersame name as input.
# Keywords:
#   key_dict    : A dictionary containing keywords and their associated value.
#                   If this is set, the data is parsed into kargs.
#  Possible optional inputs:
#   artist      : Set to artist for the given track. Optional input!
# 	album       : Set to album for the given track. Optional input!
# 	albumartist : Set to album artist for the given track. Optional input!
# 	bpm         : Set to bpm for the given track. Optional input!
# 	composer    : Set to composer for the given track. Optional input!
# 	comment     : Set to comment for the given track. Optional input!
# 	discnumber  : Set to disc number for the given track. Optional input!
# 	disctotal   : Set to total discs for the given track. Optional input!
# 	genre       : Set to genre for the given track. Optional input!
# 	grouping    : Set to grouping for the given track. Optional input!
# 	conductor   : Set to conductor for the given track. Optional input!
# 	compilation : Set to compilation for the given track. Optional input!
# 	lyrics      : Set to lyrics for the given track. Optional input!
# 	picture     : Set to picture for the given track. Optional input!
# 	picturetype : Set to picture type for the given track. Optional input!
# 	rating      : Set to rating for the given track. Optional input!
# 	remove      : Set to remove for the given track. Optional input!
# 	song        : Set to song for the given track. Optional input!
# 	skip        : Set to skip for the given track. Optional input!
# 	tracknumber : Set to track count for the given track. Optional input!
# 	tracktotal  : Set to total tracks for the given track. Optional input!
# 	year        : year. Optional input!
# Author and History:
#   Kyle R. Wodzicki     Created 22 May 2016
#
# Note that only one (1) picture is currently supported!
#-


def flac_tagger(file, key_dict = None, **kargs):
	import flac_tags as ft
	if (key_dict is not None):
		kargs={};
		for i in key_dict:
			kargs[i.lower()] = key_dict[i];
	notNone=0;                                                                    # Initialize counter to count how many keywords are set, i.e., are NOT none
	for i in kargs:
		if (kargs[i] is not None):
			notNone+=1;                                                               # Increment the counter if a keyword is NOT none
	if len(kargs) == 0 or notNone == 0:
		return_code = ft.extras.print_flac_meta( file );                                   # Print out only flac metadata
	else:
		data   = ft.parse_flac( file );                                             # Parse all data from the file
		vorbis = data['VORBIS_COMMENT']['info']
		if 'remove' in kargs:
			if kargs['remove'] is not None:
				print 'Removing data...'
				for i in kargs['remove'].split(','):
					if i.upper() == 'PICTURE':
						del data['PICTURE'];                                                # Delete picture data from dictionary
					else:
						if i.upper() == 'ALL':
							vorbis = {};                                                      # Remove all tags, i.e., initialize vorbis comment structure
						else:
							del vorbis[i.upper()];                                            # Delete given comment
		if 'artist' in kargs:
			if kargs['artist'] is not None:      vorbis['ARTIST']      = kargs['artist'];
		if 'album' in kargs:
			if kargs['album'] is not None:       vorbis['ALBUM']       = kargs['album'];
		if 'albumartist' in kargs:
			if kargs['albumartist'] is not None: vorbis['ALBUMARTIST'] = kargs['albumartist'];
		if 'bpm' in kargs:
			if kargs['bpm'] is not None:         vorbis['BPM']         = kargs['bpm'];
		if 'composer' in kargs:
			if kargs['composer'] is not None:    vorbis['COMPOSER']    = kargs['composer'];
		if 'comment' in kargs:
			if kargs['comment'] is not None:     vorbis['COMMENT']     = kargs['comment'];
		if 'discnumber' in kargs:
			if kargs['discnumber'] is not None:  vorbis['DISCNUMBER']  = kargs['discnumber'];
		if 'disctotal' in kargs:
			if kargs['disctotal'] is not None:   vorbis['DISCTOTAL']   = kargs['disctotal'];
		if 'genre' in kargs:
			if kargs['genre'] is not None:       vorbis['GENRE']       = kargs['genre'];
		if 'grouping' in kargs:
			if kargs['grouping'] is not None:    vorbis['GROUPING']    = kargs['grouping'];
		if 'conductor' in kargs:
			if kargs['conductor'] is not None:   vorbis['CONDUCTOR']   = kargs['conductor'];
		if 'compilation' in kargs:
			if kargs['compilation'] is not None: vorbis['COMPILATION'] = kargs['compilation'];
		if 'lyrics' in kargs:
			if kargs['lyrics'] is not None:      vorbis['LYRICS']      = kargs['lyrics'];
		if 'rating' in kargs:
			if kargs['rating'] is not None:      vorbis['RATING']      = kargs['rating'];
		if 'skip' in kargs:
			if kargs['skip'] is not None:        vorbis['SKIP']        = kargs['skip'];
		if 'title' in kargs:
			if kargs['title'] is not None:       vorbis['TITLE']       = kargs['title'];
		if 'tracknumber' in kargs:
			if kargs['tracknumber'] is not None: vorbis['TRACKNUMBER'] = kargs['tracknumber'];
		if 'tracktotal' in kargs:
			if kargs['tracktotal'] is not None:  vorbis['TRACKTOTAL']  = kargs['tracktotal'];
		if 'year' in kargs:
			if kargs['year'] is not None:        vorbis['DATE']        = kargs['year'];
		data = ft.flac_append.add_VORBIS_COMMENT(vorbis, data);                     # Update vorbis comment in parsed data

		if 'picture' in kargs:
			if (kargs['picture'] is not None):
				pics = kargs['picture'].split(',');                                     # Get list of pictures
				if (len(pics) > 1):
					print 'Currently only supports one (1) image. Only using first!';
				if 'picturetype' not in kargs:
					print 'No picture type defined, assuming front cover art!'
					pictype = '3';                                                        # Set picture art type to cover (front)
				elif kargs['picturetype'] is None:
					pictype = '3';                                                        # If picture type exists in kargs but is None, set to cover (front)
				else:
					pictype = kargs['picturetype'].split(',');                            # Set picture art type to user defined
					pictype = pictype[0];                                                 # IF more then one, use only first
				data = ft.flac_append.add_PICTURE(pics[0], data, picture_type=pictype); # Update the picture data in parsed data
		ft.write_flac( data, file );                                                # Write data to the file
	return 0;
	
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
	parser.add_argument("-y", "--year",        metavar="year",         type=str, \
	  help="Year track was released.");   
	
	args = parser.parse_args();                                                   # Parse the arguments
	return_code = flac_tagger( args.file, \
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
	  year        = args.year);                                                   # Call the tagger program
	
	if (return_code == 0):
		quit();
	else:
		print 'Something went wrong!!!';