#!/usr/bin/env python
######################################################################
# A python program to get audio track information from an iTunes     #
# XML library file and copy files that are already MP3 format to     #
# a destination directory or convert files that are not MP3 to MP3   #
# and placing them in the destination directory. If the file already #
# exists on the receiver, the file is skipped.                       #
#                                                                    #
# This can be run on its on, with prompts to set destination         #
# directory and bit rate for MP3, however, in this mode, all         #
# files in the iTunes library will be processed.                     #
#                                                                    #
# A better way to execute this program is by using the AppleScript   #
# application that can be found in this release.                     #
#                                                                    #
# This program maintains the Artist/Album file structure present     #
# in the iTunes Media folder.                                        #
#                                                                    #
# What it does:                                                      #
# IF it does:                                                        #
#   skip it,                                                         #
# IF it does NOT:                                                    #
#   Check IF MP3                                                     #
#   IF is MP3:                                                       #
#     copy the file to correct folder structure                      #
#   IF NOT MP3:                                                      #
#     Convert it temp directory then move to                         #
#     correct folder on receiver.                                    #
#                                                                    #
# Created on 20 Aug. 2014 by Kyle R. Wodzicki                        #
#                                                                    #
# All rights reserved.                                               #
#                                                                    #
# For more information see READ_ME.txt included in release           #
#                                                                    #
# Make changes as one sees fit but PLEASE document.                  #
# Feel free to distribute to anyone and everyone you know            #
# but please maintain this document within the distribution.         #
######################################################################

# Function to append metadata to the ffmpeg command.
def add_data(var, data):
	var.extend( ['-metadata', data] );

def iTunes_music_converter(dest_dir=None, track_id=None, bit_rate=None, codec=None):
	import os, plistlib, urllib2;
	from to_unicode import to_unicode;
	from copy_file  import copy_file;
	from subprocess import call;	                                                  # Import function to call command line program
	from subprocess import check_output;	                                          # Import function to call command line program

	to_utf = lambda input: urllib2.unquote(input).encode('utf-8');
	home_dir = os.getenv("HOME");                                                 # Set path to the home directory
	
	# Set up some defaults if nothing was input!
	if (dest_dir is None):
		dest_dir = home_dir+"/Music/iTunes_Converted/";                             # Set the default save location
		print 'No directory set...putting converted files in:';
		print '  ', dest_dir;
	if (bit_rate is None):
		bit_rate = '320k';                                                          # Set the default bit rate
	if (codec is None):
		codec = 'mp3';                                                              # Set the default codec to mp3
	codec = codec.lower();                                                        # ensure that the codec is lower case
	
	# Check for local ffmpeg command. Use it if it exists
	with open(os.devnull, 'w') as devnull:
		return_code = call(['which', 'ffmpeg'],stdout=devnull);                     # Attempt to locate ffmpeg on user machine
	if (return_code == 0):
		ffmpeg = check_output(['which', 'ffmpeg']).strip('\n');                     # IF found, use it
	else:
		ffmpeg = os.path.dirname( os.path.realpath(__file__) ) + '/ffmpeg';         # ELSE, use the one bundled with the distro	
	prefix       = 'file://';                                                     # Set the odd prefix in the file location
	itunes_xml   = home_dir+"/Music/iTunes/iTunes Music Library.xml";             # Set the path to the iTunes XML file
	all_info     = to_unicode(plistlib.readPlist(itunes_xml));                    # Get the top of the XML tree as unicode text
	music_folder = all_info['Music Folder'];                                      # Get the path to the iTunes music folder
	
	if (track_id is None):
		track_id = all_info['Tracks'].keys();                                       # Get all track info
	else:
		track_id = [int(i) for i in track_id.split()];                              # Convert track IDs to integers
		all_ids  = [int(i) for i in all_info['Tracks'].keys()];                     # Filter the tracks from the XML file by the list input
		for i in track_id:
			if (i not in all_ids):
				track_id.remove(i);
	if (len(track_id) == 0):
		return 1;

	for track in track_id:
		if ('audio file' in all_info['Tracks'][str(track)]['Kind']):
			info        = to_unicode(all_info['Tracks'][str(track)]);                 # Get the information about the track in unicode format
			source      = to_utf(info['Location']);                                   # Get the source of the track escaping HTML
			destination = source.replace(music_folder, dest_dir);                     # Set the destination source and encode to uft8
			source      = source.replace(prefix, '');                                 # Replace the weird source prefix on the file and encode to utf8
			if ('MPEG' in info['Kind']):
				return_code = copy_file(source, destination);
			else:
				cmd = [ffmpeg, '-loglevel', '0', '-stats', '-i', source];               # Set up the command to run
				cmd.extend(['-map_metadata', '-1']);                                    # Don't let ffmpeg map the metadata; it is set manually
				if (codec == 'mp3'):
					destination = '.'.join(destination.split('.')[:-1])+'.mp3';           # Set the destination path to the file with a .mp3 extension
					cmd.extend(['-f', 'mp3', '-b:a', bit_rate]);                          # Set to mp3 format at given bit rate              
				elif (codec == 'flac'):
					destination = '.'.join(destination.split('.')[:-1])+'.flac';
					cmd.extend(['-f', 'flac', '-sample_fmt', 's16']);                     # Set to flac format at 16 bit depth                 
				
				if os.path.isfile(destination):
					continue;                                                             # IF an MP3 of the file already exists, then skip it
				keys = info.keys();                                                     # Get the keys for the dictionary of track information
				if ('Name' in keys):
					add_data( cmd, 'title='        + to_utf(info['Name'])         );      # Append the track name to the command
				if ('Artist' in keys):
					add_data( cmd, 'artist='       + to_utf(info['Artist'])       );      # Add the artist to the command
				if ('Album Artist' in keys):
					add_data( cmd, 'album_artist=' + to_utf(info['Album Artist']) );      # Add the album artist to the command
				if ('Genre' in keys):
					add_data( cmd, 'genre='        + to_utf(info['Genre'])        );      # Add the genre to the command
				if ('Year' in keys):
					add_data( cmd, 'year='         + str(info['Year'])            );      # Add the year to the command
				if ('Disk Number' in keys):
					tmp = str(info['Disk Number']).encode('utf-8');                       # Add the disk number to the command
					if ('Disk Count' in keys):
						tmp = tmp + '/' + str(info['Disk Count']).encode('utf-8');          # Add the number of disks to the command
					add_data( cmd, 'disk='+tmp );
				if ('Track Number' in keys):
					tmp = str(info['Track Number']).encode('utf-8');                      # Add the track number to the command
					if ('Track Count' in keys):
						tmp = tmp + '/' + str(info['Track Count']).encode('utf-8');         # Add the number of tracks to the command
					add_data( cmd, 'track='+tmp );
				cmd.append( destination );                                              # Add the output file path to the command
				if not os.path.isdir(os.path.dirname(destination)):
					os.makedirs(os.path.dirname(destination));                            # If the destination directory does NOT exist, create it
				return_code = call(cmd);                                                # Run the command
				if (return_code != 0):
					return 1;
	return 0;

# Set up command line arguments for the function
if __name__ == "__main__":
	import argparse;                                                              # Import library for parsing
	parser = argparse.ArgumentParser(description="Convert iTunes Music Library"); # Set the description of the script to be printed in the help doc, i.e., ./script -h
	parser.add_argument("-d", metavar='directory',   type=str, \
	  help="Destination. Default is ~/Music/iTunes_Convert.");                    # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-t", metavar='track',       type=str, \
	  help="iTunes track ID. If NOT set, all songs converted.");                  # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-c", metavar='audio codec', type=str, \
	  help="Codec to use: mp3 OR flac. Default is mp3.");                         # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-b", metavar='bit rate',    type=str, \
	  help="MP3 bit rate. Default is 320k.");                                     # Set an option of inputing of a file path. No dictionary can be passed via the command line
	args = parser.parse_args();                                                   # Parse the args
	return_code = iTunes_music_converter(dest_dir = args.d, \
	                                     track_id = args.t, \
	                                     bit_rate = args.b, \
	                                     codec    = args.c); # Call the function to write the tags
	if (return_code != 0):
		print 'Conversion Failed!';
	else:
		print 'Conversion Success!';