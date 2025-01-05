#!/bin/bash

# Get a list of MP3 files in the directory
mp3_files=$(ls -1 /mnt/c/Users/dmitr/Music/it/*.mp3 | cut -d '/' -f 8)

# Create an array of MP3 file names
IFS=$'\n' read -d '' -r -a mp3_files_array <<< "$mp3_files"

# Display options to the user
echo "Select an MP3 file:"
for i in "${!mp3_files_array[@]}"; do
  echo "$((i+1))). ${mp3_files_array[$i]}"
done

# Read user input
read -p "Enter the number of the file: " choice

# Validate user input
if [[ ! "$choice" =~ ^[0-9]+$ ]] || [[ "$choice" -gt ${#mp3_files_array[@]} ]]; then
  echo "Invalid choice."
  exit 1
fi

# Get the selected file name
selected_file="${mp3_files_array[$(($choice - 1))]}"

# Echo the selected file
echo "Selected: $selected_file"