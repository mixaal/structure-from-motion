import numpy as np
from PIL import Image
from pathlib import Path
from scipy.ndimage import uniform_filter1d
from tqdm import tqdm

# Load all depth maps with progress
depth_files = sorted(Path('depth_maps').glob('*.png'))
print(f"Loading {len(depth_files)} depth maps...")
depths = np.stack([np.array(Image.open(f)) for f in tqdm(depth_files, desc="Loading")])

# Temporal smoothing
print("Applying temporal smoothing...")
window_size = 5  # Smooth over 5 frames
smoothed = uniform_filter1d(depths.astype(np.float32), size=window_size, axis=0, mode='nearest')

# Save smoothed versions
Path('depth_maps_smooth').mkdir(exist_ok=True)
for i, depth_file in tqdm(enumerate(depth_files), total=len(depth_files), desc="Saving"):
    Image.fromarray(smoothed[i].astype(np.uint16)).save(f'depth_maps_smooth/{depth_file.name}')

print("Done!")
