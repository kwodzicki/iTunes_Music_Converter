#!/usr/bin/env python
#+
# Name:
#   getImageInfo_v02
# Purpose:
#   Attempts to use the OS X sips command to get information about an image.
# Inputs:
#   file  : Path to the file.
# Outputs:
#   Returns all information about the image that is returned by the sips command
#   in a dictionary.
# Keywords:
#   None
# Author and History:
#   Kyle R. Wodzicki    Created 05 Jun. 2016
#-
def getImageInfo_v02(file):
	from plistlib   import readPlistFromString as parse;
	from subprocess import check_output        as run;
	return dict( parse( run(['sips', '--getProperty', 'allxml', file]) ) );       # Run sips to get info in XML format, parse the XML data, and convert to dictionary and return
