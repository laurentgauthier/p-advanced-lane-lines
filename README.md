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

The main pipeline implementation is found in the `advanced-lane-detection.py` file,
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
* `threshold.py`: thresholding of lanes
* `transform.py`: perspective warping functions
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

So in order to leverage these three facts the three channels are summed and the thresholding algorithm
is run on this combination (see the use of `cv2.addWeighted` in the following code in `threshold.py`):

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

The code for perspective transform is found in `transform.py` and uses OpenCV functions to
create a Bird's Eye view of the road in front of the car.

```python
def compute_transform_matrices():
    # This is the rectangle I measured on an undistored image from the video
    # where the lanes lines are pretty much centered and straight.
    bottom_left  = (190, 720)
    top_left     = (587, 455)
    top_right    = (703, 455)
    bottom_right = (1130, 720)

    # Location of the rectangle in the original undistorted image.
    src = np.float32([ top_left, top_right, bottom_right, bottom_left ])

    # Leave a margin on the left and right of the top view, making the top-view a 720x720.
    margin = 280
    dst = np.float32([
        [margin,               0],
        [image_size[1]-margin, 0], 
        [image_size[1]-margin, image_size[0]], 
        [margin,               image_size[0]],
    ])

    # Compute the transform matrix and the inverse transform matrix.
    transformMatrix       = cv2.getPerspectiveTransform(src, dst)
    inverseTranformMatrix = cv2.getPerspectiveTransform(dst, src)

    return transformMatrix, inverseTranformMatrix
```

This was verified by using the perspective transform on test images showing a piece of
straight road and checking that the lanes appear parallel in the warped image.

Here is the ouput for our test image (shown without thresholding):

![alt text][image4]

### Lane finding

All the lane finding code is found in `lanefind.py`, and is invoked from the main pipeline.

It does in one step fit a polynomial curve for each lane (left and right), compute the radius
on each side.

The code for lane detection return an image (Bird's Eye view) coloring the detected lane space.

The code in `advance-lane-detection.py` (main pipeline implementation) then applies the
inverse perspective transform and overlays it on top of the original image resulting in the
following type of output:

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

This code works nicely on both the project and challenge video, but it does fail miserably on
the harder challenge video.

Here are some thoughts on what could be done to improve the quality of the lane tracking.

Not all these ideas require software changes, as some could be implemented as physical changes.

### Tracking in sharp turns

When the car is going through sharp turns the left and/or right line can come out sight of the
camera at times.

The software should be improved to handle these cases, and more generally should be improved
to provide a more robust reponse for the cases when the road marking can be partially missing.

### Image stabilization

In experiments I created a number of Bird's Eye view video for debugging purpose and it was
quite visible that the lanes were wobbly mostly due to the vehicle suspension rocking forward
and backward.

Some form of image stabilization using either a pyshical gimbal or some form of software stabilization
could be important to create a more robust lane tracking algorithm when such adverse lighting
conditions occur.

### Reflection on the windshield

In the harder challenge video the thresholding algorithm is sometimes disrupted by the challenging
lighting conditions.

While some software changes and smarter tuning of thresholding parameters could probably be done
there is at least one issue that would require physical changes to the in-car video capture system.

The camera should be located and encased in such a way that there are no reflecting on the windshield
introducing avoidable artefacts in the image.

### Sensor Fusion

Using for example of data from the vehicle odometry and wheels position in addition to the
video images would allow the creation of a more robust lane tracking system, especially in situations
where even the human eye would have trouble tracking the lanes.
