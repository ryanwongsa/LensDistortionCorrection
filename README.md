# Lens Distortion Correction using a Single Image

## Requirements

- OpenCV3
- Python2.7
- Numpy

## Method

The program was divided into two sections. The first section involves undistorting an image using a camera calibration technique and OpenCVs built in undistortion method. The second section involves identifying features (corners) to be used for camera calibration.
This approach was chosen as it requires a similar method to camera calibration techniques using multiple images and a chessboard grid. The main differences are that there was only one image provided and a chessboard grid was not available on the image. Therefore new features (corners) which were similar to the chessboard grid would need to be found for camera calibration.

## Determining Features using the Grid in the Image

The board on the image contained a regular grid of rectangles which had an aspect ratio of approximately 2:1. An assumption was therefore made that two vertically aligned rectangles would make a square.

![Square Example](/imgSrc/squareExample.png?raw=true "Example Square")

This was used to "simulate" a chessboard's corner features by following a sequence of sub algorithms briefly highlighted below:
- Edge Detection (used to remove noise)
- Parallel Horizontal / Vertical Square Side Detection (used to determine intervals for squares)
- Contour Following (used to find when the rectangular blocks ended)
- Corner Correction (used in the case were the edge detection algorithm was underperforming)
- Symmetric Feature (Corner) Assignment (method to speed up algorithm / not required if previous algorithms are applied to all quadrants)

The one requirement of the user is to input the camera's central focus point which enables for good for contour following and side detection. An assumption was made whereby if the image was divided into 4 quadrants around the focus point then the distortions are symmetric.

![Board Example](/imgSrc/boardExample.png?raw=true "Example Grid Board")

## Code Files

### featureExtraction.py
* INPUT    `> python featureExtraction.py images/fisheye.jpg`
  * `images/fisheye.jpg` - is the original distorted image
* OUTPUT 
  * features.txt (contains the corner features to be used by CorrectImageLensDistortion)
  * text containing the grid dimensions used for CorrectImageLensDistortion.py
  * results/edge.jpg (contains edge detected image)

### CorrectImageLensDistortion.py
* INPUT    `> python CorrectImageLensDistortion.py images/fisheye.jpg 9 5 features.txt 0.5`
  * `images/fisheye.jpg` - is the original distorted image
  * `9 5` - are the number of grid corners available
  * `features.txt` - is the file containing the features / corner locations
  * `0.5` - zoom factor (due to OpenCV undistortion methods cropping images adjusting this will allow for greater image size and view but also introduce areas of the image whereby undistortion was not correctly found) [setting to 0 will show area with most undistortion of the image].

* OUTPUT 
  * results/boardDrawn.jpg (contains image with grid of corners identified)
  * results/resultImage.jpg (contains undistorted image)

## How To Run

```
1. python featureExtraction.py images/fisheye.jpg
2. python CorrectImageLensDistortion.py images/fisheye.jpg 9 5 features.txt 0
```

## Potential Improvements
- Refine Edge Detection to eliminate glare issue to allow for more grid corners to be located
- Allow for automatic detection of central focus point
- Improve robustness if the board is placed at an angle
- Corner Correction could have used a quadratic equation instead of linear equation to assign corrected points
- Possible use of the fisheye calibration opencv library (at the time documentation was limited to C++) to fix problems whereby outside of the grid feature area is heavily distorted
![Glare Example](/imgSrc/glareExample.png?raw=true "Example Glare")

## Examples

Example results are found in the examples folder where some hand designed corner features are used too.

1. 	
```
	python featureExtraction.py images/fisheye.jpg
	python CorrectImageLensDistortion.py images/fisheye.jpg 9 5 features.txt 0
```
2. 
```
python CorrectImageLensDistortion.py images/fisheye.jpg 19 8 manual_features/handmadefeatures_v2.txt 0.6
```
3.
```
python CorrectImageLensDistortion.py images/fisheye.jpg 11 7 manual_features/handmadefeatures.txt 0
```