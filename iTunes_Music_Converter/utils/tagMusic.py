#!/usr/bin/env python
from PIL import Image;
import mutagen
from mutagen import id3, mp3, flac;


def flacImage(  artwork ):
	pic = flac.Picture();                                                         # Initialize flac picture class
# 	with open(artwork, 'rb') as f: pic.data = f.read();                           # Read the artwork into pic.data
	im         = Image.open( artwork );                                           # Open the artwork file
	pic.data   = open(artwork, 'rb').read();
	pic.type   = id3.PictureType.COVER_FRONT;                                     # Set image type
	pic.mime   = u"image/{}".format(im.format.lower());                           # Set image format
	pic.width  = im.size[0];                                                      # Set image width
	pic.height = im.size[1];                                                      # Set image height
# 	pic.depth  = 16 # color depth
	im.close()
	return pic;                                                                   # Return the picture instance

def mp3Image( artwork ):
	im = Image.open( artwork );
	pic = id3.APIC(
		encoding = 3,
		type     = id3.PictureType.COVER_FRONT,
		mime     = u"image/{}".format(im.format.lower()),
		data     = open(artwork,'rb').read()
	);
	im.close()
	return pic;

def flacTags( file, info, artwork = None ):
	inst = flac.FLAC( file );
	inst.delete();
	inst.save();
	if ('Name'         in info): inst['TITLE']       = info['Name'];              # Append the track name to the dictionary
	if ('Artist'       in info): inst['ARTIST']      = info['Artist'];            # Add the artist to the dictionary
	if ('Album Artist' in info): inst['ALBUMARTIST'] = info['Album Artist'];      # Add the album artist to the dictionary
	if ('Album'        in info): inst['ALBUM']       = info['Album'];             # Add the album to the dictionary
	if ('Composer'     in info): inst['COMPOSER']    = info['Composer'];          # Add the composer to the command     
	if ('Genre'        in info): inst['GENRE']       = info['Genre'];             # Add the genre to the dictionary
	if ('Year'         in info): inst['YEAR']        = str(info['Year']);         # Add the year to the dictionary
	if ('Disc Number'  in info): inst['DISCNUMBER']  = str(info['Disc Number']);  # Add the disk number to the dictionary
	if ('Disc Count'   in info): inst['DISCTOTAL']   = str(info['Disc Count']);   # Tot number of discs
	if ('Track Number' in info): inst['TRACKNUMBER'] = str(info['Track Number']); # Add the track number to the dictionary
	if ('Track Count'  in info): inst['TRACKTOTAL']  = str(info['Track Count']);  # Total number of tracks
	if artwork is not None: inst.add_picture( flacImage(artwork) );
	inst.save();
	
def mp3Tags( file, info, artwork = None ):
	inst = mp3.MP3(file);
	inst.delete();
	inst.save();
	inst = mp3.EasyMP3(file);
	try:
		inst.add_tags();
	except:
		pass
	if ('Name'         in info): inst['title']       = info['Name'];             # Append the track name to the command
	if ('Artist'       in info): inst['artist']      = info['Artist'];           # Add the artist to the command
	if ('Album Artist' in info): inst['albumartist'] = info['Album Artist'];     # Add the album artist to the command
	if ('Album'        in info): inst['album']       = info['Album'];            # Add the album to the command
	if ('Composer'     in info): inst['composer']    = info['Composer'];         # Add the composer to the command     
	if ('Genre'        in info): inst['genre']       = info['Genre'];            # Add the genre to the command
	if ('Year'         in info): inst['date']        = str(info['Year']);        # Add the year to the command
	if ('Disc Number'  in info):
		tmp = str(info['Disc Number']);#.encode('utf-8');                             # Add the disk number to the command
		if ('Disc Count' in info):
			tmp = tmp + '/' + str(info['Disc Count']);#.encode('utf-8');                # Add the number of disks to the command
		inst['discnumber'] = tmp;
	if ('Track Number' in info):
		tmp = str(info['Track Number']);#.encode('utf-8');                            # Add the track number to the command
		if ('Track Count' in info):
			tmp += '/' + str(info['Track Count']);#.encode('utf-8');               # Add the number of tracks to the command
		inst['tracknumber'] = tmp;
	inst.save()
	if artwork is not None: 
		inst = id3.ID3(file);
		inst["APIC"] = mp3Image(artwork);
		inst.save();


def tagMusic( file, info, artwork = None ):
	inst = None;
	if file.lower().endswith('flac'):                                             # Check if file is flac
		flacTags( file, info, artwork = artwork );
	else:
		mp3Tags( file, info, artwork = artwork  );
	
if __name__ == "__main__":
	import sys
	if len(sys.argv) != 3:
		print('Incorrect number of inputs')
		exit()
	tagMusic( sys.argv[1], sys.argv[2] );