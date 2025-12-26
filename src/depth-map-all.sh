#!/bin/bash -e

CURR_PFX=$(conda info --json |jq .active_prefix_name)

if [ "$CURR_PFX" = '"base"' ]; then
  cat <<EOH
  Please use:

    conda activate <your env for video depth>, e.g."
    conda activate video-depth"

  To list all available environments:
    conda info --envs
EOH
  exit 1
fi


D=$(dirname $0)
SCENES="$D/../Scenes"

for d in $SCENES/*; do
  [ -d "$d" ] || continue
  [ -d "$d/depth_maps_video" ] || {
    echo "Creating depth maps for $d ... "
    python "$D/video_depth.py" "$d"
  }
done
