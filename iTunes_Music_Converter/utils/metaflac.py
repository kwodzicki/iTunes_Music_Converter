#!/usr/bin/env python
import os
import subprocess as sb;

def metaflac( file, **kwargs ):
	'''
	Name:
	   metaflac
	Purpose:
	   A python wraper for metaflac command line utility
	Inputs:
	   file : Path to file for tagging
	Keywords:
	   artist      : Artist/Performer for the track
	   album       : Album the track is from
	   albumartist : Artist for the album
	   bpm         : Beats per minute for the track
	   composer    : Composer of the track
	   comment     : Comment for the track
	   discnumber  : Number of the disk the trak is on
	   disctotal   : Total number of disk in the album
	   genre       : Genre of the track
	   grouping    : Grouping for the track
	   conductor   : Conductor for the track
	   compilation : If track is part of a compilation. 
	                   0 for no, 1 for yes
	   lyrics      : Lyrics for the track
	   tracktotal  : Total number of tracks  
	   picture     : Comma separated list of picture 
	                   file(s) for the track
	   picturetype : Comma separated list of picture 
	                   type(s) correspoding to the picture(s)
	                   for the track
	   rating      : Rating for the track; 0-5 stars
	   remove      : Comma separated list of tags to remove.
	                   Removing picture removes ALL pictures
	   REMOVE      : Set to remove all tags
	   skip        : If the song is to be skipped when shuffling.
	                   0 for no, 1 for yes
	   title       : Name of the track
	   tracknumber : Track number
	   date        : Year track was released
	'''
	cmdBase = "metaflac"
	cmd     =  [ [cmdBase], [cmdBase] ];
	removeAll = False
	if 'REMOVE' in kwargs:
		if kwargs['REMOVE']:
			cmd[0].append( "--remove-all-tags" );
			cmd[1].extend( ["--remove", "--block-type=PICTURE"] );
			removeAll = True;
		del kwargs['REMOVE'];                                                       # Delete the remove tag from kargs
	if 'remove' in kwargs and not removeAll:                                      # If the remove tag is in the kargs dictionary
		if kwargs['remove'] is not None:
			print( 'Removing data...' );                                              # Verbose output
			for i in kwargs['remove'].split(','):                                     # Iterate of the list of tags to remove after splitting the list on comma (,)
				if i.upper() == 'PICTURE':
					cmd[1].extend( ["--remove", "--block-type=PICTURE"] );
				else:		
					cmd[0].append( "--remove-tag={}".format(i.upper()) );
		del kwargs['remove'];                                                       # Delete the remove tag from kargs
	if len(kwargs) > 0 and not removeAll:                                         # If the kargs dictionary has entries
		for i in kwargs:                                                            # Iterate over all keywords
			if 'picture' in i: continue;                                              # Skip tags containing picture
			if kwargs[i] is not None:                                                 # If value is NOT None
				cmd[0].append( "--remove-tag={}".format(i.upper()) );                   # Append option to cmd
				cmd[0].append( "--set-tag={}={}".format(i.upper(), kwargs[i]) );        # Append option to cmd
	if 'picture' in kwargs and not removeAll:
		if kwargs['picture'] is not None:
			picType = 2;
			if 'picturetype' in kwargs:
				if kwargs['picturetype'] is not None: picType = kwargs['picturetype'];
			option = '--import-picture-from={}|{}|{}|{}x{}x{}|{}'
			cmd[0].append( option.format(picType,'','','','','',kwargs['picture'] ) );

	for c in cmd:	
		if len(c) == 1: continue;
		c.append( file );
		with open(os.devnull, 'w') as devnull:
			proc = sb.Popen( c, stdout=devnull, stderr=sb.STDOUT );
		proc.communicate();
	
if __name__ == "__main__":
	import argparse;                                                              # Import library for parsing
	parser = argparse.ArgumentParser(description="Tagger for FLAC File");         # Set the description of the script to be printed in the help doc, i.e., ./script -h
	# Add all the command line arguments
	parser.add_argument("file",                metavar="file",         type=str,
	  help="Full path to the FLAC file to edit.");                              # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-a", "--artist",      metavar="artist",       type=str,
	  help="Artist/Performer for the track."); 
	parser.add_argument("-A", "--album",       metavar="album",        type=str,
	  help="Album the track is from."); 
	parser.add_argument("-b", "--albumartist", metavar="albumartist",  type=str,
	  help="Artist for the album."); 
	parser.add_argument("-B", "--bpm",         metavar="bpm",          type=str,
	  help="Beats per minute for the track."); 
	parser.add_argument("-c", "--composer",    metavar="composer",     type=str,
	  help="Composer of the track."); 
	parser.add_argument("-C", "--comment",     metavar="comment",      type=str,
	  help="Comment for the track."); 
	parser.add_argument("-d", "--discnumber",  metavar="discnumber",   type=str,
	  help="Number of the disk the trak is on."); 
	parser.add_argument("-D", "--disctotal",   metavar="disctotal",    type=str,
	  help="Total number of disk in the album."); 
	parser.add_argument("-g", "--genre",       metavar="genre",        type=str,
	  help="Genre of the track.");
	parser.add_argument("-G", "--grouping",    metavar="grouping",     type=str,
	  help="Grouping for the track.");
	parser.add_argument("-k", "--conductor",   metavar="conductor",    type=str,
	  help="Conductor for the track."); 
	parser.add_argument("-K", "--compilation", metavar="compilation",  type=str,
	  help="If track is part of a compilation. 0 for no, 1 for yes.");  
	parser.add_argument("-l", "--lyrics",      metavar="lyrics",       type=str,
	  help="Lyrics for the track."); 
	parser.add_argument("-n", "--tracktotal",  metavar="tracktotal",   type=str,
	  help="Total number of tracks.");   
	parser.add_argument("-p", "--picture",     metavar="picture",      type=str,
	  help="Comma separated list of picture file(s) for the track."); 
	parser.add_argument("-P", "--picturetype", metavar="picturetype",  type=str,
	  help="Comma separated list of picture type(s) correspoding to the picture(s) for the track."); 
	parser.add_argument("-r", "--rating",      metavar="rating",       type=str,
	  help="Rating for the track; 0-5 stars"); 
	parser.add_argument("-R", "--remove",      metavar="remove",       type=str,
	  help="Comma separated list of tags to remove. Removing picture removes ALL pictures."); 
	parser.add_argument("--REMOVE",           action="store_true",
	  help="Set to remove all tags"); 
	parser.add_argument("-s", "--skip",        metavar="skip",         type=str,
	  help="If the song is to be skipped when shuffling. 0 for no, 1 for yes.");
	parser.add_argument("-t", "--title",       metavar="title",        type=str,
	  help="Name of the track."); 
	parser.add_argument("-T", "--tracknumber", metavar="tracknumber",  type=str,
	  help="Track number.");
	parser.add_argument("-y", "--date",        metavar="date",         type=str,
	  help="Year track was released.");   
	
	args = parser.parse_args();                                                   # Parse the arguments
	x = metaflac( args.file, \
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
	  REMOVE      = args.REMOVE, \
	  skip        = args.skip, \
	  title       = args.title, \
	  tracknumber = args.tracknumber, \
	  tracktotal  = args.tracktotal, \
	  date        = args.date);                                           # Call the tagger program
