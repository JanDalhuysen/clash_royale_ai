#!/bin/bash

echo "Preparing YOLO dataset folders..."

# Delete existing folders
rm -rf train test valid

# Create main folders and subfolders
mkdir -p train/images train/labels
mkdir -p test/images test/labels
mkdir -p valid/images valid/labels

# Copy images to all sets
# cp -r images_to_label/* train/images/
# cp -r images_to_label/* test/images/
# cp -r images_to_label/* valid/images/

# Copy labels to all sets
# cp -r labels/* train/labels/
# cp -r labels/* test/labels/
# cp -r labels/* valid/labels/

echo "Done!"
