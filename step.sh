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

# curl -sSL "${script_url}" | bash
echo "Running Image Generator"
echo "Source Image(s): ${source_image}"
echo "Left icon: ${left_icon}"
echo "Right icon: ${right_icon}"
echo "Output path: ${output_path}"

pip install Pillow
python3 "$(dirname $0)/generator.py3" "$source_image" "$left_icon" "$right_icon" "$output_path" || error_exit "Python file not found."

zip "overlayed_images.zip" "$output_path"
cp "overlayed_images.zip" "$BITRISE_DEPLOY_DIR/overlayed_images.zip"
exit 0