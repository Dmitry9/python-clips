#!/bin/bash

for file in ./with_silience/03/03_silence_*.mp3; do
    mv "$file" "${file/03_silence_/}"
done