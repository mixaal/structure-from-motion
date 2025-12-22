## Alternative Approach to Obtain Depth Maps

In this directory there are 3 scripts that can be used to obtain depth maps for images:

* `depthmap.py` - creates depth maps for each image individually
* `normalize_depthmaps.py` - scans all depth maps created above and normalizes (_stretches_) the map range into global min/max depth values
* `temporal_smoothing.py` - uses _sliding window_ to achive more smooth transitions between images

The issue with single image depth maps extraction is that there is no video context, so single image depth maps _flicker_, i.e. inconsitent values
are extracted, scripts above try to mitigate this issue but _video aware_ models are recommended. The above approach can be still used 
in stream-like robotics environments, but for real video processing Depth Anything NN is advisable.
