#!/bin/bash

for filename in ./inputs/*; do
    if [ ! -f "./outputs/$(basename "$filename" .txt)/FINISHED" ]; then
        echo "$(basename "$filename" .txt)"
        python src/init.py "$(basename "$filename" .txt)" "yes"
    fi
done
