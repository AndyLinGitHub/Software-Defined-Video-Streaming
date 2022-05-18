import time
import argparse
import threading as thread
from collections import deque

import cv2
import mediapipe

mp_object_detection = mediapipe.solutions.object_detection
mp_hands = mediapipe.solutions.hands
mp_pose = mediapipe.solutions.pose
mp_face_detection = mediapipe.solutions.face_detection

mp_drawing_styles = mediapipe.solutions.drawing_styles
mp_drawing = mediapipe.solutions.drawing_utils

def object_detection(image):
    with mp_object_detection.ObjectDetection(min_detection_confidence=0.1) as od:
        results = od.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)

    return image

def hand_pose_tracking(image):
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())

    return image

def pose_estimation(image):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    return image

def face_detection(image):
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)

    return image

camera_pipeline = (
        "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)1920, height=(int)1080, "
            "format=(string)NV12, framerate=(fraction)30/1 ! "
        "queue ! "
        "nvvidconv flip-method=2 ! "
            "video/x-raw, "
            "width=(int)1920, height=(int)1080, "
            "format=(string)BGRx, framerate=(fraction)30/1 ! "
        "videoconvert ! "
            "video/x-raw, format=(string)BGR ! "
        "appsink"
    )

rtmp_pipeline = (
        "appsrc ! "
            "video/x-raw, format=(string)BGR ! "
        "queue ! "
        "videoconvert ! "
            "video/x-raw, format=RGBA ! "
        "nvvidconv ! "
        "nvv4l2h264enc bitrate=8000000 ! "
        "h264parse ! "
        "flvmux ! "
        'rtmpsink location="rtmp://localhost/rtmp/live live=1"'
    )

class Gstreamer:
    def __init__(self):
        self.buffer = deque(maxlen = 2)
        self.started = False
        self.algo = "start"


    def gstreamer_camera(self):
        while(True):
            try:
                if not self.started:
                    self.cap.release()
                    break

                ret, frame = self.cap.read()
                if not ret:
                    break

                self.buffer.appendleft(frame)
                print("read")

            except KeyboardInterrupt:
                self.cap.release()
                break
        
        print("Camera Stop.")

        return 0


    def gstreamer_rtmpstream(self):
        while(True):
            try:
                if not self.started:
                    self.out.release()
                    break

                if len(self.buffer) == 0:
                    continue

                else:
                    image = self.buffer.pop()
                    print("write")

                    if self.algo == "od":
                        image = object_detection(image)

                    if self.algo == "hpt":
                        image = hand_pose_tracking(image)

                    if self.algo == "pe":
                        image = pose_estimation(image)

                    if self.algo == "fd":
                        image = face_detection(image)

                    self.out.write(image)

            except KeyboardInterrupt:
                self.out.release()
                break

        print("Stream Stop.")

        return 0
        
    def change_algo(self, algo):
        self.algo = algo

        if algo == "terminate":
            self.started = False

    def start(self):
        self.cap = cv2.VideoCapture(camera_pipeline, cv2.CAP_GSTREAMER)
        self.out = cv2.VideoWriter(rtmp_pipeline, 0, 30, (1920, 1080))

        self.p_1 = thread.Thread(target = self.gstreamer_camera)
        self.p_2 = thread.Thread(target = self.gstreamer_rtmpstream)

        print("Start")
        print("Camera Opened:", self.cap.isOpened())
        self.started = True

        self.p_1.start()
        self.p_2.start()