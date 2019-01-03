import tkinter as tk;
from tkinter import ttk;

import re, time;
import numpy as np;
from datetime import timedelta;
from threading import Thread, Lock;

pattern = re.compile('[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}');                    # Pattern for finding times
convert = np.asarray( [3600.0, 60.0, 1.0] );                                    # Conversion for total time

def parseTime( time ):
  '''Function for converting time string to total seconds'''
  return (np.asarray(time.split(':'), dtype = float) * convert).sum();

################################################################################
################################################################################
################################################################################
################################################################################
class progressTrack( tk.Frame ):
  maxVal  = 150;
  prog    =  25;
  elapsed = 0.0;
  def __init__(self, root, orient = None, mode = None, length = None):
    tk.Frame.__init__(self, root);
    self.configure(relief = 'groove', borderwidth = 2)
    self.artist  = tk.StringVar();                                              # Initialize tkinter string variable for track artist
    self.album   = tk.StringVar();                                              # Initialize tkinter string variable for track album
    self.track   = tk.StringVar();                                              # Initialize tkinter string variable for track track
    self.status  = tk.StringVar();                                              # Initialize tkinter string variable for status
    self.time    = None;                                                        # Initialize variable for computation time
    self.running = False;                                                       # Set running to False

    artistLabel1 = tk.Label(self, text = 'Artist:');                            # Set up label for track artist
    artistLabel2 = tk.Label(self, textvariable = self.artist);                  # Set label to display track artist using the artist tkinter string var

    albumLabel1  = tk.Label(self, text = 'Album:');                             # Set up label for track album
    albumLabel2  = tk.Label(self, textvariable = self.album);                   # Set label to display album artist using the album tkinter string var

    trackLabel1  = tk.Label(self, text = 'Track:');                             # Set up label for track name
    trackLabel2  = tk.Label(self, textvariable = self.track);                   # Set label to display track name using the track tkinter string var

    self.progress = ttk.Progressbar(
        self, orient = orient, length = length, mode = mode
    );                                                                          # Initialize track progress bar
    self.progress['maximum'] = self.maxVal;                                     # Set maximum value of the track progress bar
  
    status = tk.Label(self, textvariable = self.status);                        # Set up label for status
    
    artistLabel1.grid(  row = 0, column = 0, padx = 5, sticky = 'w'   );        # Place elements in grid
    artistLabel2.grid(  row = 0, column = 1, padx = 5, sticky = 'w'   );        # Place elements in grid
    albumLabel1.grid(   row = 1, column = 0, padx = 5, sticky = 'w'   );        # Place elements in grid
    albumLabel2.grid(   row = 1, column = 1, padx = 5, sticky = 'w'   );        # Place elements in grid
    trackLabel1.grid(   row = 2, column = 0, padx = 5, sticky = 'w'   );        # Place elements in grid
    trackLabel2.grid(   row = 2, column = 1, padx = 5, sticky = 'w'   );        # Place elements in grid
    self.progress.grid( row = 3, column = 0, padx = 5, columnspan = 2 );        # Place elements in grid
    status.grid(        row = 4, column = 0, padx = 5, columnspan = 2 );        # Place elements in grid
  ##############################################################################
  def updateInfo(self, info):
    '''
    Purpose:
       Method to update the artist/album/track information
    Inputs:
       info : Dictionary of track information
    '''
    track = '';                                                                 # Initialize track to empty string
    if ('Album Artist' in info):                                                # If 'Album Artist' is a key in the info dictionary
      self.artist.set( info['Album Artist'] );                                  # Update the artist tkinter string var
    elif ('Artist'     in info):                                                # Else, if 'Artist' is a key in the info dictionary
      self.artist.set( info['Artist'] );                                        # Update the artist tkinter string var
    else:                                                                       # Else
      self.artist.set( '' );                                                    # Update the artist tkinter string var to empty string
    
    if ('Album'        in info):                                                # If 'Album' is a key in the info dictionary
      self.album.set( info['Album'] );                                          # Update the album tkinter string var
    else:                                                                       # Else
      self.album.set( '' );                                                     # Update the album tkinter string var to empty string

    if ('Track Number' in info): track += '{:02} '.format(info['Track Number']);# If 'Track Number' is key in the info dictionary, append the track number (with formatting) to the track variable
    if ('Name'         in info): track += info['Name'];                         # if 'Name' is a key in the info dictionary, append track name to track variable
    self.track.set( track );                                                    # Set the track tkinter string var using the track variable
    self.status.set( '' );                                                      # Set status to empty
    self.progress['value'] = 0;                                                 # Set the progress bar to zero (0) progress
  ##############################################################################
  def updateStatus(self, text, prog = False, finish = False):
    '''
    Purpose:
      Method to update status text
    Inputs:
      text   : Text to update status to
    Keywords:
      prog   : If set to True, will increment the progress bar
      finish : If set to True, will set progress bar to done
    '''
    self.status.set( text );                                                    # Update the status text
    if prog:                                                                    # If prog is True
      self.progress['value'] = self.progress['value'] + self.prog;              # Update the progress bar
    if finish:
      self.progress['value'] = self.maxVal;                                     # Update the progress bar
      self.time  = time.time() - self.time;                                     # Set time to processing time
  ##############################################################################
  def reset(self):
    '''
    Method to reset all values in the frame
    '''
    self.progress['value'] = 0;                                                 # Set progress to zero
    self.artist.set('');                                                        # Set artist to empty string
    self.album.set( '');                                                        # Set album to empty string
    self.track.set( '');                                                        # Set track to empty string
    self.status.set('');                                                        # Set status to empty string
  ##############################################################################
  def setBar(self, info):
    '''
    Purpose:
      Method to set up the information in the bar
    Inputs:
      info   : Dictionary containing information about the track
    '''
    self.running = True;                                                        # Set running to True so bar cannot be used by another process
    self.updateInfo( info );                                                    # Update the information
    self.time = time.time();                                                    # Get current time for when process started
  ##############################################################################
  def freeBar(self):
    '''
    Method for freeing the bar for use by another process
    '''
    self.running = False;                                                       # Set running to False
  ##############################################################################
  def is_running(self):
    '''
    Method to check if the bar is being used
    '''
    return self.running;                                                        # Return value of running
  ##############################################################################
  def finish(self):
    '''
    Method for setting bar to 'Finished'. 
    Bar is intended to be freed by the progressFrame class.
    '''
    self.status.set('Finished!');                                               # Update the text for the bar
    self.progress['value'] = self.maxVal;                                       # Set progress bar to complete
    self.time  = time.time() - self.time;                                       # Set time to processing time
  ##############################################################################
  def conversion(self, proc):
    '''
    Purpose:
      Method to monitor the progress of FFmpeg so that the
      progress bar can be updated.
    Inputs:
      proc : Handle returned by call to subprocess.Popen.
              stdout must be sent to subprocess.PIPE and
              stderr must be sent to subprocess.STDOUT.
    '''
    startVal = self.progress['value'];                                          # Current value of the progress bar
    duration = None;                                                            # Set file duration to None;
    time     = None;                                                            # Set current file time to None;
    progress = 0;                                                               # Set progress to zero (0)
    line     = b'';                                                             # Set line to empty byte line
    while True:                                                                 # Iterate forever
      char = proc.stdout.read(1);                                               # Read one (1) byte from stdout/stderr
      if char == b'':                                                           # If the byte is empty
        break;                                                                  # Break the while loop
      elif char != b'\n' and char != b'\r':                                     # Else, if byte is NOT one of the return characters
        line += char;                                                           # Append the byte to the line variable
      else:                                                                     # Else, must be end of line
        line = line.decode('utf8');                                             # Convert byte line to string
        test = re.search(pattern, line);                                        # Look for a time pattern in the line
        if test:                                                                # If a time is found
          time = parseTime( line[test.start():test.end()] );                    # Parse the time into seconds
          if duration is None:                                                  # If duration has not been set, then assume this is the duration of the file
            duration = time;                                                    # Set duration to time
            time     = 0.0;                                                     # Set time to zero
          else:                                                                 # Else
            progress = (time / duration) * 100.0                                # Set progress to percentage of time
            self.progress['value'] = startVal + progress;                       # Set progress bar position to initial position plus progress
        line = b'';                                                             # Set line back to empty byte line
    self.progress['value'] = startVal + 100.0;                                  # Make sure progress bar in correct position


################################################################################
################################################################################
################################################################################
################################################################################
class progressFrame( tk.Frame ):
  orient  = 'horizontal';
  mode    = 'determinate';
  length  = 200;
  elapsed = 0.0
  def __init__(self, root, nprocs, dst_dir):
    '''
    Inputs:
      root    : Root window to place frame in
      nprocs  : Number of process running simultaneously
      dst_dir : The output directory for all files
    '''
    tk.Frame.__init__(self, root);

    self.tRemainSTR = tk.StringVar();                                           # tkinter string variable for the time remaining
    self.tRemain    = timedelta(seconds = -1.0);                                # floating variable for time remaining
    self.bars       = [None] * nprocs;                                          # List for track progress bar instances
    self.thread     = None;                                                     # Attribute to store thread handle for time remaining updater
    self.lock       = Lock();                                                   # Threading lock, used in freeBar
    
    frame     = tk.Frame( self );                                               # Frame for the overall progress
    outLabel  = tk.Label( frame, text = 'Output: {}'.format(dst_dir) );         # Label for the output directory
    progLabel = tk.Label( frame, text = 'Overall Progress');                    # Label for the progress bar
    self.progress = ttk.Progressbar(
      frame, orient=self.orient, length=self.length, mode=self.mode
    );                                                                          # Progress bar
    self.progress['value'] = 0;                                                 # Initialize value to zero (0)

    tRemainLabel = tk.Label( frame, textvariable = self.tRemainSTR );           # Label for time remaining
    outLabel.pack();                                                            # Pack the output dir label
    progLabel.pack();                                                           # Pack the progress bar label
    self.progress.pack();                                                       # Pack the progress bar
    tRemainLabel.pack();                                                        # Pack label for time remaining
    frame.pack();                                                               # Pack the frame
    
    self._addProgress( nprocs );                                                # Create all track progress bar instances
    self.pack();                                                                # Pack self frame
  ##############################################################################
  def nTracks(self, ntracks):
    '''
    Purpose:
      Method to set total number of tracks for overall progress bar
    Inputs:
      ntracks : Number of tracks that are going to be converted
    '''
    self.progress['maximum'] = ntracks;                                         # Set maximum value of progress bar
  ##############################################################################
  def _addProgress(self, n):
    '''
    Purpose:
      Private method to generate track progress bars
    Inputs:
      n  : Number of CPUs to use
    '''
    for i in range(n):                                                          # Iterate over number of processes allowed at one time
      self.bars[i] = progressTrack(
        self, orient = self.orient, mode = self.mode, length = self.length
      );                                                                        # Initiate a progressTrack tk.Frame class
      self.bars[i].pack(padx = 5, pady = 5);                                    # Pack the class in the main window
  ##############################################################################
  def getBar(self, info):
    '''
    Purpose:
      Method to get a 'free' track progress bar; i.e., one that
      is NOT being used.
    Inputs:
      info : Dictionary of information about the track
    '''
    if self.thread is None:                                                     # If thread attribute is None, has not been started
      self.thread = Thread(target = self.__timeRemainThread);                   # Set up thread
      self.thread.start();                                                      # Start the thread

    for bar in self.bars:                                                       # Iterate over all progress bars
      if not bar.is_running():                                                  # If the bar is NOT running
        bar.setBar( info );                                                     # Run the setBar method on the bar to update the information
        return bar;                                                             # Return reference to track progress bar instance
  ##############################################################################
  def freeBar(self, bar):
    '''
    Purpose:
      Method to free a given track progress bar
    Inputs:
      bar   : Reference to the progressTrack instance that should be freed.
    '''
    self.lock.acquire();                                                        # Acquire lock so this method cannot be running multiple times at once
    for i in range( len(self.bars) ):                                           # Iterate over all progressTrack instances
      if self.bars[i] == bar:                                                   # If the given bar is equal to that input
        self.elapsed += bar.time;                                               # Time difference between now and when free bar was found (should be roughly how long it took for conversion to occur);
        self.progress['value'] += 1;                                            # Increment number of tracks converted
        avgTime      = self.elapsed / self.progress['value'];                   # Compute average time per file
        nRemain      = (self.progress['maximum'] - self.progress['value']);     # Number of tracks remaining
        self.tRemain = timedelta(seconds = round(avgTime * nRemain));           # Compute remaining time based on number of tracks left and average process time
        bar.freeBar();                                                          # Free the bar
    self.lock.release();                                                        # Release the lock
  ##############################################################################
  def __timeRemainThread(self):
    '''
    Purpose:
      A private method to update the time remaining every second.
    Inputs:
      None.
    '''
    while self.progress['value'] < self.progress['maximum']:                    # While the # of tracks processed is < # of tracks
      if self.tRemain.total_seconds() > 0.0:                                    # If the remaining time is greater than zero (0) seconds
        self.tRemainSTR.set( 'Time Remaining: {}'.format( self.tRemain ) );     # Set the tRemainSTR tkinter string variable using the tRemain timedelta variable
        self.tRemain -= timedelta( seconds = 1.0 );                             # Decrement the tRemain timedelta by one (1) second
      time.sleep(1.0);                                                          # Sleep for one (1) second
    self.tRemainSTR.set( 'Done!' );                                             # Set tRemainSTR to 'Done!'
    
        