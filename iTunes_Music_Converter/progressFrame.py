import tkinter as tk;
from tkinter import ttk;

import re, time;
import numpy as np;
from datetime import timedelta;

pattern = re.compile('[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}');
convert = np.asarray( [3600.0, 60.0, 1.0] );

def parseTime( time ):
  return (np.asarray(time.split(':'), dtype = float) * convert).sum();

class progressTrack( tk.Frame ):
  maxVal  = 150;
  prog    =  25;
  elapsed = 0.0;
  def __init__(self, root, orient = None, mode = None, length = None):
    tk.Frame.__init__(self, root);
    self.configure(relief = 'groove', borderwidth = 2)
    self.artist  = tk.StringVar();
    self.album   = tk.StringVar();
    self.track   = tk.StringVar();
    self.status  = tk.StringVar();
    self.time    = None;
    self.running = False;

    artistLabel1 = tk.Label(self, text = 'Artist:');
    artistLabel2 = tk.Label(self, textvariable = self.artist);

    albumLabel1  = tk.Label(self, text = 'Album:');
    albumLabel2  = tk.Label(self, textvariable = self.album);

    trackLabel1  = tk.Label(self, text = 'Track:');
    trackLabel2  = tk.Label(self, textvariable = self.track);

    self.progress = ttk.Progressbar(
        self, orient = orient, length = length, mode = mode
    );
    self.progress['maximum'] = self.maxVal;
    
    status = tk.Label(self, textvariable = self.status)
    artistLabel1.grid(  row = 0, column = 0, padx = 5, sticky = 'w' );
    artistLabel2.grid(  row = 0, column = 1, padx = 5, sticky = 'w' );
    albumLabel1.grid(   row = 1, column = 0, padx = 5, sticky = 'w' );
    albumLabel2.grid(   row = 1, column = 1, padx = 5, sticky = 'w' );
    trackLabel1.grid(   row = 2, column = 0, padx = 5, sticky = 'w' );
    trackLabel2.grid(   row = 2, column = 1, padx = 5, sticky = 'w' );
    self.progress.grid( row = 3, column = 0, padx = 5, columnspan = 2);
    status.grid(        row = 4, column = 0, padx = 5, columnspan = 2 );
  ##############################################################################
  def updateInfo(self, info):
    track = '';
    if ('Album Artist' in info): 
      self.artist.set( info['Album Artist'] );
    elif ('Artist'     in info): 
      self.artist.set( info['Artist'] );
    if ('Album'        in info): self.album.set( info['Album'] );
    if ('Track Number' in info): track += '{:02} '.format(info['Track Number']);
    if ('Name'         in info): track += info['Name'];
    self.track.set( track );
    self.status.set( '' );
  ##############################################################################
  def updateStatus(self, text, prog = False):
    self.status.set( text );
    if prog:
      self.progress['value'] = self.progress['value'] + self.prog;
  ##############################################################################
  def reset(self):
    self.progress['value'] = 0
    self.artist.set('');
    self.album.set( '');
    self.track.set( '');
    self.status.set('');
  ##############################################################################
  def setBar(self, info):
    self.running = True;
    self.reset();
    self.updateInfo( info );
    self.time = time.time();
  ##############################################################################
  def freeBar(self):
    self.running = False;
  ##############################################################################
  def is_running(self):
    return self.running;  
  ##############################################################################
  def finish(self):
    self.status.set('Finished!');                                          # Update the text for the bar
    self.progress['value'] = self.maxVal;                                      # Set progress bar to complete
    self.time  = time.time() - self.time
#     self.freeBar();
  ##############################################################################
  def conversion(self, proc):
    startVal = self.progress['value'];
    duration = None;
    time     = None;
    progress = 0;
    line     = b'';
    while True:
      char = proc.stdout.read(1);
      if char == b'':
        break;
      elif char != b'\n' and char != b'\r':
        line += char;
      else:
        line = line.decode('utf8')
        test = re.search(pattern, line)
        if test:
          time = parseTime( line[test.start():test.end()] );
          if duration is None:
            duration = time;
            time     = 0.0;
          else:
            progress = (time / duration) * 100.0
            self.progress['value'] = startVal + progress;
        line = b'';
    self.progress['value'] = startVal + 100.0;


################################################################################
class progressFrame( tk.Frame ):
  orient  = 'horizontal';
  mode    = 'determinate';
  length  = 200;
  elapsed = 0.0
  def __init__(self, root, ntracks, nprocs):
    tk.Frame.__init__(self, root);

    self.bars = [None] * nprocs;
    frame     = tk.Frame( self );
    
    label = tk.Label(frame, text='Overall Progress');
    self.progress = ttk.Progressbar(frame, orient=self.orient,
                                    length=self.length, mode=self.mode);
    
    self.timeRemain = tk.StringVar();
    
    self.progress['value']   = 0;
    self.progress['maximum'] = ntracks;

    label.pack();
    self.progress.pack();
    tk.Label(frame, textvariable = self.timeRemain).pack();
    frame.pack();
    
    self._addProgress( nprocs );
    self.pack();
  ##############################################################################
  def _addProgress(self, n):
    for i in range(n):
      self.bars[i] = progressTrack(
        self, orient = self.orient, mode = self.mode, length = self.length
      );
      self.bars[i].pack(padx = 5, pady = 5);
  ##############################################################################
  def resetBar(self, bar = None):
    if bar is None:
      for bar in self.bars: bar.reset();
    else:
      self.bars[bar].reset();
  ##############################################################################
  def getBar(self, info):
    for bar in self.bars:
      if not bar.is_running():
        bar.setBar( info );
        return bar;
  ##############################################################################
  def freeBar(self, bar):
    for i in range( len(self.bars) ):
      if self.bars[i] == bar:
        self.elapsed += bar.time;                                               # Time difference between now and when free bar was found (should be roughly how long it took for conversion to occur);
        self.progress['value'] += 1;                                             # Increment number of tracks converted
        avgTime    = self.elapsed / self.progress['value']
        remain     = (self.progress['maximum'] - self.progress['value']);
        remainTime = timedelta(seconds = avgTime * remain);
        self.timeRemain.set( 'Time Remaining: {}'.format(remainTime) );
        bar.freeBar();