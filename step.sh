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
    echo "Error: Please provide at least left or right icon's path/text"
    exit 1
fi

# curl -sSL "${script_url}" | bash
echo "Running Image Generator"

pip3 install Pillow
python3 "$(dirname $0)/generator.py3" "$(dirname $0)" "$source_image" "$left_icon" "$right_icon" "$output_path" "$text_color" "$center_icon"

if [ "${output_path: -1}" == "/" ]; then
    output_path_without_slash=${output_path%?}
    zip "$output_path_without_slash.zip" "$output_path"
    cp "$output_path.zip" "$BITRISE_DEPLOY_DIR/$output_path.zip"
else
    cp "$output_path" "$BITRISE_DEPLOY_DIR/$output_path"
fi
exit 0