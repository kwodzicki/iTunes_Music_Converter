#!/usr/bin/env python
# Two functions used to download album artwork
import sys, os, io, time;
import musicbrainzngs as MB;
from subprocess import call
from PIL import Image;

to_unicode = lambda x: x;
maxAttempt = 3
importance = ['format', 'year', 'tracks', 'lang', 'status'];                    # This sets the importance of given inputs. If no artwork is found, then these are set to None one by one in an attempt to find artwork

##############################################################################
def search_releases(artist, album, quality):
  attempt = 0;
  while attempt < maxAttempt:
    try:
      result = MB.search_releases(artist=artist, release=album, quality=quality);# Attempt to get release information
    except:
      attempt+=1;                                                               # Increment the attempt counter by one
      time.sleep(2);                                                            # Sleep 2 seconds
    else:  
      break;  
  if attempt == maxAttempt: return None;                                         # If MusicBrainz search fails three times, return 2
  return result;  
##############################################################################
def get_release_by_id(release_id):
  attempt = 0;                                                                  # Set attempt number for album art
  while attempt < maxAttempt:  
    try:  
      result = MB.get_release_by_id( release_id )['release'];                   # Get information about the relase
    except:  
      attempt+=1;                                                               # Increment the attempt counter by one
      time.sleep(2);                                                            # Sleep 10 seconds
    else:  
      break;  
  if attempt == maxAttempt: return None;                                         # If MusicBrainz search fails three times, return 2
  return result;  
##############################################################################  
def get_image(release_info, release_id, file):  
  if 'cover-art-archive' in release_info:  
    if 'front' in release_info['cover-art-archive']:  
      if release_info['cover-art-archive']['front'] == 'true':  
        attempt = 0;                                                            # Set attempt number for album art
        while attempt < maxAttempt:  
          try:  
            image = MB.caa.get_image(release_id, 'front');                      # Download the image
          except:  
            attempt+=1;                                                         # Increment the attempt counter by one
            time.sleep(2);                                                      # Sleep 10 seconds
          else:  
            break;  
        if attempt == maxAttempt: return False;                                 # If MusicBrainz search fails three times, return 2
        im = Image.open( io.BytesIO( image ) );                                 # Open up a PIL image
        if 'JPEG' not in im.format.upper():                                     # If the image is not JPEG
          im = im.convert('RGB');                                               # Convert to jpeg
        if im.size[0] > 500 or im.size[1] > 500:                                # If the image is too large
          im = im.resize( (500,500,) );                                         # Resize it
        im.save(file, quality=80);          
        return True;
##############################################################################  
def parse_release( release ):
  '''
  Name:
    parse_release
  Purpose:
    A function to parse out information of interest from a dictionary containing
    information about a release.
  Inputs:
    release : Dictionary containing information about a release grabbed from
               the MusicBrainz API using the musicbrainzngs python package.
  Outputs:
    Returns a dictionary with the following information:
      status, format, number of tracks, date, language.
    If any of this information was NOT found in the release information, the
    value in the dictionary is None.
  Keywords:
    None.
  Author and History:
    Kyle R. Wodzicki     Created 24 May 2016

      Modified 12 Nov. 2016 by Kyle R. Wodzicki
        Added the 'rm_special' function to remove fancy unicode apostrophes.
      Modified 18 Nov. 2016 by Kyle R. Wodzicki
        Added removal of ellipsis to 'rm_special' function.
  '''
  def rm_special(in_var):
    in_var = in_var.replace(u"\u2018", "'").replace(u"\u2019", "'");            # Remove fancy single quotes; replace with standard single quote
    in_var = in_var.replace(u"\u201c",'"').replace(u"\u201d", '"');             # Remove fancy double quotes; replace with standard double quote
    in_var = in_var.replace(u"\u2026",'...');                                   # Remove ellipsis; replace with 3 periods
    in_var = in_var.replace(u"\u2010", '-');                                    # Remove fancy hypen; replace with normal hyphen
    return in_var;                                                              # Return variable

  if ('status'        not in release) or ('release-group' not in release) or \
     ('artist-credit' not in release) or ('title'         not in release):
    return None;                                                                # These two tags are required at minimum, so if either does NOT exist, return None.
  if ('type' not in release['release-group']):
    return None;                                                                # If there is no release type under the release-group tag, then return None
  data = {}
  if ('artist' not in release['artist-credit'][0]):
    return None;
  else:
    tmp = release['artist-credit'][0]['artist']
    if ('name' in tmp):
      data['artist'] = to_unicode(rm_special(tmp['name'])).upper();
    elif ('sort-name' in tmp):
      data['artist'] = to_unicode(rm_special(tmp['sort-name'])).upper();
    else:
      return None;
  data['album']    = to_unicode(rm_special(release['title'])).upper();               # Get album title
  data['status']   = to_unicode(release['status']).upper();                     # Get the status of the release
  data['disambig'] = None
  if ('disambiguation' in release):
#     if (release['disambiguation'] != ''):
    data['disambig'] = to_unicode(rm_special(release['disambiguation'])).upper();
  if ('medium-list' in release):
    tmp = release['medium-list'][0]
    data['format'] = to_unicode(tmp['format'])      if ('format'      in tmp) else None;
    data['tracks'] = to_unicode(tmp['track-count']) if ('track-count' in tmp) else None;
  else:
    data['format'] = None;
    data['tracks'] = None;
  
  data['year'] = None;
  if ('date' in release):
    if release['date'][:4] != '':
      data['year'] = int(release['date'][:4]);
  elif ('release-event-list' in release):
    tmp = release['release-event-list'][0]
    if 'date' in tmp:
      if tmp['date'][:4] != '':
        data['year'] = int(tmp['date'][:4]);
  data['lang'] = None;
  if ('text-representation' in release):
    if ('language' in release['text-representation']):
      data['lang'] = to_unicode(release['text-representation']['language']).upper();
  return data;
##############################################################################  
def get_album_art(artist, album, file, 
  year = None, lang = None, tracks = None, quality = None, format = None, 
  status = None, verbose = False):
  '''
  Name:
    get_album_art
  Purpose:
    A function to download album artwork using the musicbrainz api
  Inputs:
    artist  : The artist of the album
    album   : Name of the album
    file    : Full path to where the file will be downloaded
  Outputs:
    Downloads album artwork
  Keywords:
    year     : Year album was released
    tracks   : The number of tracks on the album. Default is None.
    lang     : The language of the release. Default is english (eng)
    quality  : Quality of the returned info. Default is high.
    format   : Format of the release (cd, vinyl, etc.). Default is CD.
    status   : The type of release. Default is official.
  Author and History:
    Kyle R. Wodzicki     Created 24 May 2016
      Adapted from examples int he musicbrainzngs package.

      Modified 12 Nov. 2016 by Kyle R. Wodzicki
        Changed the data['artist'] == artist.upper() to 
        data['artist'] in artist.upper(). This should allow a little more 
        flexibility. One example is the Riding with the King album by B.B. King
        and Eric Clapton. However, musicbrainz has the artist as just B.B. King.
        Issues may arise if the name of an artist somehow fits into the name
        of the artist of interest.
  '''
  MB.set_useragent("iTunes_Convert_KRW", "1.0");                                # Set the user of the MusicBrainz API
  MB.set_rate_limit(limit_or_interval=False);                                   # Set the limit interval to false, i.e., no limit

  open(file, 'a').close();                                                    # Empty file created so do not attempt to download on subsequent runs. THIS FILE IS OVERWRITTEN IF ARTWORK FOUND!!!!
  quality = 'high'     if quality is None else quality;
  status  = 'official' if status  is None else status;
  lang    = 'eng'      if lang    is None else lang;
  format  = 'CD'       if format  is None else format;

  release_id = None;                                                            # Set release_id to None
  result = search_releases(artist, album, quality);  
  if result is None: return 2  
  for i in range(-1,len(importance)):  
    if (i >= 0): exec(importance[i] + " = None");                          # Set a given 'importance' variable to None.
    for release in result['release-list']:                                      # Iterate over list of releases
      data = parse_release( release );                                          # Parse the release
      if data is None: continue;                                                # If vital information not present in release, the skip
      if (verbose is True): print( data );                                      # Print data IF verbose
      if (data['artist'] in artist.upper() or artist.upper() in data['artist']):
        if (data['album'] not in album.upper() and \
            album.upper() not in data['album']): continue;
        if (status is not None):
          if (data['status'] != status.upper()): continue;                      # If status exists and does NOT match the default status, skip
        if (data['disambig'] is not None):  
          if (data['disambig'] not in album.upper()): continue;  
        if (format is not None):  
          if (format.upper() != data['format']): continue;                      # If user input format for the album and that does not match the number on the release, skip
        if (tracks is not None):  
          if (int(tracks) != data['tracks']): continue;                         # If user input number of tracks and that does not match the number on the release, skip
        if (year is not None):  
          if (int(year) != data['year']): continue;                             # If user input year and that does not match the year of the release, skip
        if (lang is not None):  
          if (lang.upper() != data['lang']): continue;                          # If user input year and that does not match the year of the release, skip
        release_id = release['id'];                                             # Get the MusicBrainz ID for the album
        release_info = get_release_by_id( release_id );                    # Get information about the relase
        if release_info is None: return 3;                                      # If MusicBrainz search fails three times, return 2
        if (verbose is True): print( release_info );
        if get_image(release_info, release_id, file):
          return 0;
  return 1


# Set up command line arguments for the function
if __name__ == "__main__":
  import argparse;                                                              # Import library for parsing
  parser = argparse.ArgumentParser(description="Album Cover Art Grabber")       ; # Set the description of the script to be printed in the help doc, i.e., ./script -h
  parser.add_argument("-a", "--artist",  metavar='artist name',       type=str, \
    help="Artist that create the album. Required input!");                      # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-A", "--album",   metavar='album name',        type=str, \
    help="Name of the album. Required input!");                                 # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-y", "--year",    metavar='year of release',   type=str, \
    help="Year the album was released. Optional input.");                       # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-t", "--tracks",  metavar='number of tracks',  type=str, \
    help="The number of tracks on the album. Optional input.");                 # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-q", "--quality", metavar='quality of matches', type=str, \
    help="Quality of matches from MusicBrainz. Default is high.");              # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-f", "--format",  metavar='vinyl,cd,etc.',     type=str, \
    help="Type of medium the album was released on. Default is CD.");           # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-s", "--status",  metavar='release status',    type=str, \
    help="Status of the release. Default is offical.");                         # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("-v", "--verbose", action='store_true', \
    help="Increase verbosity");                                                 # Set an option of inputing of a file path. No dictionary can be passed via the command line
  parser.add_argument("file",            metavar='file',              type=str, \
    help="Path to download the file to. Default is current directory.");        # Set an option of inputing of a file path. No dictionary can be passed via the command line

  args = parser.parse_args();                                                   # Parse the args
  if (args.artist is None) or (args.album is None) or (args.year is None):
    print( 'Must input artist, album, and year!' )
    quit();
  return_code = get_album_art(args.artist, args.album, args.file, \
                              year    = args.year, \
                              tracks  = args.tracks, \
                              quality = args.quality, \
                              format  = args.format, \
                              status  = args.status, \
                              verbose = args.verbose); # Call the function to write the tags
  if (return_code == 4):
    print( 'Error getting cover art!' );
  elif (return_code == 3):
    print( 'Error getting release information!' );
  elif (return_code == 2):
    print( 'Error searching for release information!' );
  elif (return_code == 1):
    print( 'Failed to find artwork matching request!' );
  else:
    if args.verbose is True:
      print( 'Download successful!' );