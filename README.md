# SLIC
#### Simple Linear Iterative Clustering ([Paper](https://ieeexplore.ieee.org/document/6205760))
  
##### Install Dependencies
```
pip install -r requirements.txt
```
  
##### Pixel-SLIC
```
usage: python slic.py [-h] [-p PATH] [-s S [S ...]] [-r] [-n NUM] [-t THRESHOLD] [-o OUTPUT] [-dp]

optional arguments:                                                                                                   
    -h, --help                                            show this help message and exit
    -p PATH, --path PATH                                  Image to run SLIC on
    -s S [S ...], --S S [S ...]                           Superpixel Size (s or (sx sy))
    -r, --rect                                            Allow/use rectangular superpixel
    -n NUM, --num NUM                                     Number of Superpixel (Used to compute S, if S is not provided)
    -t THRESHOLD, --threshold THRESHOLD                   Residual error threshold (Breaking condition)
    -o OUTPUT, --output OUTPUT                            Path to write outputs
    -dp, --disable_postprocessing                         Disable Postprocessing of the output clusters
```  
  
##### Voxel-SLIC
```
usage: python slic_voxels.py [-h] [-p PATH] [-s S [S ...]] [-r] [-n NUM] [-t THRESHOLD] [-o OUTPUT] [-c] [-dp]

optional arguments:
  -h, --help                                              show this help message and exit
  -p PATH, --path PATH                                    Video to run SLIC on
  -s S [S ...], --S S [S ...]                             Superpixel Size (s or (sx sy))
  -r, --rect                                              Allow/use rectangular superpixel
  -n NUM, --num NUM                                       Number of Superpixel
  -t THRESHOLD, --threshold THRESHOLD                     Residual error threshold
  -o OUTPUT, --output OUTPUT                              Path to write outputs
  -c, --plt_surface                                       If true plot the surface plot of the output
  -dp, --disable_postprocessing                           Disable Postprocessing of the output clusters
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
![lena_color_512](https://user-images.githubusercontent.com/45385843/158006248-2431594a-0b56-416b-a7da-6e864e5911db.jpg)|![out](https://user-images.githubusercontent.com/45385843/161009662-786b6655-febc-4608-bbd8-e358e4f0f231.png)

Output from running `python slic.py -p images/hdimg.jpg -r`
Original            |  Segmented
:-------------------------:|:-------------------------:
![hdimg](https://user-images.githubusercontent.com/45385843/158521830-464fc085-524c-4b74-a96a-681cc844825c.jpg)|![out](https://user-images.githubusercontent.com/45385843/161009949-a99d1aa5-86d4-4792-ba29-57dd250b7eba.png)

Output from running `python slic_voxels.py -p images/flag_low_res.mp4` [(Link)](https://iitkgpacin-my.sharepoint.com/:v:/g/personal/sahadebjoy10_iitkgp_ac_in/EcpYcWMpcbZImawx9qFcPKUBAsPfeTV7cepuQgbqaIFDVw?e=HNktzO)  

Output from running ` python slic_stereo_voxels.py -p ../sintelLF/ambushfight_1/` [(Link)](https://iitkgpacin-my.sharepoint.com/:v:/g/personal/sahadebjoy10_iitkgp_ac_in/Ecfijn58M8dEsTyd9kosbSAB0pQJmm8XLOc3yAwA8T8TBg?e=3SPpKo)

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

> Part of Term Project for EC69502: Image Processing Lab, IIT Kharagpur
