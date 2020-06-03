# !/usr/bin/env zsh

showUsage ()
{
   # Display Help
   echo "[Correct Usage] zsh fetch.zsh <DEV_URL> <OPTIONAL:MP3_DIR>"
}


if [ $# < 1 ]
then
    showUsage
    exit
fi

DEFAULT_MP3_DIR="./mp3_files"
URL=$1
MP3_DIR=${2:-$DEFAULT_MP3_DIR}
echo "MP3 DIR is $MP3_DIR"
echo "Fetching from $URL ..."
# MP3_URL=$(curl "$URL" | grep ".mp3" | sed -e 's?https://www\.??' |/#   <source src="/)
MP3_URL=$(curl "$URL" | grep ".mp3")

# Hackish way for now because I can't do string matching :( 
MP3_URL=${MP3_URL:17:-20}
echo "Downloading... $MP3_URL"

# Redirect both std and error output  
wget $MP3_URL -q --show-progress --progress=bar:force 2>&1 -P $MP3_DIR

echo "Finished downloading"