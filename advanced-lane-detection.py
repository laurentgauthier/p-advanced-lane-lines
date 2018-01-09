import video
import calibration
import transform
import threshold
import lanefind
import glob
import sys
import cv2
import numpy as np

input_video_file = sys.argv[1]
output_video_file = sys.argv[2]

# Make a list of calibration images
calibration_images = glob.glob('camera_cal/calibration*.jpg')
mtx, dist = calibration.camera_calibration(calibration_images)

# Compute the perspective transform matrix and its inverse.
transformMatrix, inverseTransformMatrix = transform.compute_transform_matrices()

initial_detection_done = False

def process_frame(image):
    global initial_detection_done

    # Threshold the image.
    binary = threshold.threshold_image(image)

    # Remove the image distortion.
    undistorted = calibration.camera_undistort(binary, mtx, dist)

    # Use the transform matrix to compute the top-view.
    topview = transform.compute_top_view(undistorted, transformMatrix)

    # Find the lanes.
    if not initial_detection_done:
        color_warp, left_curve_radius_m, right_curve_radius_m, car_center_offset_m = lanefind.initial_lane_finding(topview)
        initial_detection_done = True
    else:
        color_warp, left_curve_radius_m, right_curve_radius_m, car_center_offset_m = lanefind.incremental_lane_finding(topview)

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = cv2.warpPerspective(color_warp, inverseTransformMatrix, (image.shape[1], image.shape[0]))

    # Convert the binary image into an RGB image, as the video recording is expecting
    # a color image.
    color_image = cv2.cvtColor(topview, cv2.COLOR_GRAY2RGB)
    # return color_image

    # Combine the result with the original image
    color_undistorted = calibration.camera_undistort(image, mtx, dist)
    result = cv2.addWeighted(color_undistorted, 1, newwarp, 0.3, 0)

    # Add radius and center offset to the final image as text.
    cv2.putText(result, " Curve radius: %1.0f m" % ((left_curve_radius_m+right_curve_radius_m)/2,),  (50, 50), \
                cv2.FONT_HERSHEY_SIMPLEX, 2, [255, 0, 0], 3)
    cv2.putText(result, "Center offset: %1.2f m" % (car_center_offset_m,),  (50, 100), \
                cv2.FONT_HERSHEY_SIMPLEX, 2, [255, 0, 0], 3)

    return result

video.process_clip(input_video_file, output_video_file, process_frame)
