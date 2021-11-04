#!/bin/bash
set -ex

if [ "$source_image" == "" ]; then
    echo "Error: Please provide the source image's path"
    exit 1
fi

if [ "$output_path" == "" ]; then
    output_path="$source_image"
fi

if [ "$left_icon" == "" ] && [ "$right_icon" == "" ]; then
    echo "Error: Please provide at least left or right icon's path"
    exit 1
fi
ls
python3 ./generator.py3 "$source_image" "$left_icon" "$right_icon" "$output_path"

zip "overlayed_images.zip" "$output_path"
cp "overlayed_images.zip" $BITRISE_DEPLOY_DIR/overlayed_images.zip || true
exit 0