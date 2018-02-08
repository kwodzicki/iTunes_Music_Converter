#!/usr/bin/env python3
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

import os, shutil, time, sys;
from plistlib   import readPlist;	                                              # Import plistRead
from subprocess import call, check_output;                                      # Import function to call command line program
from threading  import Thread, Lock
from iTunes_Music_Converter.utils.tagMusic      import tagMusic
from iTunes_Music_Converter.utils.get_album_art import get_album_art;	          # Import get_album_art function

from urllib.parse import unquote

class Counter(object):
	'''A cross-thread counter object'''
	def __init__(self, lock):
		self.val = 0
		self.lock = lock
	def increment(self):
		with self.lock:
			self.val += 1
	def value(self):
		with self.lock:
			return self.val
	def incVal(self):
		with self.lock:
			self.val += 1
			return self.val
            
class iTunes_Music_Converter( object ):
	'''
	Name:
		iTunes_Music_Converter
	Purpose:
		A function to convert music files in an iTunes library to a given format.
		the two currently supported formats are MP3 and FLAC.
	Inputs:
		None.
	Outputs:
		Converted audio files.
	Keywords:
		dest_dir : The top level directory to save files in. Converted files will
								be placed in Artist/Album/ directories within this directory.
								DEFAULT is to place music in iTunes_Converted directory in
								the users home music folder.
		track_id : String of iTunes track ID(s), separated by spaces, for songs to
								convert. DEFAULT is to convert entire library.
		bit_rate : Set the bit rate for conversion. This only applies when
								converting to MP3. MUST include 'k' in bit rate, i.e., 192k.
								DEFAULT is 320k.
		codce    : The codec to use for encoding. The two supported options are
								MP3 and FLAC. DEFAULT is MP3.
		verbose  : Increase the verbosity
	Author and History:
		Kyle R. Wodzicki     Created 24 May 2016

			Modified 11 Nov. 2016 By Kyle R. Wodzicki
				Changed when initial timing for each track is set
				Added a total timer for entire process
	'''
	def __init__(self, dest_dir=None, bit_rate=None, codec=None, verbose=False):
		if not self._testFFmpeg():                                                  # Test for FFmpeg command
			print( 'ffmpeg command NOT found! Exiting!' );                            # Print error
			return None;                                                              # Return None
		self.verbose = verbose;                                                     # Set verbose
		self.home_dir = os.path.expanduser("~");                                    # Set path to users home directory
		if (dest_dir is None):                                                      # If destination directory is None
			self.dest_dir = os.path.join(self.home_dir, 'Music', 'iTunes_Converted'); # Set default directory
			print( 'No directory set...putting converted files in:' );                # Print message so that user knows what is going on
			print( '    {}'.format(self.dest_dir) );                                  # Print message
		else:                                                                       # Else, use dest_dir
			self.dest_dir = dest_dir;                                                 # Append forward slash to the end of the directory if one is not there
			if self.verbose:                                                          # If verbose
				print( 'Ouput directory is:' );                                         # Some verbose output
				print( '    {}'.format(self.dest_dir) );                                # Some verbose output

		self.cmdBase  = ['ffmpeg', '-y', '-loglevel', '0', '-i'];                   # Set up base ffmpeg command
		self.cmdOpts  = None;                                                       # Initialize cmdOpts to None
		self._codec   = 'mp3'  if codec    is None else codec.lower();              # Set the audio codec
		self._bitrate = '320k' if bit_rate is None else bit_rate;                   # Set the audio bit rate
		self._setCmdOpts();                                                         # Set up ffmpeg command options

		self.prefix       = 'file://';                                              # Set the odd prefix used in file locations in the iTunes XML file
		self.itunes_plst  = os.path.join(self.home_dir,'Music','iTunes','iTunes Music Library.xml'); # Set the path to the iTunes XML file; assumed to be in users Music/iTunes directory
		self.itunes_data  = readPlist( self.itunes_plst );                          # Get the top of the XML tree as unicode text
		self.music_folder = self.itunes_data['Music Folder'];                       # Get the path to the iTunes music folder
		self.all_tracks   = [];                                                     # Set all tracks to empty list
		for i in self.itunes_data['Tracks']:                                        # Iterate over all tracks
			if 'audio file' in self.itunes_data['Tracks'][i]['Kind']:                 # If a track is an audio file
				self.all_tracks.append( i );                                            # Append the track id to the all_tracks list

		self.cnt      = None;                                                       # Set cnt to None
		self.nTrack   = None;                                                       # Set nTracks to None
		self.nProc    = 2;                                                          # Set number of concurrent processes allowed
		self.process  = [];                                                         # Initialize list of processes
		self.lock     = Lock();                                                     # Initialize a thread lock
	##############################################################################
	def convert(self, track_id = None):
		'''Function that iterates over tracks to convert them.'''
		if (track_id is None):                                                      # If not track list input,
			track_id = [i for i in self.all_tracks];                                  # If the track_id variable is NOT set, convert all tracks in iTunes library
		else:                                                                       # Else, track list was input
			if type(track_id) is not str: track_id = str(track_id);                   # Make sure its a list
			track_id = [i for i in track_id.split() if i in self.all_tracks];         # Parse track IDs input into function checking that they are in the all_ids list
		if (len(track_id) == 0): return 1;                                          # If track_id has zero length, then nothing to convert, return 1
		self.cnt, self.nTrack = Counter(self.lock), len(track_id);                  # Initialize a counter to 0 and get the number of track IDs in the list
		t00 = time.time();                                                          # Get time for start of iteration over tracks
		for track in track_id:                                                      # Iterate over all tracks
			info   = self.itunes_data['Tracks'][track];                               # Get the information about the track
			self._processChecker();                                                   # Block to ensure there aren't too many process
			proc = Thread(target = self._convertThread, args = (info,) );             # Initialize thread
			proc.start();                                                             # Start thread
			self.process.append( proc );                                              # Append thread to process list
		self.cnt    = None;                                                         # Set cnt to None
		self.nTrack = None;                                                         # Set nTrack to None
		for proc in self.process:                                                   # Iterate over all processes
			try:                                                                      # Try to
				proc.join();                                                            # Join the process
			except:                                                                   # On exception
				proc.communicate();                                                     # Communicate with process
			self.process.remove( proc );                                              # Remove it from the list
		if self.verbose:                                                            # If verbose
			print( 'Elapsed: {} {}'.format( round((time.time()-t00)/60),'min' ) );    # Print elapsed time if verbose is true
	##############################################################################
	def _getSrcDest(self, info):
		'''A function to parse/generate source and destination directories.'''
		src  = unquote( info['Location'] );                                         # Get path to source file in unquoted text
		dest = src.replace(self.music_folder, '');                                  # Set destination to the source with the music folder replaced by an empty string
		dest = os.path.join( self.dest_dir, dest );                                 # Prepend the output directory to the destination path
		src  = src.replace(self.prefix, '');                                        # Remove the prefix from the source directory
		if not os.path.isdir(os.path.dirname(dest)):                                # If the destination directory does NOT exist
			os.makedirs(os.path.dirname(dest));                                       # Create it
		return src, dest;                                                           # Return the source and destination directories
	##############################################################################
	def _convertThread(self, info):
		logFmt = self._logFormat( info );                                           # Get log format
		if (info['Track Type'].upper() == 'REMOTE'):                                # If track type is remote
			if self.verbose: print( logFmt.format('Remote file, skipping!') );        # Print it is being skipped
			return;                                                                   # Skip to next iteration
		src, dest = self._getSrcDest( info );                                       # Get source and destination file
		if os.path.isfile(dest):                                                    # If destination file already exists
			if self.verbose: print( logFmt.format('File EXISTS on receiver!') );      # Some verbose output
			return;                                                                   # If the destination file already exists, continue past it
		if self.verbose: print( logFmt.format('Fetching artwork...') );             # Print info; attempting to get album cover
		cover = self._getCover( dest, info, logFmt );                               # Set path to cover art file
		if self.verbose:                                                            # If verbose 
			t0 = time.time();                                                         # Get the start time
		if 'MPEG' in info['Kind']:                                                  # If file is an mp3
			if self.verbose: print( logFmt.format('Copying file') );                  # If the file is already mp3, just copy
			try:                                                                      # Try to
				shutil.copy( src, dest );                                               # Copy the file
				tagMusic( dest, info, artwork = cover );                                # Write metadata to the file
			except:                                                                   # On exception...
				if self.verbose: print( logFmt.format('Failed to copy file!') );        # Log a message
				if os.path.isfile(dest): os.remove(dest);                               # Remove the file if it exists	
		else:                                                                       # Else, it is NOT an mp3
			if self.verbose:	print( logFmt.format('Encoding file') );                # Print message
			dest = '.'.join( dest.split('.')[:-1] ) + '.' + self.codec;               # Ensure destination file has correct extension
			cmd = self.cmdBase + [src] + self.cmdOpts + [dest];                       # Generate command
			return_code, nTry = 1, 0                                                  # Initialize return_code an nTry
			while (return_code != 0) and (nTry < 3):                                  # While return_code is not zero (0) and nTry is less than three (3)
				return_code = call(cmd);                                                # Run the command
				nTry+=1;                                                                # Increment try
			if return_code == 0:                                                      # If the return code is zero (0)
				tagMusic( dest, info, artwork = cover );                                # Write metadata
		if self.verbose:                                                            # If verbose
			tmp = '{:>13}{:05.1f}{:1}'.format('Finised in: ',time.time()-t0,'s');     # Determine run time
			print( logFmt.format( tmp ) );	                                          # Print log info
	##############################################################################
	def _getCover(self, dest, info, logFmt):
		'''
		Wrapper function to parse track information
		a attempt cover art download.
		'''
		cover = os.path.join( os.path.dirname(dest), 'coverart.jpeg' );             # Set path to cover art file
		if os.path.isfile(cover):                                                   # If the cover art file exists
			cover = None if os.stat(cover).st_size > 0 else cover;                    # Set cover code to zero if cover art file exists
		elif ('Artist' in info or 'Album Artist' in info) and ('Album' in info):    # Else, if there is enough information in the info dictionary
			if ('Album Artist' in info):                                              # If the album artist is in the dictionary
				artist = info['Album Artist'];				                                  # Attempt to download album art work for the album IF the 
			elif ('Artist'     in info):                                              # Else, if the artist is in the dictionary
				artist = info['Artist'];                                                # Attempt to download album art work for the album IF the 
			album  = info['Album'];                                                   # Get album info
			y = info['Year'] if 'Year' in info else None;                             # Set y variable to year of album release
			t = info['Track Count'] if 'Track Count' in info else None;               # Set t variable to number of tracks on the album
			status = get_album_art(artist,album,cover,year=y,tracks=t);               # Attempt to download the cover art
			if status != 0: cover = None;                                             # If the status is NOT zero (0), set cover to None
		else:                                                                       # Else, file does NOT exist and not enough information to try to download it
			open(cover, 'a').close();                                                 # Empty file created so do not attempt to download on subsequent runs.
			cover = None;                                                             # If art work file does NOT exist and there is NOT enough info to try to download, set cover_code to 1
		if self.verbose:                                                            # If verbose
			if cover:                                                                 # If cover is not None
				print(logFmt.format('Artwork Success!'));                               # If verbose is NOT false and cover art exists/was downloaded print successes
			else:                                                                     # Else, cover is None
				print(logFmt.format('Artwork Failed!'));                                # If verbose is NOT false and cover art not exists/failed to downloaded print failed
		return cover;                                                               # Return cover
	##############################################################################
	def _logFormat( self, info ):
		'''Set up string format for log messages.'''
		cnt = self.cnt.incVal();                                                    # Get count of the track being processed
		fmt = '{:>6} of {:>6} {:39.38}'
		tmp = "";
		if ('Album Artist' in info): 
			tmp += info['Album Artist']+'/';
		elif ('Artist'     in info): 
			tmp+= info['Artist']+'/';
		if ('Album'        in info): tmp+= info['Album'] +'/';
		if ('Track Number' in info): tmp+= '{:02} '.format(info['Track Number']);
		if ('Name'         in info): tmp+= info['Name'];
		return fmt.format( cnt, self.nTrack, tmp ) + ' - {:21.20}';
	##############################################################################
	def _processChecker(self):
		'''Stop too many processes from running'''
		if len(self.process) >= self.nProc:                                         # If running enough process
			while all( [proc.is_alive() for proc in self.process] ):                  # While all the process are alive
				time.sleep(0.01);                                                       # Sleep for a little
			for proc in self.process:                                                 # One of the process is no longer alive so iterate to find the dead one
				if not proc.is_alive():                                                 # If the process is not alive
					try:                                                                  # Try to...
						proc.join();                                                        # Join the process
					except:                                                               # On exception
						proc.communicate();                                                 # Communicate with process
					self.process.remove( proc );                                          # Remove it from the list
					break;           														                          # Break the for loop
	##############################################################################
	def _setCmdOpts(self):	
		if self.codec == 'mp3':                                                     # If codec is mp3
			self.cmdOpts = ['-acodec', 'mp3', '-b:a', self._bitrate];                 # Set convert options
		else:                                                                       # Else, assume flac
			self.cmdOpts = ['-acodec', 'flac'];                                       # Set convert options
		self.cmdOpts.extend( ['-map_metadata', '-1', '-vn'] );                      # Turn off metadata and video stream copy

	##############################################################################
	# Check for ffmpeg command
	def _testFFmpeg(self):
		'''Test the FFmpeg exists'''
		try:                                                                        # Try to call a command
			ffmpeg = check_output( ['which', 'ffmpeg'] );                             # IF found, use it
		except:                                                                     # On exception
			return False;                                                             # Return False
		return True;                                                                # If made it here, no exception, return True

	##############################################################################
	def __set_codec(self, value = None):
		self._codec = 'mp3' if value is None else value.lower();
		self._setCmdOpts();
	def __get_codec(self):
		return self._codec;
  ##########
	def __set_bitrate(self, value = None):
		self._bitrate = '320k' if value is None else value;
		self._setCmdOpts()
	def __get_bitrate(self):
		return self._bitrate;
  ##########
	codec    = property(__get_codec,   __set_codec);
	bit_rate = property(__get_bitrate, __set_bitrate);