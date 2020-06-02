URL=https://dev.to/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow


echo "Fetching from $URL ..."
# MP3_URL=$(curl "$URL" | grep ".mp3" | sed -e 's?https://www\.??' |/#   <source src="/)
MP3_URL=$(curl "$URL" | grep ".mp3")
# Hackish way because I can't do string matching :( 
MP3_URL=${MP3_URL:17:-20}
echo "Downloading... $MP3_URL"

# Redirect both std and error output  
wget $MP3_URL > /dev/null 2>&1