#!/usr/bin/env python
######################################################################
# A python program to get audio track information from the iTunes    #
# XML library file and convert them to either MP3 or FLAC. Any file  #
# that is an MP3 will be copied, regardless of the codec, with all   #
# other file types convert to either MP3 or FLAC. An attempt to      #
# download cover art for the album is also made, with cover art      #
# saved in the Artist/Album directory as coverart.jpeg. This is done #
# through the musicbrainzngs.                                        #
#                                                                    #
# Created on 24 May. 2016 by Kyle R. Wodzicki                        #
#                                                                    #
# All rights reserved.                                               #
#                                                                    #
# For more information see READ_ME.txt included in release           #
#                                                                    #
# Make changes as one sees fit but PLEASE document.                  #
# Feel free to distribute to anyone and everyone you know            #
# but please maintain this document within the distribution.         #
######################################################################

def mp3_tags( info ):
#+
# Name:
#   flac_tags
# Purpose:
#   A function to parse apart the information from the iTunes XML file into
#   a list that can be append to the ffmpeg command
# Inputs:
#   info : A dictionary containing all information about a given track as
#           read in from the iTunes XML file.
# Outputs:
#   Returns a list that can be appended on the list for the ffmpeg command.
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 24 May 2016
#-
	import urllib2;
	meta = [];                                                                    # Initialize list
	if ('Name' in info): 
		meta.extend(['-metadata', 'title='        + info['Name'].encode('utf-8')]);         # Append the track name to the command
	if ('Artist' in info):  
		meta.extend(['-metadata', 'artist='       + info['Artist'].encode('utf-8')]);       # Add the artist to the command
	if ('Album Artist' in info):
		meta.extend(['-metadata', 'album_artist=' + info['Album Artist'].encode('utf-8')]); # Add the album artist to the command
	if ('Album' in info):
		meta.extend(['-metadata', 'album='        + info['Album'].encode('utf-8')]);        # Add the album to the command
	if ('Composer' in info):
		meta.extend(['-metadata', 'composer='     + info['Composer'].encode('utf-8')]);     # Add the composer to the command     
	if ('Genre' in info):
		meta.extend(['-metadata', 'genre='        + info['Genre'].encode('utf-8')]);        # Add the genre to the command
	if ('Year' in info):
		meta.extend(['-metadata', 'year='         + str(info['Year'])]);            # Add the year to the command
	if ('Disk Number' in info):
		tmp = str(info['Disk Number']).encode('utf-8');                             # Add the disk number to the command
		if ('Disk Count' in info):
			tmp = tmp + '/' + str(info['Disk Count']).encode('utf-8');                # Add the number of disks to the command
		meta.extend(['-metadata', 'disk='+tmp] );
	if ('Track Number' in info):
		tmp = str(info['Track Number']).encode('utf-8');                            # Add the track number to the command
		if ('Track Count' in info):
			tmp = tmp + '/' + str(info['Track Count']).encode('utf-8');               # Add the number of tracks to the command
		meta.extend(['-metadata', 'track='+tmp] );
	return meta;

def flac_tags( info ):
#+
# Name:
#   flac_tags
# Purpose:
#   A function to parse apart the information from the iTunes XML file into
#   a dictionary that can be used by the flac_tagger function. This is just
#   an interface between iTunes XML Library tagging convention and the inputs
#   for the flac_tagger function
# Inputs:
#   info : A dictionary containing all information about a given track as
#           read in from the iTunes XML file.
# Outputs:
#   Returns a dictionary that can be fed into the key_dict keyword of the 
#   flac_tagger function
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 24 May 2016
#-
	import urllib2;
	meta = {};                                                                    # Initialize dictionary
	if ('Name' in info): meta['title']  = info['Name'].encode('utf-8');                                      # Append the track name to the dictionary
	if ('Artist' in info): 
		meta['artist'] = info['Artist'].encode('utf-8');                                    # Add the artist to the dictionary
	if ('Album Artist' in info): 
		meta['albumartist'] = info['Album Artist'].encode('utf-8');                         # Add the album artist to the dictionary
	if ('Album' in info):
		meta['album'] = info['Album'].encode('utf-8');                                      # Add the album to the dictionary
	if ('Composer' in info):
		meta['composer'] = info['Composer'].encode('utf-8');                                # Add the composer to the command     
	if ('Genre' in info):
		meta['genre'] = info['Genre'].encode('utf-8');                                      # Add the genre to the dictionary
	if ('Year' in info):
		meta['year'] = str(info['Year']);                                           # Add the year to the dictionary
	if ('Disk Number' in info):
		meta['disknumber'] = str(info['Disk Number']).encode('utf-8');              # Add the disk number to the dictionary
	if ('Disk Count' in info):
		meta['disktotal'] = str(info['Disk Count']).encode('utf-8'); 
	if ('Track Number' in info):
		meta['tracknumber'] = str(info['Track Number']).encode('utf-8');            # Add the track number to the dictionary
	if ('Track Count' in info):
		meta['tracktotal'] = str(info['Track Count']).encode('utf-8')
	return meta;

def iTunes_music_converter(dest_dir=None, track_id=None, bit_rate=None, codec=None, verbose=False):
#+
# Name:
#   iTunes_music_converter
# Purpose:
#   A function to convert music files in an iTunes library to a given format.
#   the two currently supported formats are MP3 and FLAC.
# Inputs:
#   None.
# Outputs:
#   Converted audio files.
# Keywords:
#   dest_dir : The top level directory to save files in. Converted files will
#               be placed in Artist/Album/ directories within this directory.
#               DEFAULT is to place music in iTunes_Converted directory in
#               the users home music folder.
#   track_id : String of iTunes track ID(s), separated by spaces, for songs to
#               convert. DEFAULT is to convert entire library.
#   bit_rate : Set the bit rate for conversion. This only applies when
#               converting to MP3. MUST include 'k' in bit rate, i.e., 192k.
#               DEFAULT is 320k.
#   codce    : The codec to use for encoding. The two supported options are
#               MP3 and FLAC. DEFAULT is MP3.
#   verbose  : Increase the verbosity
# Author and History:
#   Kyle R. Wodzicki     Created 24 May 2016
#-
	import os, time, sys;
	from plistlib      import readPlist;	                                        # Import plistRead
	from urllib2       import unquote as unquote;                                 # Import unquote from urllib2
	from to_unicode    import to_unicode;	                                        # Import to_unicode function for consistency when working with strings
	from subprocess    import call, check_output;	                                # Import function to call command line program
	from flac_tags     import flac_tagger;	                                      # Import tagger for flac files
	from get_album_art import get_album_art;	                                    # Import get_album_art function
	home_dir = os.getenv("HOME");                                                 # Set path to users home directory
	if (verbose is True): Print = sys.stdout.write;                               # Define a print command
	
	# Set up some defaults if nothing was input!
	if (dest_dir is None):
		dest_dir = home_dir+"/Music/iTunes_Converted/";                             # Set the default save location
		print 'No directory set...putting converted files in:';                     # Print message so that user knows what is going on
		print '    ', dest_dir;
	elif (dest_dir[-1] != '/'):
		dest_dir = dest_dir + '/';                                                  # Append forward slash to the end of the directory if one is not there
	if (bit_rate is None): bit_rate = '320k';                                     # Set the default bit rate
	if (codec    is None): codec    = 'mp3';                                      # Set the default codec to mp3
	codec = codec.lower();                                                        # ensure that the codec is lower case
	
	# Check for local ffmpeg command. Use it if it exists
	with open(os.devnull, 'w') as devnull:
		return_code = call(['which', 'ffmpeg'],stdout=devnull);                     # Attempt to locate ffmpeg on user machine. This is done because it is likely more up-to-date than the bundled ffmpeg
	if (return_code == 0):
		ffmpeg = check_output(['which', 'ffmpeg']).strip('\n');                     # IF found, use it
	else:
		ffmpeg = os.path.dirname( os.path.realpath(__file__) ) + '/ffmpeg';         # ELSE, use the one bundled with the distro	
		if not os.path.isfile(ffmpeg):
			print 'ffmpeg command NOT found! Please install before running!';         # Print a message
			return 1;                                                                 # Return 1
		
	prefix       = 'file://';                                                     # Set the odd prefix used in file locations in the iTunes XML file
	itunes_xml   = home_dir+"/Music/iTunes/iTunes Music Library.xml";             # Set the path to the iTunes XML file; assumed to be in users Music/iTunes directory
	all_info     = to_unicode( readPlist(itunes_xml) );                           # Get the top of the XML tree as unicode text
	music_folder = all_info['Music Folder'];                                      # Get the path to the iTunes music folder
	
	all_ids  = [int(i) for i in all_info['Tracks'].keys() if 'audio file' in all_info['Tracks'][i]['Kind']]; # Get the track_id of every track in the iTunes XML library as an integer
	if (track_id is None):
		track_id = [str(i) for i in all_ids];                                       # If the track_id variable is NOT set, convert all tracks in iTunes library
	else:
		track_id = [i for i in track_id.split() if int(i) in all_ids];              # Parse track IDs input into function checking that they are in the all_ids list
	if (len(track_id) == 0): return 1;                                            # If track_id has zero length, then nothing to convert, return 1
	cnt, nTrack = 0, len(track_id);                                               # Initialize a counter to 0 and get the number of track IDs in the list
	for track in track_id:
		cnt+=1;                                                                     # Increment the track counter
		info = all_info['Tracks'][track];                                           # Get the information about the track in unicode format
		for key in info: 
			if (key != 'Location'): info[key] = to_unicode(info[key]);                # Convert all info to unicode. This is done now due to issues with converting the file location to unicode and escaping the HTML
		if (verbose is True):
			tmp = "";
			if ('Artist'       in info): tmp+= info['Artist']+'/'
			if ('Album'        in info): tmp+= info['Album'] +'/'
			if ('Track Number' in info): tmp+= '{:02} '.format(info['Track Number']);
			if ('Name'         in info): tmp+= info['Name']
			Print(u'{:63.61}#{:07}/{:07}\n'.format(tmp,cnt,nTrack));                  # If verbose is set, build an Artist/Album/Track path
		if (info['Track Type'].upper() == 'REMOTE'):
			if (verbose is True): print '    Remote file (i.e., iCloud)... Skipping!';# Print it is being skipped
			time.sleep(0.5);                                                          # Sleep for 1/2 second
			continue;                                                                 # Skip to next iteration
		source      = unquote(info['Location']);                                    # Get the source of the track escaping HTML. The returned string is utf-8 encoded
		destination = source.replace(music_folder, dest_dir);                       # Set the destination source
		source      = source.replace(prefix, '');                                   # Replace the weird source prefix on the file
		cmd = [ffmpeg, '-y', '-loglevel', '0', '-threads', '1', '-i', source];      # Set up the command to run with much of output suppressed and running on only one thread
# 			cmd = [ffmpeg, '-y', '-threads', '1', '-i', source];    # Set up the command to run with much of output suppressed and running on only one thread
		
		if (codec == 'mp3') or ('MPEG' in info['Kind']):
			destination = '.'.join(destination.split('.')[:-1])+'.mp3';               # Remove the extension from the file name and add mp3 extension			
		elif (codec == 'flac'):
			destination = '.'.join(destination.split('.')[:-1])+'.flac';              # Remove the extension from the file name and add flac extension
		else:
			print '    Invalid codec type!';                                          # Print an error no matter what
			return 1;                                                                 # Return 1 for a failure
		if os.path.isfile(destination): 
			if (verbose is True): print '    File EXISTS on receiver!';               # Some verbose output
			continue;                                                                 # If the destination file already exists, continue past it
		
		if not os.path.isdir(os.path.dirname(destination)):
			os.makedirs(os.path.dirname(destination));                                # If the destination directory does NOT exist, create it
		if (verbose is True): 
			Print('{:23}'.format('    Fetching artwork...'));                         # Print info; attempting to get album cover
			sys.stdout.flush();                                                       # Flust data to screen
		cover = os.path.dirname(destination)+'/coverart.jpeg';                      # Set path to cover art file
		if os.path.isfile(cover):
			cover_code = 0 if os.stat(cover).st_size > 0 else 1;                      # Set cover code to zero if cover art file exists
		elif ('Artist' in info) and ('Album' in info):
			artist = info['Artist'];                                                  # Attempt to download album art work for the album IF the 
			album  = info['Album'];
			y = info['Year'] if 'Year' in info else None;                             # Set y variable to year of album release
			t = info['Track Count'] if 'Track Count' in info else None;               # Set t variable to number of tracks on the album
			cover_code = get_album_art(artist,album,cover,year=y,tracks=t);           # Attempt to download the cover art
		else:
			cover_code = 1;                                                           # If art work file does NOT exist and there is NOT enough info to try to download, set cover_code to 1
		#=== Some verbose output
		if (verbose is True):
			if (cover_code == 0): 
				Print('{:.>12}'.format('Success! - '));                                 # If verbose is NOT false and cover art exists/was downloaded print successes
			else:
				Print('{:.>12}'.format('Failed! - '));                                  # If verbose is NOT false and cover art not exists/failed to downloaded print failed
			sys.stdout.flush();                                                       # Flust data to screen

		mpeg_test = True if 'MPEG' in info['Kind'] else False;                      # Test if the file is of MPEG format
		if (codec == 'mp3') or mpeg_test:
			if (cover_code == 0):
				cmd.extend(['-i',cover,'-map','0:0','-map','1:0','-vcodec','copy']);    # If cover art was downloaded/exists, then add info the ffmpeg command
				cmd.extend(['-metadata:s:v', 'title=Cover (front)']);
			if mpeg_test:
				cmd.extend(['-acodec', 'copy'])
			else:
				cmd.extend(['-acodec', 'mp3', '-b:a', bit_rate]);          
			cmd.extend( mp3_tags(info) );                                             # Parse tags from track information and add MP3 tags to command 
		else: 
			cmd.extend(['-acodec', 'flac', '-sample_fmt', 's16']);                    # Set to flac format at 16 bit depth                 
		if (verbose is True): 
			if mpeg_test:
				Print('{:.<16}'.format('Copying file'));                                # If the file is already mp3, just copy
			else:
				Print('{:.<16}'.format('Encoding file'));                               # If the file is NOT already mp3, encode
			sys.stdout.flush();                                                       # Flust data to screen

		cmd.extend(['-map_metadata', '-1']);                                        # Don't let ffmpeg map the metadata; it is set manually
		cmd.append( destination );                                                  # Add the output file path to the command
		t0 = time.time();                                                           # Get time the command was started
		return_code, nTry = 1, 0
		while (return_code != 0) and (nTry < 3):
			return_code = call(cmd);                                                  # Run the command
			nTry+=1;
		
		if (return_code == 0) and (codec == 'flac') and not mpeg_test:
			key_dict = flac_tags(info);                                               # Parse iTunes XML Info to format usable by flac_tagger
			if (cover_code == 0):
				key_dict['picture']     = cover;                                        # If cover art was downloaded, append the file path to the falc_tagger keywords dictionary
				key_dict['picturetype'] = '3';                                          # If cover art was downloaded, append the image type to the falc_tagger keywords dictionary
			return_code = flac_tagger(destination, key_dict=key_dict);                # If return code was 0 and the codec was flac, then run flac tagger to add tags and cover art
		if (return_code != 0):
			if (verbose is True):
				Print('{:.>19}\n'.format('Failed!'));
				sys.stdout.flush();                                                     # Flust data to screen
			else:
				print 'Failed!';
		else:
			if (verbose is True): 
				Print('{:.>13}{:05.1f}{:1}\n'.format('Finised in: ',time.time()-t0,'s'));
				sys.stdout.flush();                                                     # Flust data to screen
################################################################################
# Set up command line arguments for the function
if __name__ == "__main__":
	import argparse;                                                              # Import library for parsing
	parser = argparse.ArgumentParser(description="Convert iTunes Music Library"); # Set the description of the script to be printed in the help doc, i.e., ./script -h
	parser.add_argument("-d", "--dir", metavar='directory',   type=str, \
	  help="Destination. Default is ~/Music/iTunes_Convert.");                    # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-t", "--track", metavar='track',       type=str, \
	  help="iTunes track ID. If NOT set, all songs converted.");                  # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-c", "--codec", metavar='audio codec', type=str, \
	  help="Codec to use: mp3 OR flac. Default is mp3.");                         # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-b", "--bitrate", metavar='bit rate',    type=str, \
	  help="MP3 bit rate. Default is 320k.");                                     # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-v", "--verbose", action='store_true', \
	  help="increase verbosity")
	args = parser.parse_args();                                                   # Parse the args
	return_code = iTunes_music_converter(dest_dir = args.dir, \
	                                     track_id = args.track, \
	                                     bit_rate = args.bitrate, \
	                                     codec    = args.codec, \
	                                     verbose  = args.verbose); # Call the function to write the tags