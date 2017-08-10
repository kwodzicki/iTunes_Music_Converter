#!/bin/bash
#+
# Name:
#   install_iTunes_Convert
# Purpose:
#   This bash script will copy the two scripts used to convert songs in iTunes
#   as well as add the creation of a system variable to the user's 
#   '.profile' OR '.bash_profile' files.
# Inputs:
#   None.
# Outputs:
#   None.
# Author and History:
#   Created by Kyle R. Wodzicki   on 12 May 2016.
# See READ_ME.txt for more information
#
#-
# See READ_ME.txt for more information
#

# Create function to add environment variable to '.profile' or '.bash_profile'
function add_to_profile {
  echo "" >> "$1"
  echo "# Set an environment variable for the iTunes conversion scripts" >> "$1"
  echo "export iTunesConvert=$2" >> "$1"
}

clear

# Set the name of the applicaiton
app_name="convert_music.app"

# Set the directory that the convert_music application is stored in
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source_dir="$dir/Source_Code"

echo $dir
echo $source_dir

# Download the musicbrainz python code and place it in the python directory
mb_py="$source_dir/Python/musicbrainz"
git clone git://github.com/alastair/python-musicbrainzngs.git "$mb_py"
mv "$mb_py/musicbrainzngs" "$source_dir/Python/"
rm -Rf "$mb_py"

source_app="$source_dir/Applications/$app_name"

# Set the destination directory for the convert_music application, i.e.,
#  the iTunes scripts folder
dest_dir="$HOME/Library/iTunes/Scripts"
dest_app="$dest_dir/$app_name"

# Create directory if it does not exist
if [ ! -d "$dest_dir" ]; then 
  echo 'iTunes Scripts directory does NOT exits...Creating!'
  mkdir -p "$dest_dir"
fi

# If the application exists, check if it is older than the one to be installed
if [ -e "$dest_app" ]; then
  if [ "$dest_app" -ot "$source_app" ]; then 
  	echo 'Updating Music Converter!'
  	rm -Rf "$dest_app"
  	cp -R "$source_app" "$dest_app"
  else
    echo 'MP3 Convert is already the latest version!'
  fi
else
  echo 'Installing Music Converter!'
  cp -fR "$source_app" "$dest_app"
fi


if [ -f $HOME/.profile ]; then
  echo "Adding system variable to .profile"
  add_to_profile $HOME/.profile "$source_dir/Python/"
elif [ -f $HOME/.bash_profile ]; then
  echo "Adding system variable to .bash_profile"
  add_to_profile $HOME/.bash_profile "$source_dir/Python/"
else
  echo "Creating .bash_profile"
  add_to_profile $HOME/.bash_profile "$source_dir/Python/"
fi

sleep 3
exit 0