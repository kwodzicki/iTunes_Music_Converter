#!/usr/bin/env python
import setuptools
import subprocess, os, site;
print('Hello')

def add_to_profile( file, path ):
  if not check_profile( file, path ):
    with open(file, 'a') as f:
      f.write("\n# Add python bin to path\n");
      f.write("export PATH=$PATH:{}\n".format(path));

def check_profile( file, path ):
  with open(file, 'r') as f:
    data = f.read();
  if path in data:
    return True;
  return False;

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
	
# Code to add path to user profile
base = site.PREFIXES[0];
path = os.path.join(base, 'bin')

if os.path.isfile( os.path.join(home, '.profile' ) ):
	profile = os.path.join(home, '.profile');
	add_to_profile( profile, path );
elif os.path.isfile( os.path.join(home, '.bash_profile' ) ):
	profile = os.path.join(home, '.bash_profile' );
	add_to_profile( profile, path );
else:
	profile = os.path.join(home, '.bash_profile' );
	add_to_profile( profile, path );



setuptools.setup(
  name         = "iTunes_Music_Converter",
  description  = "Convert music in iTunes library to MP3 and FLAC files.",
  url          = "https://github.com/kwodzicki/iTunes_Music_Converter",
  author       = "Kyle R. Wodzicki",
  author_email = "krwodzicki@gmail.com",
  version      = "0.3.2",
  packages     = setuptools.find_packages(),
  install_requires = [ 
    "musicbrainzngs", "mutagen", "Pillow", "tkinter"
  ],
  package_data         = {'iTunes_Music_Converter': [ appFile ]},
  include_package_data = True,
  scripts=['bin/iTunes_Music_Converter'],
  zip_safe = False
);
