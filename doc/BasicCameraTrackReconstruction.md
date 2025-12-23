# Camera Track Reconstruction

By using `src/reconstruct.sh` we create the colmap-like folder structure under the `Scenes/<movie>` directory. This can be imported into blender
using blender photogrammetry plugin. 

### Installation

Before running the `src/reconstruct.sh` script, install all the dependencies and `glomap` itself:
```bash
./glomap-build.sh
```

This will install necessary components as `colmap` and also builds `glomap` and installs it into `$HOME/opt/glomap` so it's usable as 
`$HOME/opt/glomap/bin/glomap`.

### Video Processing Folder Structure

* `Videos` - videos to be processed, already processed videos are skipped
* `Scenes` - scenes from processed videos, to be imported into blender

### Reconstructing Scene from Video

When you run `src/reconstruct.sh` it scans the video directory and creates the corresponding scene, the result looks like this:
```bash
ls -l Scenes/20251202_130635.mp4/sparse/
total 361796
drwxrwxr-x 2 mikc mikc      4096 Dec 21 20:17 0
-rw-rw-r-- 1 mikc mikc       189 Dec 21 20:22 cameras.txt
-rw-rw-r-- 1 mikc mikc 346423186 Dec 21 20:22 images.txt
-rw-rw-r-- 1 mikc mikc    996479 Dec 21 20:50 points3D.ply
-rw-rw-r-- 1 mikc mikc  23040159 Dec 21 20:22 points3D.txt
```


## Colmap Addon Installation

See [Addon Installation](BlenderAddonAndImporting.md)

Optionally, depth maps can be created using `video_depth.py` python script, this script creates `depth_maps_video` folder
with 16bit depth map png images. These can be used in blender. For more details refer to the [Video Maps Usage and Installation](VideoDepthMapInstall.md)



