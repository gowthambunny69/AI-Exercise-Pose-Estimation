import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self, static_mode=False, model_complexity=1, enable_segmentation=False, detection_confidence=0.5, tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=static_mode,
                                      model_complexity=model_complexity,
                                      enable_segmentation=enable_segmentation,
                                      min_detection_confidence=detection_confidence,
                                      min_tracking_confidence=tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_pose(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame, results
