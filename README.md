## Structure from Motion Tracker

This is an automated video processing pipeline for blender. It consists of generating the point cloud (`point3D.txt`, `point3d.ply`),
camera track and optionally depth-maps for a given video. It was insipired by polyfjord - https://youtube.com/polyfjord _Autotracker_ work
which does the camera tracking on Windows. This work add depth maps, automates installation of some components on Linux/Ubuntu/Debian
distributions and uses `glomap` for track estimation instead of `colmap`. The colmap is still used for SIFT extraction and pairing, 
but glomap can be 10x faster and typically the result is accurate. Depending on whehter `ceres` is compiled to run gpu the 1000 frames video
can be processed in 2-5min (ceres on gpu) or 20-30mins (ceres on cpu) which is a major speed-up to colmap's 4 hours of processing.

### Folder Structure

* `Videos` - videos to be processed, already processed videos are skipped
* `Scenes` - scenes from processed videos, to be imported into blender

### Reconstructing Scene from Video

When you run `reconstruct.sh` it scans the video directory and creates the corresponding scene, the result looks like this:
```bash
ls -l Scenes/20251202_130635.mp4/Sparse/
total 361796
drwxrwxr-x 2 mikc mikc      4096 Dec 21 20:17 0
-rw-rw-r-- 1 mikc mikc       189 Dec 21 20:22 cameras.txt
-rw-rw-r-- 1 mikc mikc 346423186 Dec 21 20:22 images.txt
-rw-rw-r-- 1 mikc mikc    996479 Dec 21 20:50 points3D.ply
-rw-rw-r-- 1 mikc mikc  23040159 Dec 21 20:22 points3D.txt
```

This folder can be imported in bledner using `photogrammetry_importer.zip` plugin:

* https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer

as Menu > Import > Colmap

Optionally, depth maps can be created using `video_depth.py` python script, this script creates `depth_maps_video` folder
with 16bit depth map png images. These can be used in blender. Here is an example of source color image and it's corresponding
depth map:
![Source RGB Image](doc/frame_000013.jpg)
![Depth Image](doc/frame_000013_depth.png)


### Installation
First, install the basics and glomap:
```bash
./glomap-build.sh
```

This will install necessary components as `colmap` and also builds `glomap` and installs it into `$HOME/opt/glomap` so it's usable as 
`$HOME/opt/glomap/bin/glomap`.

### Video-Depth Maps Installation

Create conda environment and install `depth-anything-v2`:

```bash
conda create -n video-depth python=3.12 -y
conda activate video-depth
pip install depth-anything-v2
pip install diffusers transformers accelerate
```

Now it's time  to verify that `pytorch` works with your graphics card:
```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.get_arch_list()); print(torch.randn(1).cuda())"
```

should output something like this:
```
2.9.1+cu128
['sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90', 'sm_100', 'sm_120']
tensor([0.4232], device='cuda:0')
```

Sometimes, if the graphics card is too new for some version of `nvcc` and `pytorch`, different output can be seen, e.g.:
```
NVIDIA GeForce RTX 5050 Laptop GPU with CUDA capability sm_120 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_50 sm_60 sm_70 sm_75 sm_80 sm_86 sm_90.
If you want to use the NVIDIA GeForce RTX 5050 Laptop GPU GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/

```

In that case we need to make sure that both  `nvacc` and `pytorch` support the architecture. Example for nvcc:
```bash
nvcc --version
nvcc --list-gpu-arch
```

Example output: 
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Thu_Mar_28_02:18:24_PDT_2024
Cuda compilation tools, release 12.4, V12.4.131
Build cuda_12.4.r12.4/compiler.34097967_0
compute_50
compute_52
compute_53
compute_60
compute_61
compute_62
compute_70
compute_72
compute_75
compute_80
compute_86
compute_87
compute_89
compute_90
```

Since `compute_120` is not listed above we need to uninstall `pytorch` and  install proper cuda toolkit:
```bash
conda install -c "nvidia/label/cuda-12.8.0" cuda-toolkit
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision # or specify version here
```

Now we should see `nvcc --version` and `nvcc --list-gpu-arch`:
```
compute_75
compute_80
compute_86
compute_87
compute_88
compute_89
compute_90
compute_100
compute_110
compute_103
compute_120
compute_121
```

Let's go back to "verify that pytorch works with gpu" and we should see the `sm_XXX` architecture.

Install the model by downloading it from huggingface:
```bash
mkdir -p checkpoints
cd checkpoints
wget https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth
cd ..
```

Now running:
```bash
conda activate video-depth # unless already inside conda env
python video_depth.py  Scenes/20251202_130635.mp4/
```

will create folder `depth_maps_video/` in the directory where source `images/` are present.


### Links
 * https://github.com/colmap/colmap
 * https://github.com/colmap/glomap
 * https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer
 * https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html
 * https://github.com/DepthAnything/Depth-Anything-V2
