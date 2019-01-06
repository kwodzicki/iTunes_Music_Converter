#!/usr/bin/env python
import setuptools
import subprocess, os, site;

# Code to install the Apple Script
home = os.path.expanduser('~');
dir  = os.path.join( home, 'Library', 'iTunes', 'Scripts' );
if not os.path.isdir( dir ): os.makedirs( dir );
appFile = os.path.join( dir, 'convert_music.app' )
cmd = ['/usr/bin/osacompile', '-o', appFile, 'convert_music.txt'];
if os.path.isfile( appFile ): os.remove( appFile );
# print( out );
with open(os.devnull, 'w') as null:
	proc = subprocess.Popen(cmd, stdout=null, stderr=subprocess.STDOUT);
proc.communicate();
if proc.returncode != 0:
	raise Exception('Failed to compile convert_music application!');
	
setuptools.setup(
  name         = "iTunes_Music_Converter",
  description  = "Convert music in iTunes library to MP3 and FLAC files.",
  url          = "https://github.com/kwodzicki/iTunes_Music_Converter",
  author       = "Kyle R. Wodzicki",
  author_email = "krwodzicki@gmail.com",
  version      = "0.3.5",
  packages     = setuptools.find_packages(),
  install_requires = [ 
    "musicbrainzngs", "mutagen", "Pillow", "tkinter"
  ],
  package_data         = {'iTunes_Music_Converter': [ appFile ]},
  include_package_data = True,
  scripts=['bin/iTunes_Music_Converter'],
  zip_safe = False
);
