from transformers import pipeline
from PIL import Image
import numpy as np
import os
from pathlib import Path
from tqdm import tqdm

# Load pipeline
pipe = pipeline(task='depth-estimation', model='depth-anything/Depth-Anything-V2-Large-hf', device=0)

os.makedirs('depth_maps', exist_ok=True)

# Collect all image paths (just paths, not loaded images)
image_files = [f for f in os.listdir('images/') 
               if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# Batch process
batch_size = 16  # Adjust based on your GPU memory

for i in tqdm(range(0, len(image_files), batch_size)):
    batch_files = image_files[i:i+batch_size]
    
    # Load batch images (only load what we need)
    batch_images = [Image.open(f'images/{f}') for f in batch_files]
    
    # Process batch
    results = pipe(batch_images)
    
    # Save and close
    for img_file, result, img in zip(batch_files, results, batch_images):
        depth_array = np.array(result['depth'])
        depth_16bit = (depth_array / depth_array.max() * 65535).astype(np.uint16)
        
        output_name = Path(img_file).stem + '_depth.png'
        Image.fromarray(depth_16bit).save(f'depth_maps/{output_name}')
        img.close()  # Close file handle

print(f'Processed {len(image_files)} images')

#from transformers import pipeline
#from PIL import Image
#import numpy as np
#import os
#from pathlib import Path
#
#pipe = pipeline(task='depth-estimation', model='depth-anything/Depth-Anything-V2-Large-hf')
#
#for img_path in os.listdir('images/'):
#    if img_path.lower().endswith(('.jpg', '.png', '.jpeg')):
#        image = Image.open(f'images/{img_path}')
#        depth = pipe(image)['depth']
#        
#        # Save as 16-bit PNG (change extension to .png)
#        depth_array = np.array(depth)
#        depth_16bit = (depth_array / depth_array.max() * 65535).astype(np.uint16)
#
#        # Force PNG extension
#        output_name = Path(img_path).stem + '_depth.png'
#        Image.fromarray(depth_16bit).save(f'depth_maps/{output_name}')
#        print(f'Processed {img_path}')
