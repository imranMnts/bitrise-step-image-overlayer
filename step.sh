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

mkdir "image_overlayer_results" || true

if [ "${output_path: -1}" == "/" ]; then
    output_path_without_slash=${output_path%?}
    output_name=$(basename $output_path_without_slash)

    cp -r "$output_path_without_slash" "image_overlayer_results"
else
    cp -r "$output_path" "image_overlayer_results"
fi

if [ "$export_results" == "True" ]; then
    if [ "$archive_result" == "True" ]; then
        zip -r "image_overlayer_results.zip" "image_overlayer_results"    
        cp "image_overlayer_results.zip" "$BITRISE_DEPLOY_DIR/image_overlayer_results.zip"
    else 
        cp "image_overlayer_results" "$BITRISE_DEPLOY_DIR/image_overlayer_results"
    fi
fi

exit 0