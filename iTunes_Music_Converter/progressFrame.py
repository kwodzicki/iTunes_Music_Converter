import tkinter as tk;
from tkinter import ttk;

import re, time;
import numpy as np;
from datetime import timedelta;

pattern = re.compile('[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}');
convert = np.asarray( [3600.0, 60.0, 1.0] );

def parseTime( time ):
  return (np.asarray(time.split(':'), dtype = float) * convert).sum();

class progressFrame( tk.Frame ):
  def __init__(self, root, ntracks, nprocs):
    tk.Frame.__init__(self, root);

    self.times   = None;
    self.bars    = None;
    self.texts   = None;
    self.maxVal  = 150;
    self.prog    =  25;
    self.elapsed = 0.0;
    
    frame = tk.Frame( self );
    
    label = tk.Label(frame, text='Overall Progress');
    self.totProgress = ttk.Progressbar(frame, orient="horizontal",
                                    length=200, mode="determinate");
    
    self.timeRemain = tk.StringVar();
    
    self.totProgress['value']   = 0;
    self.totProgress['maximum'] = ntracks;

    label.pack();
    self.totProgress.pack();
    tk.Label(frame, textvariable = self.timeRemain).pack();
    frame.pack();
    
    self._addProgress( nprocs );
    self.pack();
	##############################################################################
  def _addProgress(self, n):
    self.bars   = [];
    self.labels = [];
    self.texts  = [];
    self.times  = [];
    for i in range(n):
      self.times.append(0.0);
      frame = tk.Frame(self);
      self.texts.append( tk.StringVar() );
      self.bars.append(
        ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
      )
      self.bars[i]['maximum'] = self.maxVal;
      tk.Label(frame, text = 'Thread {}'.format(i+1)).pack();
      self.bars[i].pack();
      tk.Label(frame, textvariable = self.texts[i]).pack();
      
      frame.pack( padx = 5 );
	##############################################################################
  def resetBar(self, bar = None):
    if bar is None:
      for i in range( len(self.bars) ):
        self.bars[i]['value'] = 0
        self.texts[i].set('');
    else:
      self.bars[bar]['value'] = 0
      self.texts[bar].set('');
	##############################################################################
  def getFreeBar(self):
    for i in range( len(self.bars) ):
      if self.bars[i]['value'] == self.maxVal or self.bars[i]['value'] == 0:
        self.resetBar(i);
        self.bars[i]['value'] = 0.1
        self.times[bar] = time.time();
        return i;
	##############################################################################
  def updateText(self, bar, text, prog = False):
    print(bar, text);
    self.texts[bar].set( text );
    if prog:
      self.bars[bar]['value'] = self.bars[bar]['value'] + self.prog;
	##############################################################################
  def finishedBar(self, bar):
    self.elapsed += (time.time() - self.times[bar]);                            # Time difference between now and when free bar was found (should be roughly how long it took for conversion to occur);
    self.texts[bar].set('Finished!');                                           # Update the text for the bar
    self.bars[bar]['value'] = self.maxVal;                                      # Set progress bar to complete
    self.totProgress['value'] += 1;                                             # Increment number of tracks converted
    avgTime    = self.elapsed / self.totProgress['value']
    remain     = (self.totProgress['maximum'] - self.totProgress['value']);
    remainTime = timedelta(seconds = avgTime * remain);
    self.timeRemain.set( 'Time Remaining: {}'.format(remainTime) );
	##############################################################################
  def conversion(self, bar, proc):
    startVal = self.bars[bar]['value'];
    duration = None;
    time     = None;
    progress = 0;
    while True:
      line = proc.stdout.readline();
      if line == '':
        break;
      test = re.search(pattern, line)
      if test:
        time = parseTime( line[test.start():test.end()] );
        if duration is None:
          duration = time;
          time     = 0.0;
        else:
          progress = (time / duration) * 100.0
          self.bars[bar]['value'] = startVal + progress;
    self.bars[bar]['value'] = startVal + 100.0;
