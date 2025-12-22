import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm
import os

# Find global min/max across all depth maps
print("Computing global depth range...")
global_min = float('inf')
global_max = float('-inf')

depth_files = sorted(Path('depth_maps').glob('*.png'))

for depth_file in tqdm(depth_files):
    depth = np.array(Image.open(depth_file))
    global_min = min(global_min, depth.min())
    global_max = max(global_max, depth.max())

print(f"Global range: {global_min} - {global_max}")

# Re-normalize all depth maps
os.makedirs('depth_maps_normalized', exist_ok=True)

for depth_file in tqdm(depth_files):
    depth = np.array(Image.open(depth_file)).astype(np.float32)
    
    # Normalize to global range
    depth_normalized = (depth - global_min) / (global_max - global_min) * 65535
    depth_normalized = depth_normalized.astype(np.uint16)
    
    Image.fromarray(depth_normalized).save(f'depth_maps_normalized/{depth_file.name}')
