#!/bin/bash
#+
# Name:
#   uninstall_iTunes_Convert
# Purpose:
#   This bash script will remove the two scripts used to convert songs in iTunes
#   as well as remove the creation of a system variable from the user's 
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

# Create a function to remove the environment variable from the users .profile
# or .bash_profile file.
function remove_from_profile {
  sed -e '/# Set an environment variable for the iTunes conversion scripts/ {
  $!N
  d
  }' "$1" > "$1.new"
  mv "$1.new" "$1"
}

clear

# Set directory script is located in
source_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/Source_Code"

# Set the name of the applicaiton
app_name="convert_music.app"

# Set the destination directory for the convert_music application, i.e.,
#  the iTunes scripts folder
dest_dir="$HOME/Library/iTunes/Scripts"

# Create directory if it does not exist
if [ ! -d "$dest_dir" ]; then 
  echo 'iTunes Scripts NOT installed...EXITING!!!'
  exit 0
else
	echo 'Removing the iTunes Script'
	rm -Rf "$dest_dir/$app_name"
fi

# Remove the system variable from the .profile or .bash_profile file
if [ -f $HOME/.profile ]; then
  echo "Removing system variable from '.profile'"
  remove_from_profile $HOME/.profile
elif [ -f $HOME/.bash_profile ]; then
  echo "Removing system variable from '.bash_profile'"
  remove_from_profile $HOME/.bash_profile
fi

sleep 3
exit 0