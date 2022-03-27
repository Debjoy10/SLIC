# SLIC
#### Simple Linear Iterative Clustering ([Paper](https://ieeexplore.ieee.org/document/6205760))

##### Pixel-SLIC
```
usage: python slic.py [-h] [-p PATH] [-s S [S ...]] [-r] [-n NUM] [-t THRESHOLD] [-o OUTPUT]

optional arguments:                                                                                                   
    -h, --help                                            show this help message and exit
    -p PATH, --path PATH                                  Image to run SLIC on
    -s S [S ...], --S S [S ...]                           Superpixel Size (s or (sx sy))
    -r, --rect                                            Allow/use rectangular superpixel
    -n NUM, --num NUM                                     Number of Superpixel (Used to compute S, if S is not provided)
    -t THRESHOLD, --threshold THRESHOLD                   Residual error threshold (Breaking condition)
    -o OUTPUT, --output OUTPUT                            Path to write outputs
```  
  
##### Voxel-SLIC
```
usage: python slic_voxels.py [-h] [-p PATH] [-s S [S ...]] [-r] [-n NUM] [-t THRESHOLD] [-o OUTPUT] [-c]

optional arguments:
  -h, --help                                              show this help message and exit
  -p PATH, --path PATH                                    Video to run SLIC on
  -s S [S ...], --S S [S ...]                             Superpixel Size (s or (sx sy))
  -r, --rect                                              Allow/use rectangular superpixel
  -n NUM, --num NUM                                       Number of Superpixel
  -t THRESHOLD, --threshold THRESHOLD                     Residual error threshold
  -o OUTPUT, --output OUTPUT                              Path to write outputs
  -c, --plt_surface                                       If true plot the surface plot of the output
```
  
##### Stereo-Voxel-SLIC
```
usage: python slic_stereo_voxels.py [-h] [-p PATH] [-s S [S ...]] [-r] [-n NUM] [-t THRESHOLD] [-o OUTPUT]

optional arguments:
  -h, --help                                              show this help message and exit
  -p PATH, --path PATH                                    Video to run SLIC on
  -s S [S ...], --S S [S ...]                             Superpixel Size (s or (sx sy))
  -r, --rect                                              Allow/use rectangular superpixel
  -n NUM, --num NUM                                       Number of Superpixel
  -t THRESHOLD, --threshold THRESHOLD                     Residual error threshold
  -o OUTPUT, --output OUTPUT                              Path to write outputs
```  


Output from running `python slic.py -p images/lena_color_512.jpg -s 15`
Original            |  Segmented
:-------------------------:|:-------------------------:
![lena_color_512](https://user-images.githubusercontent.com/45385843/158006248-2431594a-0b56-416b-a7da-6e864e5911db.jpg)|![out](https://user-images.githubusercontent.com/45385843/158006246-bbef6fe7-bb97-415e-977d-94de7a32ab3c.png)  

Output from running `python slic.py -p images/hdimg.jpg -r`
Original            |  Segmented
:-------------------------:|:-------------------------:
![hdimg](https://user-images.githubusercontent.com/45385843/158521830-464fc085-524c-4b74-a96a-681cc844825c.jpg)|![out](https://user-images.githubusercontent.com/45385843/158521850-f496af46-23ff-473a-9aa6-a751e25d63f0.png)  

Output from running `python slic_voxels.py -p images/flag_low_res.mp4` [(Link)](https://drive.google.com/file/d/1xPH3tyflk46rzR5bzvqk1n0nIttj9J4X/view?usp=sharing)  

Output from running ` python slic_stereo_voxels.py -p ../sintelLF/ambushfight_1/` [(Link)](https://drive.google.com/file/d/1BTp1j2M9MweIZx-lTYq9zxzEZ4YaGZf3/view?usp=sharing)

### TODOs

- [x] SLIC on pixels `SLIC.py`
- [x] SLIC on voxels (video) (New code file `video_SLIC.py` using `voxel` class from `feature.py`)
- [x] Add visualisation function for video SLIC (in `visualisation.py` - check paper for an example)
- [x] Code to move pixel to lowest gradient position in 3x3 neighbourhood
- [x] Connectivity enforcing postprocessing step (For all SLICs)
- [x] Add Stereo-video-SLIC code
- [x] Add support for allowing rectangular superpixels
- [ ] Add inter-cluster tracking for video/stereo
- [ ] Trackbar based display
- [x] Check code for errors

> Requirements - tqdm, opencv, numpy, argparse, copy - Install from package manager  

> Part of Term Project for EC69502: Image Processing Lab, IIT Kharagpur
