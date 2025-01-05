#!/bin/bash

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <track_number>"
  exit 1
fi

track_number="$1"

echo ${track_number}