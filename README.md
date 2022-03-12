# SLIC
#### Simple Linear Iterative Clustering ([Paper](https://ieeexplore.ieee.org/document/6205760))

```
usage: python slic.py [-h] [-p PATH] [-s S] [-n NUM] [-t THRESHOLD]

optional arguments:                                                                                                   
    -h, --help                                            show this help message and exit
    -p PATH, --path PATH                                  Image to run SLIC on
    -s S, --S S                                           Superpixel Size
    -n NUM, --num NUM                                     Number of Superpixel (Used to compute S, if S is not provided)
    -t THRESHOLD, --threshold THRESHOLD                   Residual error min threshold (Breaking condition)
    -o OUTPUT, --output OUTPUT                            Path to write output image
```  
  
  
Output from running `python slic.py -p images/lena_color_512.jpg -s 15`-
Original            |  Segmented
:-------------------------:|:-------------------------:
![lena_color_512](https://user-images.githubusercontent.com/45385843/158006248-2431594a-0b56-416b-a7da-6e864e5911db.jpg)|![out](https://user-images.githubusercontent.com/45385843/158006246-bbef6fe7-bb97-415e-977d-94de7a32ab3c.png)



### TODOs

- [x] SLIC on pixels `SLIC.py`
- [ ] SLIC on voxels (video) (New code file `video_SLIC.py` using `voxel` class from `feature.py`)
- [ ] Add visualisation function for video SLIC (in `visualisation.py` - check paper for an example)
- [x] Code to move pixel to lowest gradient position in 3x3 neighbourhood
- [ ] Connectivity enforcing postprocessing step (For both image, video SLIC)
- [ ] Trackbar based display (Low priority)
- [ ] Check code for errors


> Requirements - tqdm, opencv, numpy, argparse, copy - Install from package manager  

> Part of Term Project for EC69502: Image Processing Lab, IIT Kharagpur
