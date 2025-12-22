#!/bin/bash -xe

# 1 - use gpu, 0 don't use gpu
USE_GPU=1

export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia

D=$(dirname $0)
VIDEOS="$D/Videos"
SCENES="$D/Scenes"

FFMPEG=/usr/bin/ffmpeg
COLMAP=/usr/bin/colmap
GLOMAP="$HOME/opt/glomap/bin/glomap"

for video in $VIDEOS/*.{mp4,avi,mov,mkv}; do
  [ -f $video ] || continue
  video_base=$(basename $video)
  process_dir="$SCENES/$video_base"
  images_dir="$process_dir/images"
  scene_db="$process_dir/database.db"
  sparse_dir="$process_dir/Sparse"
  [ -d "$process_dir" ] || {
    echo "Processing video $video ---> $process_dir ..."
    mkdir -p "$process_dir"
  }
  [ -d $images_dir ] || {
    echo "   ---> Extracting images from video ... "
    mkdir -p "$images_dir"
    $FFMPEG -loglevel error -stats -i "$video" -qscale:v 2 "$images_dir/frame_%06d.jpg"
    cd $process_dir
    ln -s images/*.jpg .
    cd -
  }
  [ -f "$scene_db" ] || {
    echo "   ---> Extracting SIFT from images ... "
    $COLMAP feature_extractor \
    --database_path "$scene_db" \
    --image_path    "$images_dir" \
    --ImageReader.single_camera 1 \
    --SiftExtraction.use_gpu $USE_GPU \
    --SiftExtraction.max_image_size 4096

    echo "   ---> Running sequential matcher ... "
    $COLMAP sequential_matcher \
    --database_path "$scene_db" \
    --SiftMatching.use_gpu $USE_GPU \
    --SequentialMatching.overlap 15

  }
  [ -d "$sparse_dir/0" ] || {
    echo "   ---> Running sparse reconstruction using glomap ... "
    $GLOMAP mapper \
    --database_path "$scene_db" \
    --image_path    "$images_dir" \
    --output_path   "$sparse_dir" \
    --skip_retriangulation 1

  }
  [ -f "$sparse_dir/points3D.txt" ] || {
    echo "   ---> Exporting model for blender ... "
    $COLMAP model_converter \
        --input_path  "$sparse_dir/0" \
        --output_path "$sparse_dir" \
        --output_type TXT 
  }
  [ -f "$sparse_dir/points3D.ply" ] || {
    $COLMAP model_converter \
        --input_path  "$sparse_dir/0" \
        --output_path "$sparse_dir/points3D.ply" \
        --output_type PLY
  }


done
