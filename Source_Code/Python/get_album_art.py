#!/usr/bin/env python
# Two functions used to download album artwork
def parse_release( release ):
#+
# Name:
#   parse_release
# Purpose:
#   A function to parse out information of interest from a dictionary containing
#   information about a release.
# Inputs:
#   release : Dictionary containing information about a release grabbed from
#              the MusicBrainz API using the musicbrainzngs python package.
# Outputs:
#   Returns a dictionary with the following information:
#     status, format, number of tracks, date, language.
#   If any of this information was NOT found in the release information, the
#   value in the dictionary is None.
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 24 May 2016
#
#     Modified 12 Nov. 2016 by Kyle R. Wodzicki
#       Added the 'rm_special' function to remove fancy unicode apostrophes.
#     Modified 18 Nov. 2016 by Kyle R. Wodzicki
#       Added removal of ellipsis to 'rm_special' function.
#-
	from to_unicode import to_unicode
	def rm_special(in_var):
		in_var = in_var.replace(u"\u2018", "'").replace(u"\u2019", "'");            # Remove fancy single quotes; replace with standard single quote
		in_var = in_var.replace(u"\u201c",'"').replace(u"\u201d", '"');             # Remove fancy double quotes; replace with standard double quote
		in_var = in_var.replace(u"\u2026",'...');                                   # Remove ellipsis; replace with 3 periods
		in_var = in_var.replace(u"\u2010", '-');                                    # Remove fancy hypen; replace with normal hyphen
		return in_var;                                                              # Return variable

	if ('status'        not in release) or ('release-group' not in release) or \
	   ('artist-credit' not in release) or ('title'         not in release):
		return None;                                                                # These two tags are required at minimum, so if either does NOT exist, return None.
	if ('type' not in release['release-group']):
		return None;                                                                # If there is no release type under the release-group tag, then return None
# 	elif ('ALBUM'  not in release['release-group']['type'].upper()) and \
# 	     ('REMIX'  not in release['release-group']['type'].upper()) and \
# 	     ('SINGLE' not in release['release-group']['type'].upper()) and \
# 	     ('LIVE'   not in release['release-group']['type'].upper()) and \
# 	     (release['release-group']['type'].upper() != 'EP') and \
# 	     (release['release-group']['type'].upper() != 'COMPILATION') and \
# 	     (release['release-group']['type'].upper() != 'SOUNDTRACK'): 
# 		return None;                                                                # If the release is NOT an album, return None
	data = {}
	if ('artist' not in release['artist-credit'][0]):
		return None;
	else:
		tmp = release['artist-credit'][0]['artist']
		if ('name' in tmp):
			data['artist'] = to_unicode(rm_special(tmp['name'])).upper();
		elif ('sort-name' in tmp):
			data['artist'] = to_unicode(rm_special(tmp['sort-name'])).upper();
		else:
			return None;
	data['album']    = to_unicode(rm_special(release['title'])).upper();               # Get album title
	data['status']   = to_unicode(release['status']).upper();                     # Get the status of the release
	data['disambig'] = None
	if ('disambiguation' in release):
# 		if (release['disambiguation'] != ''):
		data['disambig'] = to_unicode(rm_special(release['disambiguation'])).upper();
	if ('medium-list' in release):
		tmp = release['medium-list'][0]
		data['format'] = to_unicode(tmp['format'])      if ('format'      in tmp) else None;
		data['tracks'] = to_unicode(tmp['track-count']) if ('track-count' in tmp) else None;
	else:
		data['format'] = None;
		data['tracks'] = None;
	
	if ('date' in release):
		data['year'] = int(release['date'][:4]);
	elif ('release-event-list' in release):
		tmp = release['release-event-list'][0]
		data['year'] = int(tmp['date'][:4]) if ('date' in tmp) else None;
	else:
		data['year'] = None;
	data['lang'] = None;
	if ('text-representation' in release):
		if ('language' in release['text-representation']):
			data['lang'] = to_unicode(release['text-representation']['language']).upper();
	return data;
	
def get_album_art(artist, album, file, year = None, lang = None, tracks = None, \
                  quality = None, format = None, status = None, verbose = False):
#+
# Name:
#   get_album_art
# Purpose:
#   A function to download album artwork using the musicbrainz api
# Inputs:
#   artist  : The artist of the album
#   album   : Name of the album
#   file    : Full path to where the file will be downloaded
# Outputs:
#   Downloads album artwork
# Keywords:
#   year     : Year album was released
#   tracks   : The number of tracks on the album. Default is None.
#   lang     : The language of the release. Default is english (eng)
#   quality  : Quality of the returned info. Default is high.
#   format   : Format of the release (cd, vinyl, etc.). Default is CD.
#   status   : The type of release. Default is official.
# Author and History:
#   Kyle R. Wodzicki     Created 24 May 2016
#     Adapted from examples int he musicbrainzngs package.
#
#     Modified 12 Nov. 2016 by Kyle R. Wodzicki
#       Changed the data['artist'] == artist.upper() to 
#       data['artist'] in artist.upper(). This should allow a little more 
#       flexibility. One example is the Riding with the King album by B.B. King
#       and Eric Clapton. However, musicbrainz has the artist as just B.B. King.
#       Issues may arise if the name of an artist somehow fits into the name
#       of the artist of interest.
#-
	import sys, os, time;
	import musicbrainzngs as MB;
	from subprocess import call
	from to_unicode import to_unicode
	from flac_tags.extras.getImageInfo import getImageInfo;                       # Import the get image info function
	
	open(file, 'a').close();                                                      # Empty file created so do not attempt to download on subsequent runs. THIS FILE IS OVERWRITTEN IF ARTWORK FOUND!!!!
	
	MB.set_useragent("iTunes_Convert_KRW", "1.0");                                # Set the user of the MusicBrainz API
	MB.set_rate_limit(limit_or_interval=False);                                   # Set the limit interval to false, i.e., no limit
	
	artist, album = to_unicode(artist), to_unicode(album)
	if (quality is None):
		quality = to_unicode('high');
	if (status is None):
		status = to_unicode('official');
	if (lang is None):
		lang = to_unicode('eng');
	if (format is None):
		format = to_unicode('CD');
	attempt = 0;                                                                  # Set attempt number for album art
	while attempt < 3:
		try:
			result = MB.search_releases(artist=artist, release=album, quality=quality);# Attempt to get release information
		except:
			attempt+=1;                                                               # Increment the attempt counter by one
			time.sleep(10);                                                           # Sleep 10 seconds
		else:
			break;
	if attempt == 3: return 2;                                                    # If MusicBrainz search fails three times, return 2
	result = to_unicode(result)
# 	importance = ['format', 'year', 'tracks', 'lang'];                            # This sets the importance of given inputs. If no artwork is found, then these are set to None one by one in an attempt to find artwork
	importance = ['format', 'year', 'tracks', 'lang', 'status'];                  # This sets the importance of given inputs. If no artwork is found, then these are set to None one by one in an attempt to find artwork
	release_id = None;                                                            # Set release_id to None
	for i in range(-1,len(importance)):
		if (i >= 0): exec(importance[i] + " = None");                               # Set a given 'importance' variable to None.
		for release in result['release-list']:
# 			print release;
			data = parse_release( release );
			if data is None: continue;                                                # If vital information not present in release, the skip
			if (verbose is True): print data;                                         # Print data IF verbose
# 			print data['artist'], artist.upper();
# 			print data['album'], album.upper();
# 			print '';
# 			if (data['status'] == status.upper()) and \
# 			   (data['artist'] in artist.upper() or artist.upper() in data['artist']):
# 				print data['album'];
			if (data['artist'] in artist.upper() or artist.upper() in data['artist']):
				if (data['album'] not in album.upper() and \
				    album.upper() not in data['album']): continue;
				if (status is not None):
					if (data['status'] != status.upper()): continue;                      # If status exists and does NOT match the default status, skip
				if (data['disambig'] is not None):
					if (data['disambig'] not in album.upper()): continue;
				if (format is not None):
					if (to_unicode(format).upper() != data['format']): continue;          # If user input format for the album and that does not match the number on the release, skip
				if (tracks is not None):
					if (int(tracks) != data['tracks']): continue;                         # If user input number of tracks and that does not match the number on the release, skip
				if (year is not None):
					if (int(year) != data['year']): continue;                             # If user input year and that does not match the year of the release, skip
				if (lang is not None):
					if (to_unicode(lang).upper() != data['lang']): continue;              # If user input year and that does not match the year of the release, skip
				release_id   = release['id'];                                           # Get the MusicBrainz ID for the album
				attempt = 0;                                                            # Set attempt number for album art
				while attempt < 3:
					try:
						release_info = MB.get_release_by_id( release_id )['release'];       # Get information about the relase
					except:
						attempt+=1;                                                         # Increment the attempt counter by one
						time.sleep(10);                                                     # Sleep 10 seconds
					else:
						break;
				if attempt == 3: return 3;                                              # If MusicBrainz search fails three times, return 2
				release_info = MB.get_release_by_id( release_id )['release'];           # Get information about the relase
				if (verbose is True): print release_info;
				if (release_info['cover-art-archive']['front'] == 'true'):
					attempt = 0;                                                          # Set attempt number for album art
					while attempt < 3:
						try:
							image = MB.caa.get_image(release_id, 'front');                    # Download the image
						except:
							attempt+=1;                                                       # Increment the attempt counter by one
							time.sleep(10);                                                   # Sleep 10 seconds
						else:
							break;
					if attempt == 3: return 4;                                            # If MusicBrainz search fails three times, return 2
					info  = getImageInfo(data = image);                                   # Get information about the image
					tmp_file = '.'.join(file.split('.')[:-1])+'tmp.'+info['ext'];         # Set up a file name to save to if image is NOT jpeg
					f = open(tmp_file, 'w');                                              # Open the file for writing
					f.write( image );                                                     # Write the data to the file
					f.close();                                                            # Close the file
					cmd = ['sips','-s','format','jpeg','-Z','500',tmp_file,'--out',file]; # Set the command to run; output file will be jpeg format and how height OR width no greater that 500 pixels
					with open(os.devnull, 'w') as devnull:
						return_code = call(cmd, stdout=devnull, stderr=devnull);            # Run the sips command and pipe output to /dev/null
					os.remove(tmp_file);                                                  # Delete the file that is NOT jpeg
					return 0;
#=== OLD CODE FOR SAVING/CONVERTING THE IMAGE. NEW CODE KEEPS FILES SMALL!!!
# 					if ('jpeg' in info['type']):
# 						f = open(file, 'w');                                                # IF there is front cover art for the album, open local file
# 						f.write( image );                                                   # Write the image to the file
# 						f.close();                                                          # Close the local file
# 					else:
# 						tmp_file = '.'.join(file.split('.')[:-1])+'.'+info['ext'];          # Set up a file name to save to if image is NOT jpeg
# 						f = open(tmp_file, 'w');                                            # Open the file for writing
# 						f.write( image );                                                   # Write the data to the file
# 						f.close();                                                          # Close the file
# 						cmd = ['sips','-s','format','jpeg',tmp_file,'--out',file];          # Set the command to run; output file will be jpeg format and how height/width no greater that 350 pixels
# 						with open(os.devnull, 'w') as devnull:
# 							return_code = call(cmd ,stdout=devnull);                          # Run the sips command and pipe output to /dev/null
# 						os.remove(tmp_file);                                                # Delete the file that is NOT jpeg
# 					return 0;                                                             # Return 0 when downloaded
	return 1;                                                                     # Return 1 if no match found 

# Set up command line arguments for the function
if __name__ == "__main__":
	import argparse;                                                              # Import library for parsing
	parser = argparse.ArgumentParser(description="Album Cover Art Grabber")       ; # Set the description of the script to be printed in the help doc, i.e., ./script -h
	parser.add_argument("-a", "--artist",  metavar='artist name',       type=str, \
	  help="Artist that create the album. Required input!");                      # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-A", "--album",   metavar='album name',        type=str, \
	  help="Name of the album. Required input!");                                 # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-y", "--year",    metavar='year of release',   type=str, \
	  help="Year the album was released. Optional input.");                       # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-t", "--tracks",  metavar='number of tracks',  type=str, \
	  help="The number of tracks on the album. Optional input.");                 # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-q", "--quality", metavar='quality of matches', type=str, \
	  help="Quality of matches from MusicBrainz. Default is high.");              # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-f", "--format",  metavar='vinyl,cd,etc.',     type=str, \
	  help="Type of medium the album was released on. Default is CD.");           # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-s", "--status",  metavar='release status',    type=str, \
	  help="Status of the release. Default is offical.");                         # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("-v", "--verbose", action='store_true', \
	  help="Increase verbosity");                                                 # Set an option of inputing of a file path. No dictionary can be passed via the command line
	parser.add_argument("file",            metavar='file',              type=str, \
	  help="Path to download the file to. Default is current directory.");        # Set an option of inputing of a file path. No dictionary can be passed via the command line

	args = parser.parse_args();                                                   # Parse the args
	if (args.artist is None) or (args.album is None) or (args.year is None):
		print 'Must input artist, album, and year!'
		quit();
	return_code = get_album_art(args.artist, args.album, args.file, \
	                            year    = args.year, \
	                            tracks  = args.tracks, \
                              quality = args.quality, \
                              format  = args.format, \
                              status  = args.status, \
                              verbose = args.verbose); # Call the function to write the tags
	if (return_code == 4):
		print 'Error getting cover art!';
	elif (return_code == 3):
		print 'Error getting release information!';
	elif (return_code == 2):
		print 'Error searching for release information!';
	elif (return_code == 1):
		print 'Failed to find artwork matching request!';
	else:
		if args.verbose is True:
			print 'Download successful!';