from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QLabel, QProgressBar;
from PyQt5 import QtCore;

import re, time;
import numpy as np;
from datetime import timedelta;
from threading import Thread, Lock;

durPattern = re.compile('Duration: [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}');       # Pattern for finding times
timPattern = re.compile('time=[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}');            # Pattern for finding times
convert    = np.asarray( [3600.0, 60.0, 1.0] );                                 # Conversion for total time

def parseTime( time ):
  '''Function for converting time string to total seconds'''
  time = time.split('=')[-1];
  return (np.asarray(time.split(':'), dtype = float) * convert).sum();
def parseDuration( time ):
  '''Function for converting time string to total seconds'''
  time = time.split()[-1];
  return (np.asarray(time.split(':'), dtype = float) * convert).sum();

  
################################################################################
################################################################################
################################################################################
################################################################################
class progressTrack( QFrame ):
  maxVal   = 150;
  prog     =  25;
  elapsed  = 0.0;
  progressUpdate = QtCore.pyqtSignal(int);
  artist         = QtCore.pyqtSignal(str);
  album          = QtCore.pyqtSignal(str);
  track          = QtCore.pyqtSignal(str);
  status         = QtCore.pyqtSignal(str);
  
  def __init__(self, root, orient = None, mode = None):
    QFrame.__init__(self);
    self.time    = None;                                                        # Initialize variable for computation time
    self.running = False;                                                       # Set running to False

    artist           = QLabel('Artist:');                                       # Set up label for track artist
    album            = QLabel('Album:');                                        # Set up label for track album
    track            = QLabel('Track:');                                        # Set up label for track name

    self.artistLabel = QLabel('');                                              # Set label to display track artist using the artist tkinter string var
    self.albumLabel  = QLabel('');                                              # Set label to display album artist using the album tkinter string var
    self.trackLabel  = QLabel('');                                              # Set label to display track name using the track tkinter string var

    self.artist.connect(self.artistLabel.setText)
    self.album.connect(self.albumLabel.setText)
    self.track.connect(self.trackLabel.setText);

    self.progress   = QProgressBar();                                                                          # Initialize track progress bar
    self.progress.setMaximum(self.maxVal);                                      # Set maximum value of the track progress bar
    self.progressUpdate.connect( self.progress.setValue );
    status = QLabel('');                        # Set up label for status
    self.status.connect(status.setText);
        
    layout = QGridLayout();
    layout.setColumnStretch(1, 1);
    layout.addWidget(artist,           0, 0, 1, 1);
    layout.addWidget(self.artistLabel, 0, 1, 1, 1);
    layout.addWidget(album,            1, 0, 1, 1);
    layout.addWidget(self.albumLabel,  1, 1, 1, 1);
    layout.addWidget(track,            2, 0, 1, 1);
    layout.addWidget(self.trackLabel,  2, 1, 1, 1);
    layout.addWidget(self.progress,    3, 0, 1, 2);
    layout.addWidget(status,           4, 0, 1, 2);    

    layout.setVerticalSpacing(2);
    self.setLayout( layout );
    self.show();
    self.__labelWidth = round( self.progress.width() * 0.75 );                  # Get width of progress bar after everything is packed
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
      txt = self.__truncateText( self.artistLabel, info['Album Artist'] );
      self.artist.emit( txt );                                                  # Update the artist tkinter string var
    elif ('Artist'     in info):                                                # Else, if 'Artist' is a key in the info dictionary
      txt = self.__truncateText( self.artistLabel, info['Artist'] );
      self.artist.emit( txt );                                                  # Update the artist tkinter string var
    else:                                                                       # Else
      self.artist.emit( '' );                                                   # Update the artist tkinter string var to empty string
    
    if ('Album'        in info):                                                # If 'Album' is a key in the info dictionary
      txt = self.__truncateText( self.albumLabel, info['Album'] );
      self.album.emit( txt );                                                   # Update the album tkinter string var
    else:                                                                       # Else
      self.album.emit( '' );                                                    # Update the album tkinter string var to empty string

    if ('Track Number' in info): track += '{:02} '.format(info['Track Number']);# If 'Track Number' is key in the info dictionary, append the track number (with formatting) to the track variable
    if ('Name'         in info): track += info['Name'];                         # if 'Name' is a key in the info dictionary, append track name to track variable
    txt =self.__truncateText( self.trackLabel, track);
    self.track.emit( txt );                                                     # Set the track tkinter string var using the track variable
    self.status.emit( '' );                                                     # Set status to empty
    self.progressUpdate.emit( 0 );                                              # Set the progress bar to zero (0) progress

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
    self.status.emit( text );                                                   # Update the status text
    if prog:                                                                    # If prog is True
      self.progressUpdate.emit( self.progress.value() + self.prog );            # Update the progress bar
    if finish:
      self.progressUpdate.emit( self.maxVal )                                   # Update the progress bar
      self.time  = time.time() - self.time;                                     # Set time to processing time
  ##############################################################################
  def reset(self):
    '''
    Method to reset all values in the frame
    '''
    self.progressUpdate.emit( 0 );                                              # Set progress to zero
    self.artist.emit('');                                                       # Set artist to empty string
    self.album.emit( '');                                                       # Set album to empty string
    self.track.emit( '');                                                       # Set track to empty string
    self.status.emit('');                                                       # Set status to empty string
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
    self.status.emit('Finished!');                                              # Update the text for the bar
    self.progressUpdate.emit( self.maxVal );                                    # Set progress bar to complete
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
    startVal = self.progress.value();                                           # Current value of the progress bar
    duration = None;                                                            # Set file duration to None;
    time     = 0.0;                                                             # Set current file time to None;
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
        if duration is None:                                                    # If duration is None; i.e., has not been determined yet
          test = re.search(durPattern, line);                                   # Look for the duration pattern in the line
          if test: duration = parseDuration( line[test.start():test.end()] );   # If pattern is found, then parse the duration
        else:                                                                   # Else
          test = re.search(timPattern, line);                                   # Look for a time pattern in the line
          if test:                                                              # If time patter found
            time = parseTime( line[test.start():test.end()] );                  # Parse the time into seconds          
            progress = (time / duration) * 100.0                                # Set progress to percentage of time
            self.progressUpdate.emit( startVal + progress );                    # Set progress bar position to initial position plus progress
        line = b'';                                                             # Set line back to empty byte line
    self.progressUpdate.emit( startVal + 100 );                                 # Make sure progress bar in correct position
  ##############################################################################
  def __truncateText( self, widget, txt ):
    '''
    Purpose:
       A private method to truncate long text so that the 
       GUI window does NOT resize
    Inputs:
       widget  : Handle for the widget that text will
                 be written to
       txt     : String of text that is to be written
                 to widget
    Ouputs:
       Returns truncated string
    '''
    n    = len(txt);                                                            # Number of characters in string
    px   = widget.fontMetrics().width( txt );                                   # Number of pixels in string
    if px < self.__labelWidth:                                                  # If string is smaller enough already
      return txt;                                                               # Return the input string
    else:                                                                       # Else
      px_n = px / n;                                                            # Compute # of pixels per character
      nn   = int( self.__labelWidth / px_n ) - 5;                               # Compute number of characters that will fit in widget, less 5
      return '{} ...'.format( txt[:nn] );                                       # Return newly formatted string
            
      

################################################################################
################################################################################
################################################################################
################################################################################
class progressFrame( QFrame ):
  orient      = 'horizontal';
  mode        = 'determinate';
  elapsed     = 0.0
  progressUpdate = QtCore.pyqtSignal(int);
  progressMax    = QtCore.pyqtSignal(int);
  tRemainSTR     = QtCore.pyqtSignal(str);
  tElapsSTR      = QtCore.pyqtSignal(str);
  def __init__(self, root, nprocs, dst_dir):
    '''
    Inputs:
      root    : Root window to place frame in
      nprocs  : Number of process running simultaneously
      dst_dir : The output directory for all files
    '''
    QFrame.__init__(self);

    self.tRemain    = timedelta(seconds = -1.0);
    self.refTime    = None;
    self.bars       = [None] * nprocs;                                          # List for track progress bar instances
    self.thread     = None;                                                     # Attribute to store thread handle for time remaining updater
    self.getLock    = Lock();                                                   # Threading lock, used in freeBar
    self.freeLock   = Lock();
    self._n         = -1;                                                       # Number of tracks converted
    self._m         =  0;                                                       # Number of tracks to convert

    outLabel        = QLabel( 'Output: {}'.format(dst_dir) );                   # Label for the output directory
    progLabel       = QLabel( 'Overall Progress');                              # Label for the progress bar
    tRemainSTR      = QLabel( '' )                                              # tkinter string variable for the time remaining
    tElapsSTR       = QLabel( '' );
    self.tRemainSTR.connect( tRemainSTR.setText )
    self.tElapsSTR.connect(  tElapsSTR.setText )


    self.progress = QProgressBar( );                                                                          # Progress bar
    self.progress.setValue( 0 );                                                # Initialize value to zero (0)
    self.progressMax.connect( self.progress.setMaximum );
    self.progressUpdate.connect( self.progress.setValue );
    
    self.layout = QVBoxLayout();
    self.layout.setSpacing(2);
    self.layout.addWidget( outLabel  );                                         # Pack the output dir label
    self.layout.addWidget( progLabel );                                         # Pack the progress bar label
    self.layout.addWidget( self.progress );                                     # Pack the progress bar
    self.layout.addWidget( tRemainSTR );                                        # Pack label for time remaining
    self.layout.addWidget( tElapsSTR );                                         # Pack label for time remaining
    
    self._addProgress( nprocs );                                                # Create all track progress bar instances
    self.setLayout( self.layout )
    self.show();
  ##############################################################################
  def nTracks(self, ntracks):
    '''
    Purpose:
      Method to set total number of tracks for overall progress bar
    Inputs:
      ntracks : Number of tracks that are going to be converted
    '''
    self._n = 0;
    self._m = ntracks;
    self.progressMax.emit( ntracks );                                           # Set maximum value of progress bar
  ##############################################################################
  def _addProgress(self, n):
    '''
    Purpose:
      Private method to generate track progress bars
    Inputs:
      n  : Number of CPUs to use
    '''
    for i in range(n):                                                          # Iterate over number of processes allowed at one time
      self.bars[i] = progressTrack(self, orient=self.orient, mode=self.mode);                                                                        # Initiate a progressTrack tk.Frame class
      self.layout.addWidget( self.bars[i] );                                    # Pack the class in the main window
  ##############################################################################
  def getBar(self, info):
    '''
    Purpose:
      Method to get a 'free' track progress bar; i.e., one that
      is NOT being used.
    Inputs:
      info : Dictionary of information about the track
    '''
    self.getLock.acquire();
    if self.thread is None:                                                     # If thread attribute is None, has not been started
      self.thread = Thread(target = self.__timeRemainThread);                   # Set up thread
      self.thread.start();                                                      # Start the thread
      Thread(target = self.__timeElapsThread).start();                          # Start thread for remaining time
    free = False;                                                               # Initialize free to false, this tells if a free bar has been found
    while not free:                                                             # While free is flase
      for bar in self.bars:                                                     # Iterate over all progress bars
        if not bar.is_running():                                                # If the bar is NOT running
          bar.setBar( info );                                                   # Run the setBar method on the bar to update the information
          free = True;                                                          # Set free to True
          break;                                                                # Break the for loop
      if not free: time.sleep(0.01);                                            # If not free, sleep 10 milliseconds
    self.getLock.release();                                                     # Release the getLock lock
    return bar;                                                                 # Return reference to track progress bar instance
  ##############################################################################
  def freeBar(self, bar):
    '''
    Purpose:
      Method to free a given track progress bar
    Inputs:
      bar   : Reference to the progressTrack instance that should be freed.
    '''
    self.freeLock.acquire();                                                    # Acquire lock so this method cannot be running multiple times at once
    for i in range( len(self.bars) ):                                           # Iterate over all progressTrack instances
      if self.bars[i] == bar:                                                   # If the given bar is equal to that input
        self._n += 1;                                                           # Increment number of tracks converted
        self.progressUpdate.emit( self._n );                                    # Update number of tracks converted
        self.elapsed += bar.time;                                               # Time difference between now and when free bar was found (should be roughly how long it took for conversion to occur);
        avgTime      = self.elapsed / self._n;                                  # Compute average time per file
        nRemain      = (self._m - self._n);                                     # Number of tracks remaining
        self.tRemain = timedelta(seconds = round(avgTime * nRemain));           # Compute remaining time based on number of tracks left and average process time
        bar.freeBar();                                                          # Free the bar
    self.freeLock.release();                                                    # Release the lock
  ##############################################################################
  def __timeRemainThread(self):
    '''
    Purpose:
      A private method to update the time remaining every second.
    Inputs:
      None.
    '''
    while self._n < self._m:                                                    # While the # of tracks processed is < # of tracks
      if self.tRemain.total_seconds() > 0.0:                                    # If the remaining time is greater than zero (0) seconds
        self.tRemainSTR.emit( 'Time Remaining: {}'.format( self.tRemain ) );    # Set the tRemainSTR tkinter string variable using the tRemain timedelta variable
        self.tRemain -= timedelta( seconds = 1.0 );                             # Decrement the tRemain timedelta by one (1) second
      time.sleep(1.0);                                                          # Sleep for one (1) second
    self.tRemainSTR.emit( 'Done!' );                                            # Set tRemainSTR to 'Done!'
  ##############################################################################
  def __timeElapsThread(self):
    '''
    Purpose:
      A private method to update the time remaining every second.
    Inputs:
      None.
    '''
    t0 = time.time();                                                           # Start time of thread
    while self._n < self._m:                                                    # While the # of tracks processed is < # of tracks
      t = time.strftime('%H:%M:%S', time.gmtime( time.time() - t0 ) );          # Get time elapsed since thread start and format as HH:MM:SS
      self.tElapsSTR.emit( 'Time Elapsed: {}'.format( t ) );                    # Set the tRemainSTR tkinter string variable using the tRemain timedelta variable
      time.sleep(1.0);                                                          # Sleep for one (1) second
    
        