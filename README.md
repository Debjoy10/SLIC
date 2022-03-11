# SLIC
### Simple Linear Iterative Clustering ([Paper](https://ieeexplore.ieee.org/document/6205760))

```
usage: python slic.py [-h] [-p PATH] [-s S] [-n NUM] [-t THRESHOLD]

optional arguments:                                                                                                   
    -h, --help                                            show this help message and exit
    -p PATH, --path PATH                                  Image to run SLIC on
    -s S, --S S                                           Superpixel Size
    -n NUM, --num NUM                                     Number of Superpixel (Used to compute S, if S is not provided)
    -t THRESHOLD, --threshold THRESHOLD                   Residual error min threshold (Breaking condition)
```

Original            |  Segmented
:-------------------------:|:-------------------------:
![m](https://user-images.githubusercontent.com/45385843/157873347-c9f8ab66-1003-4474-b01d-76a5fdc6fec8.png)|![image_screenshot_11 03 2022](https://user-images.githubusercontent.com/45385843/157872406-f8a67b26-3b3f-46e9-a601-ff87cfb1b8cb.png)


### TODOs

- [x] SLIC on pixels `SLIC.py`
- [ ] SLIC on voxels (video) (New code file `video_SLIC.py` using `voxel` class from `feature.py`)
- [ ] Add visualisation function for video SLIC (in `visualisation.py` - check paper for an example)
- [ ] Code to move pixel to lowest gradient position in 3x3 neighbourhood (Edit function `min_grad_center()` in `SLIC.py`)
- [ ] Connectivity enforcing postprocessing step (For both image, video SLIC)
- [ ] Trackbar based display (Low priority)
- [ ] Check code for errors


> Requirements - tqdm, opencv, numpy - Install from package manager  

> Part of Term Project for EC69502: Image Processing Lab, IIT Kharagpur
