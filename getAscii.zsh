# !/usr/bin/env zsh

echo $#

if [[ $# < 1 ]]
then
  echo "1 argument that points to the img file path has to be specified"
  exit

else 

fi

filename="${1##*/}"
dirname="${1%/*}"
file=${1:t:r}

if [[ "$filename" = "$dirname" ]];
then
  $dirname="."
fi

echo "File without format: $file"
echo "Filename: $filename"
echo "Dirname: $dirname"

if [[ $(file -b $1) =~ JPEG ]];  
then 
  echo "$1 is a jpeg, no need for conversion"
  thumbnail=$1
else 
  
  echo "$1 is not jpeg, converting now..."
  thumbnail="$dirname/$file.jpg"
  sips -s format jpeg $1 --out "$dirname/$file.jpg" > /dev/null
fi

jp2a --width=80 --colors $thumbnail


