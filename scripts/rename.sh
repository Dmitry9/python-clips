#!/bin/bash

for file in ./audio/subfolder/*.mp3; do
    mv "$file" "${file/chapter_silence_/}"
done