.PHONY: tests

tests:
	python3 calibration.py test_images/straight_lines1.jpg output_images/straight_lines1-undistorted.jpg
	python3 transform.py output_images/straight_lines1-undistorted.jpg \
		output_images/straight_lines1-topview.jpg \
		output_images/straight_lines1-unwarped.jpg
	python3 threshold.py test_images/straight_lines1.jpg output_images/straight_lines1-threshold.jpg
	python3 calibration.py test_images/straight_lines2.jpg output_images/straight_lines2-undistorted.jpg
	python3 transform.py output_images/straight_lines2-undistorted.jpg \
		output_images/straight_lines2-topview.jpg \
		output_images/straight_lines2-unwarped.jpg
	python3 threshold.py test_images/straight_lines2.jpg output_images/straight_lines2-threshold.jpg
	python3 calibration.py test_images/test1.jpg output_images/test1-undistorted.jpg
	python3 transform.py output_images/test1-undistorted.jpg \
		output_images/test1-topview.jpg \
		output_images/test1-unwarped.jpg
	python3 threshold.py test_images/test1.jpg output_images/test1-threshold.jpg
	python3 calibration.py test_images/test2.jpg output_images/test2-undistorted.jpg
	python3 transform.py output_images/test2-undistorted.jpg \
		output_images/test2-topview.jpg \
		output_images/test2-unwarped.jpg
	python3 threshold.py test_images/test2.jpg output_images/test2-threshold.jpg
	python3 calibration.py test_images/test3.jpg output_images/test3-undistorted.jpg
	python3 transform.py output_images/test3-undistorted.jpg \
		output_images/test3-topview.jpg \
		output_images/test3-unwarped.jpg
	python3 threshold.py test_images/test3.jpg output_images/test3-threshold.jpg
	python3 calibration.py test_images/test4.jpg output_images/test4-undistorted.jpg
	python3 transform.py output_images/test4-undistorted.jpg \
		output_images/test4-topview.jpg \
		output_images/test4-unwarped.jpg
	python3 threshold.py test_images/test4.jpg output_images/test4-threshold.jpg
	python3 calibration.py test_images/test5.jpg output_images/test5-undistorted.jpg
	python3 transform.py output_images/test5-undistorted.jpg \
		output_images/test5-topview.jpg \
		output_images/test5-unwarped.jpg
	python3 threshold.py test_images/test5.jpg output_images/test5-threshold.jpg
	python3 calibration.py test_images/test6.jpg output_images/test6-undistorted.jpg
	python3 transform.py output_images/test6-undistorted.jpg \
		output_images/test6-topview.jpg \
		output_images/test6-unwarped.jpg
	python3 threshold.py test_images/test6.jpg output_images/test6-threshold.jpg
