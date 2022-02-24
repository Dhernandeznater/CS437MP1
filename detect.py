import argparse
import sys
import time
import picar_4wd as fc 

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions

MODEL = 'efficientdet_lite0.tflite'
CAMERA_ID = 0
WIDTH = 640
HEIGHT = 480
NUM_THREADS = 4


# Use Tensorflow to detect a stop sign, if one is found
# stop car for 5 seconds and continue the movement of the car
def detect_stop(forward_time: float):
    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=NUM_THREADS,
        score_threshold=0.3,
        max_results=3,
        enable_edgetpu=False)
    detector = ObjectDetector(model_path=MODEL, options=options)

    cur_time = time.time()
    total_time = forward_time
    stop_detected = False

    while cur_time - start_time < total_time:
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        image = cv2.flip(image, 1)

        detections = detector.detect(image)

        # Loop through detections, stop if sign is detected
        for detection in detections:
            print(detection[1][0].label)
            if detection[1][0].label == "stop sign" and not stop_detected:
                print("Found Stop Sign")
                fc.stop()
                time.sleep(5)
                fc.forward(100)
                total_time += 5
                stop_detected = True
        
        cur_time = time.time()

    cap.release()

    return stop_detected

fc.forward(100)
detect_stop(10)
print("done run")
fc.stop()