#!/usr/bin/env python
#+
# Name:
#   picture_desc
# Purpose:
#   A function to return a short description for embedded pictures based on
#   the picture type
# Inputs:
#   type : Integer for the type of picture as outlined in the FLAC specification
# Outputs:
#   Returns a short string description.
# Keywords:
#   None.
# Author and History:
#   Kyle R. Wodzicki     Created 17 May 2016
#-
def picture_desc(type):
	type = int(type);
	if (type == 0):
		desc = 'Other'.encode('utf-8');
	elif (type == 1):
		desc = 'File Icon'.encode('utf-8');
	elif (type == 2):
		desc = 'Other file icon'.encode('utf-8');
	elif (type == 3):
		desc = 'Cover (front)'.encode('utf-8');
	elif (type == 4):
		desc = 'Cover (back)'.encode('utf-8');
	elif (type == 5):
		desc = 'Leaflet page'.encode('utf-8');
	elif (type == 6):
		desc = 'Media'.encode('utf-8');
	elif (type == 7):
		desc = 'Lead artist/lead performer/soloist'.encode('utf-8');
	elif (type == 8):
		desc = 'Artist/performer'.encode('utf-8');
	elif (type == 9):
		desc = 'Conductor'.encode('utf-8');
	elif (type == 10):
		desc = 'Band/Orchestra'.encode('utf-8');
	elif (type == 11):
		desc = 'Composer'.encode('utf-8');
	elif (type == 12):
		desc = 'Lyricist/text writer'.encode('utf-8');
	elif (type == 13):
		desc = 'Recording Location'.encode('utf-8');
	elif (type == 14):
		desc = 'During recording'.encode('utf-8');
	elif (type == 15):
		desc = 'During performance'.encode('utf-8');
	elif (type == 16):
		desc = 'Movie/video screen capture'.encode('utf-8');
	elif (type == 17):
		desc = 'A bright coloured fish'.encode('utf-8');
	elif (type == 18):
		desc = 'Illustration'.encode('utf-8');
	elif (type == 19):
		desc = 'Band/artist logotype'.encode('utf-8');
	elif (type == 20):
		desc = 'Publisher/Studio logotype'.encode('utf-8');
	return desc;