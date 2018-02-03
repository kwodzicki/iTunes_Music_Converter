#!/usr/bin/python
#+
# Name:
#   to_unicode
# Purpose:
#   A function to convert text from a given encoding to unicode.
# Inputs:
#   obj   : The object to decode to unicode
# Outputs:
#   Returns and unicode string of whatever input.
# Keywords:
#   encoding : Set the encoding, default is 'utf-8'
# Author and History:
#   Kyle R. Wodzicki     Created 07 May 2016
#     From http://farmdev.com/talks/unicode/
#-
def to_unicode(obj, encoding = None):
	if (encoding is None):
		encoding = 'utf-8';                # Set the default encoding
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding);    # If the input is NOT unicode, convert it
	return obj;                          # Return the object