# Navigate to your project directory
cd /mnt/c/Users/dmitr/Music/gravity-falls

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # For Linux/macOS
# OR
venv\Scripts\activate     # For Windows

# Ensure pip is up to date
pip install --upgrade pip

# Install required dependencies
pip install webvtt-py ffmpeg-python

# Save dependencies to requirements file (optional but recommended)
pip freeze > requirements.txt

# Make the script executable (optional on Linux/macOS)
chmod +x extract_phrases.py

## This command will create a 30-second MP3 file named silence.mp3 containing only silence. 
Explanation:

ffmpeg: This is the command-line tool for handling multimedia files.
-f lavfi: Specifies that the input is from a Lavfi source (Libavfilter).
-i anullsrc=r=44100:cl=mono: This creates a source of silence.
r=44100 sets the sample rate to 44.1 kHz, a common audio standard.
cl=mono specifies that the output should be in mono (single channel).
-t 30: Sets the duration of the silence to 30 seconds.
-q:a 9: Sets the audio quality to 9 (lower number means higher quality).
-acodec libmp3lame: Specifies that the output should be encoded as MP3 using the libmp3lame encoder.
silence.mp3: This is the name of the output file.

```bash
ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 30 -q:a 9 -acodec libmp3lame silience.mp3
```

# Run the script
```bash
python extract_phrases.py
```


Creating a text file that lists all the MP3 files in the order you want them concatenated. This text file is then used as input for ffmpeg.
```bash
find ./with_silience -maxdepth 2 -name "*.mp3" -printf "file '%p'\n" > input.txt
sort -t'/' -k3 -n input.txt -o input.txt
ffmpeg -f concat -safe 0 -i input.txt -c copy output.mp3
```

# Detect silience
```bash
sudo apt install mp3splt
mp3splt -h
cd ./audio
cd subfolder
mp3splt -s -p th=-50 4.mp3
```

## routine
```bash
node scripts/select.it.js
```