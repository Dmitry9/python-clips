#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <track_number>"
  exit 1
fi

track_number="$1"

mkdir audio
cd audio/
mkdir subfolder
cp /mnt/c/Users/dmitr/Music/it/${track_number}.mp3 .
mv ${track_number}.mp3 chapter.mp3
# in audio folder
mp3splt -d subfolder -s -p th=-50 chapter.mp3
cd ..
bash scripts/rename.sh
rm audio/*.log
rm audio/chapter.mp3
python 2_slow_down.py
python 3_concat_mp3.py silience-5.mp3
find ./with_silience -maxdepth 2 -name "*.mp3" -printf "file '%p'\n" > input.txt
sort -t'/' -k3 -n input.txt -o input.txt
ffmpeg -f concat -safe 0 -i input.txt -c copy output.mp3
mv output.mp3 /mnt/c/Users/dmitr/Music/it/paused/${track_number}.mp3
bash scripts/cleanup.sh