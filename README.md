## Structure from Motion Tracker

This is an automated video processing pipeline for blender. It consists of generating the point cloud (`points3D.txt`, `points3d.ply`),
camera track and optionally depth-maps for a given video. It was insipired by polyfjord - https://youtube.com/polyfjord _Autotracker_ work
which does the camera tracking on Windows. This work add depth maps, automates installation of some components on Linux/Ubuntu/Debian
distributions and uses `glomap` for track estimation instead of `colmap`. The colmap is still used for SIFT extraction and pairing, 
but glomap can be 10x faster and typically the result is accurate. Depending on whehter `ceres` is compiled to run gpu the 1000 frames video
can be processed in 2-5min (ceres on gpu) or 20-30mins (ceres on cpu) which is a major speed-up to colmap's 4 hours of processing.


## Topics

* [Basic Camera Track Reconstruction](doc/BasicCameraTrackReconstruction.md) - This page covers the basic track reconstruction using the `src/reconstruct.sh` script
* [Using Depth Maps from Video](doc/VideoDepthMapInstall.md) - Covers the creation of depth maps and usage in blender
* [Gaussian Splatting](doc/GaussianSplatting.md) - Summarizes how to create dense point cloud and how to use it in blender


### Links
 * https://github.com/colmap/colmap
 * https://github.com/colmap/glomap
 * https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer
 * https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html
 * https://github.com/DepthAnything/Depth-Anything-V2
 * https://github.com/graphdeco-inria/gaussian-splatting
