# Advanced Lane Finding

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./test_images/test1.jpg "Original Road Image"
[image2]: ./output_images/test1-undistorted.jpg "Image with distortion removed"
[image3]: ./output_images/test1-threshold.jpg "Image with Threshold"
[image4]: ./output_images/test1-topview.jpg "Top view"
[image5]: ./output_images/lane-finding-final.png "Final Image Tracking"
[video1]: ./project_result.mp4 "Project Video Result"
[video2]: ./challenge_result.mp4 "Challenge Video Result"

# Code Overview

The main pipeline implementation is found in the `advanced-line-detection.py` file,
where the steps of the pipeline are implemented, including the camera calibration.

This script can be run using `python3` and takes two parameters:

1. Name of the video file to used as input.
2. Name of the video file in which the result is saved.

It can be used as follows:

```sh
python3 advanced-lane-detection.py project_video.mp4 project_result.mp4
```

The implementation of the individual steps of the pipeline are imported from the following files:

* `calibration.py`: camera calibration functions
* `transform.py`: perspective warping functions
* `threshold.py`: thresholding of lanes
* `lanefind.py`: lane finding function, polynomial curve fitting and radius calculation
* `video.py`: utility functions for the video processing

Each of these scripts includes a standalone test which can be used manually run some unit tests
when making code updates.

Finally a `Makefile` is provided to run tests of individual functions on the images found
under the `test_images` directory.

## Pipeline (single images)

To illustrate the individual steps in the pipeline we will show here the various steps involved
and are illustrated in this README using the following original test image.

![original image][image1]

The result of the various algorithms for other test images can be found under the `output_images`
for those who are curious :-).

### Correction of Distortion

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:

![undistorted image][image2]

In the implementation of the pipeline this step occurs after the thresholding, but to ease visual
verification of the distortion correction this step is illustrated first.

### Thresholding

The thresholding algorithm used is OpenCV's Gaussian adpative thresholding which is doing threshold
against the local mean, rather than use a global static threshold value that would not work
in all lighting condition.

Prior to thresholding the image a blur is run to reduce the noise in the image.

In order to improve the quality of the lane detection this code relies on the following three observations:

* White lines can be detected by using just the red channel in RGB color space.
* Yellow lines can be detected by using just the blue channel in RBG color space.
* All types of lines can be detected using the S channel in HLS color space.

So in order to leverage these three facts the three are combined and the thresholding algorithm is run on
this combination (see the following code in `threshold.py`:

```python
def threshold_image(image):
    # Blur the image
    kernel_size = 3
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    R = blurred[:,:,1] # Good for white lines.
    B = blurred[:,:,1] # Good for yellow lines.
    RB = cv2.addWeighted(R, 0.5, B, 0.5, 0.0)

    # Extract the S channel.
    hls = cv2.cvtColor(blurred, cv2.COLOR_RGB2HLS)
    S = hls[:,:,2]

    # Run an adaptive Gaussian threshold on the combination of S and R+B.
    binary = cv2.adaptiveThreshold(cv2.addWeighted(S, 0.5, RB, 0.5, 0.0),\
                                   255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY, 33, -10)
    return binary

```

Here's an example of the output for this step:

![image afer thresholding][image3]

### Top View

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 585, 460      | 320, 0        | 
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

### Lane finding

All the lane finding code is found in `lanefind.py`, and is invoked from the main pipeline.

![alt text][image5]

## Pipeline (video)

Both the project video and the challenge video have been processed
and the algorithm implemented delivered satisfying results on both
of them.

Results when applied on the project video:

* [project video result][video1]

Results when applied on the challenge video:

* [challenge video result][video2]


## Discussion

...
