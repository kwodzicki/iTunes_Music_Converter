import os;

home_dir     = os.path.expanduser( '~' );                                       # Set path to users home directory
iTunesFolder = os.path.join( home_dir, 'Music', 'iTunes' );                     # Location of iTunes library information
prefix       = 'file://';