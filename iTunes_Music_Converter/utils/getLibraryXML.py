import os;
from .data import iTunesFolder;

def getLibraryXML( ):
  files = os.listdir( iTunesFolder );                                           # Get all files in the directory
  i     = 0;                                                                    # Set i to zero
  while i < len(files):                                                         # While i is less than the length of files
    if not files[i].endswith('.xml'):                                           # If the file does NOT end with .xml
      files.remove( files[i] );                                                 # Remove it from the list
    else:                                                                       # Else
      files[i] = os.path.join( iTunesFolder, files[i] );                        # Replace file name in list with full path to file
      i += 1;                                                                   # Increment i by one (1)
  times  = [os.stat(file).st_mtime for file in files];                          # Get modified time for each file in the files list
  newest = -9.9e-06;                                                            # Set newest time to very small number
  for time in times:                                                            # Iterate over all times
    if time > newest:                                                           # If the current modification time is larger than newest variable
      newest = time;                                                            # Set newest modification time to time
  tid = times.index( newest );                                                  # Get index of the newest time
  return files[tid];                                                            # Return file path corresponding to newest time
