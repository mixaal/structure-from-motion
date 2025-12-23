import torch
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm
from depth_anything_v2.dpt import DepthAnythingV2
import os
import sys

wd = "./"
# Dir is the first argument
try:
    wd = sys.argv[1]
except Exception as e:
    print("Usage: python video_depth.py <scene direcotry with images>")
    exit(-1)

# Load model
model = DepthAnythingV2(encoder='vitl', features=256, out_channels=[256, 512, 1024, 1024])
model.load_state_dict(torch.load('checkpoints/depth_anything_v2_vitl.pth'))
model = model.to('cuda').eval()

# Chdir to the scene directory
os.chdir(wd)

# Process video frames
image_files = sorted(Path('images').glob('*.jpg'))
Path('depth_maps_video').mkdir(exist_ok=True)

for img_file in tqdm(image_files):
    img = cv2.imread(str(img_file))
    depth = model.infer_image(img)
    
    # Normalize to 16-bit
    depth_16bit = (depth / depth.max() * 65535).astype(np.uint16)
    #cv2.imwrite(f'depth_maps_video/{img_file.stem}_depth.png', depth_16bit)
    cv2.imwrite(f'depth_maps_video/{img_file.stem}.png', depth_16bit)
