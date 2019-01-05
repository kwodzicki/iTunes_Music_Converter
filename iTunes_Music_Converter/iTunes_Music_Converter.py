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
from plistlib   import readPlist;                                               # Import plistRead
from subprocess import check_output, Popen, PIPE, STDOUT, DEVNULL;
from threading  import Thread, Lock;
from urllib.parse import unquote;
from tkinter import Tk;

# from iTunes_Music_Converter.utils.tagMusic      import tagMusic
# from iTunes_Music_Converter.utils.get_album_art import get_album_art;           # Import get_album_art function
from .utils import tagMusic, get_album_art, getLibraryXML, data;


# from iTunes_Music_Converter.utils import data;
from iTunes_Music_Converter.progressFrame import progressFrame;

class Counter(object):
  '''A cross-thread counter object'''
  def __init__(self):
    self.__val  = 0;
    self.__lock = Lock();
  def increment(self):
    with self.__lock:
      self.__val += 1;
  def value(self):
    with self.__lock:
      return self.__val;
  def incVal(self):
    with self.__lock:
      self.__val += 1;
      return self.__val;
  def reset(self):
    with self.__lock:
      self.__val = 0;

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
    verbose  : Increase the verbosity; display progress in command line
    gui      : Display GUI of progress
  Author and History:
    Kyle R. Wodzicki     Created 24 May 2016

      Modified 11 Nov. 2016 By Kyle R. Wodzicki
        Changed when initial timing for each track is set
        Added a total timer for entire process
  '''
  def __init__(self, dest_dir=None, bit_rate=None, codec=None, verbose=False, gui=False):
    if not self._testFFmpeg():                                                  # Test for FFmpeg command     
      return None;                                                              # Return None
    self.verbose = verbose;                                                     # Set verbose
    self.gui     = gui;                                                         # Set gui, not used yet

    ncpu = os.cpu_count();                                                      # Number of CPUs available
    if ncpu <= 2:                                                               # If number of CPUs <=2
      self.nProc = ncpu;                                                        # Set number of concurrent processes allowed to number of CPUs
    else:                                                                       # Else, number of CPUs > 2
      self.nProc = round(ncpu / 2);                                             # Set to half the number of CPUs rounded up

    if (dest_dir is None):                                                      # If destination directory is None
      self.dest_dir = os.path.join(data.home_dir, 'Music', 'iTunes_Converted'); # Set default directory
    else:                                                                       # Else, use dest_dir
      self.dest_dir = dest_dir;                                                 # Append forward slash to the end of the directory if one is not there

    if self.gui:                                                                # If verbose is set
      self.root     = Tk();                                                     # Initialize a root window
      self.progress = progressFrame( self.root, self.nProc, self.dest_dir );    # Set up progress window
      self.root.winfo_toplevel().title('convert_music');                        # Set the window title
    else:
      self.root     = None;
      self.progress = None;

    self.cmdBase  = ['ffmpeg', '-y', '-hide_banner', '-loglevel', '32', '-i'];  # Set up base ffmpeg command
    self.cmdOpts  = None;                                                       # Initialize cmdOpts to None
    self._codec   = 'mp3'  if codec    is None else codec.lower();              # Set the audio codec
    self._bitrate = '320k' if bit_rate is None else bit_rate;                   # Set the audio bit rate
    self._setCmdOpts();                                                         # Set up ffmpeg command options

    self.itunes_plst  = getLibraryXML();                                        # Set the path to the iTunes XML file; assumed to be in users Music/iTunes directory
    self.itunes_data  = readPlist( self.itunes_plst );                          # Get the top of the XML tree as unicode text
    self.music_folder = self.itunes_data['Music Folder'];                       # Get the path to the iTunes music folder
    self.all_tracks   = [];                                                     # Set all tracks to empty list
    for i in self.itunes_data['Tracks']:                                        # Iterate over all tracks
      if 'audio file' in self.itunes_data['Tracks'][i]['Kind']:                 # If a track is an audio file
        self.all_tracks.append( i );                                            # Append the track id to the all_tracks list

      
    self.cnt       = Counter();                                                 # Set cnt to Counter class
    self.nTrack    = None;                                                      # Set nTracks to None
    self.process   = [];                                                        # Initialize list of processes
    self.__Lock    = Lock();                                                    # Lock for downloading cover art
  ##############################################################################
  def convert(self, track_id = None):
    if (track_id is None):                                                      # If not track list input,
      track_id = [i for i in self.all_tracks];                                  # If the track_id variable is NOT set, convert all tracks in iTunes library
    else:                                                                       # Else, track list was input
      if type(track_id) is not str: track_id = str(track_id);                   # Make sure its a list
      track_id = [i for i in track_id.split() if i in self.all_tracks];         # Parse track IDs input into function checking that they are in the all_ids list
    self.nTrack = len(track_id);                                                # Number of tracks to convert
    if self.nTrack == 0:                                                        # If number of tracks is zero
      if self.gui: self.root.destroy();                                         # If verbose is set, destroy the root tkinter object
      return 1;                                                                 # return 1
    self.cnt.reset();                                                           # Reset the count for cnt attribute
    if self.gui:
      self.progress.nTracks( self.nTrack );                                     # Set number of tracks to convert in the progress bar
    
    thread = Thread(target = self._convert, args = (track_id,));                # Initialize thread to run _convert method
    thread.start();                                                             # Start the thread

    if self.gui:                                                                # If verbose is set
      self.root.mainloop();                                                     # Start the tkinter main loop
    else:                                                                       # Else
      thread.join();                                                            # Just join the thread and wait for it to finish

  ##############################################################################
  def _convert(self, track_id):
    '''Function that iterates over tracks to convert them.'''
    t00 = time.time();                                                          # Get time for start of iteration over tracks
    for track in track_id:                                                      # Iterate over all tracks
      info = self.itunes_data['Tracks'][track];                                 # Get the information about the track
      proc = self._processChecker();                                            # Block to ensure there aren't too many process
      proc = Thread(target = self._convertThread, args = (info,) );             # Initialize thread
      proc.start();                                                             # Start thread
      self.process.append( proc );                                              # Append thread to process list
    while len(self.process) > 0:                                                # While there are processes left int he process attribute
      proc = self.process.pop();                                                # Pop processes off the process attribute list
      try:                                                                      # Try to
        proc.join();                                                            # Join the process
      except:                                                                   # On exception
        proc.communicate();                                                     # Communicate with process
  ##############################################################################
  def _convertThread(self, info):
    logFmt = self._logFormat(info);                                             # Get logging format
    if (info['Track Type'].upper() == 'REMOTE'):                                # If track type is remote
      return;                                                                   # Skip to next iteration
    src, dest = self._getSrcDest( info );                                       # Get source and destination file
    file = unquote(info['Location']).replace( unquote(self.music_folder), '' );
    if self.gui:
      bar    = self.progress.getBar( info );
    if self.verbose:
      logFmt = self._logFormat( info );                                         # Get log format
    if os.path.isfile(dest):                                                    # If destination file already exists
      if self.gui: 
        bar.updateStatus('File EXISTS on receiver!', finish = True);            # Print it is being skipped
        self.progress.freeBar(bar);
      if self.verbose: 
        print( log.Fmt.format('File EXISTS on receiver!') );                    # Print it is being skipped
      return;                                                                   # If the destination file already exists, continue past it
    if self.gui: 
      bar.updateStatus('Fetching artwork...');                                  # Print it is being skipped
    cover = self._getCover( dest, info, logFmt );                               # Set path to cover art file
    if self.gui:                                                                # If gui
      bar.updateStatus('Artwork Downloaded', prog = True);                      # Print it is being skipped
      t0 = time.time();                                                         # Get the start time

    status = 1;
    if 'MPEG' in info['Kind']:                                                  # If file is an mp3
      if self.gui: 
        bar.updateStatus('Copying file');
      try:                                                                      # Try to
        shutil.copy( src, dest );                                               # Copy the file
      except:                                                                   # On exception...
        if self.gui: 
          bar.updateStatus('Failed to copy file!');
          self.progress.freeBar(bar);
        if os.path.isfile(dest): os.remove(dest);                               # Remove the file if it exists  
      else:
        bar.updateStatus('Copy success!', prog = True);
        status = 0;
    else:                                                                       # Else, it is NOT an mp3
      if self.gui:
        bar.updateStatus('Encoding file!');
      cmd = self.cmdBase + [src] + self.cmdOpts + [dest];                       # Generate command
      with open('/Users/kyle/test.txt', 'w') as fid: fid.write(cmd)
      proc = Popen(cmd, stdout = PIPE, stderr = STDOUT, stdin = DEVNULL);
      if self.gui:
        bar.conversion(proc);
      proc.communicate();
      status = proc.returncode
    if status == 0:                                                  # If the return code is zero (0)
      if self.gui:
        bar.updateStatus('Writing metadata');
      tagMusic( dest, info, artwork = cover );                                  # Write metadata
      if self.gui:
        bar.finish();

    if self.gui:                                                                # If gui
      self.progress.freeBar(bar);
  ##############################################################################
  def _getSrcDest(self, info):
    '''A function to parse/generate source and destination directories.'''
    src  = unquote( info['Location'] );                                         # Get path to source file in unquoted text
    dest = src.replace(self.music_folder, '');                                  # Set destination to the source with the music folder replaced by an empty string
    dest = os.path.join( self.dest_dir, dest );                                 # Prepend the output directory to the destination path
    if 'MPEG' not in info['Kind']:                                              # If file is NOT an mp3
      dest = '.'.join( dest.split('.')[:-1] ) + '.' + self.codec;               # Ensure destination file has correct extension
    src  = src.replace(data.prefix, '');                                        # Remove the prefix from the source directory
    with self.__Lock:                                                           # Get the __Lock
      if not os.path.isdir(os.path.dirname(dest)):                              # If the destination directory does NOT exist
        os.makedirs(os.path.dirname(dest));                                     # Create it
    return src, dest;                                                           # Return the source and destination directories
  ##############################################################################
  def _getCover(self, dest, info, logFmt):
    '''
    Wrapper function to parse track information
    a attempt cover art download.
    '''
    self.__Lock.acquire();                                                      # Get the __Lock so that cant try to download same cover art at once
    cover = os.path.join( os.path.dirname(dest), 'coverart.jpeg' );             # Set path to cover art file
    if os.path.isfile(cover):                                                   # If the cover art file exists
      cover = None if os.stat(cover).st_size == 0 else cover;                   # Set cover code to zero if cover art file exists
    elif ('Artist' in info or 'Album Artist' in info) and ('Album' in info):    # Else, if there is enough information in the info dictionary
      if ('Album Artist' in info):                                              # If the album artist is in the dictionary
        artist = info['Album Artist'];                                          # Attempt to download album art work for the album IF the 
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
    self.__Lock.release();                                                      # Release the lock
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
    nProc = len(self.process)
    if nProc >= self.nProc:                                                     # If running enough process
      while all( [proc.is_alive() for proc in self.process] ):                  # While all the process are alive
        time.sleep(0.01);                                                       # Sleep for a little
      for i in range(nProc):                                                    # One of the process is no longer alive so iterate to find the dead one
        if not self.process[i].is_alive():                                      # If the process is not alive
          proc = self.process.pop(i);                                           # Pop off the process
          try:                                                                  # Try to...
            proc.join();                                                        # Join the process
          except:                                                               # On exception
            proc.communicate();                                                 # Communicate with process
          return proc;                                                          # Return the handle of the finished process
    return None;                                                                # Return None
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