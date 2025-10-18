#!/bin/bash

for filename in ./inputs/*; do
    if [ -d "./outputs/$(basename "$filename" .txt)" ]; then
        echo "about to render LAWKI $(basename "$filename" .txt)"
        if [ ! -f "./outputs/$(basename "$filename" .txt)/lawki.mp4" ]; then
        echo "no mp4"
        python lawki.py "$(basename "$filename" .txt)"
        fi
    fi
done