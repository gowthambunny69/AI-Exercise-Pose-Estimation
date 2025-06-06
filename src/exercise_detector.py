def detect_exercise_type(landmarks):
    left_shoulder = landmarks[11]
    left_elbow = landmarks[13]
    left_wrist = landmarks[15]
    left_hip = landmarks[23]
    left_knee = landmarks[25]
    left_ankle = landmarks[27]

    shoulder_y = left_shoulder.y
    elbow_y = left_elbow.y
    wrist_y = left_wrist.y
    hip_y = left_hip.y
    knee_y = left_knee.y
    ankle_y = left_ankle.y

    is_horizontal = abs(shoulder_y - hip_y) < 0.1 and abs(elbow_y - shoulder_y) < 0.1
    elbow_below_shoulder = elbow_y > shoulder_y
    if is_horizontal and elbow_below_shoulder:
        return 'pushup'

    horizontal_alignment = (
        abs(shoulder_y - hip_y) < 0.08 and
        abs(hip_y - ankle_y) < 0.08
    )
    elbow_under_shoulder = abs(left_elbow.x - left_shoulder.x) < 0.1

    if horizontal_alignment and elbow_under_shoulder:
        return 'plank'

    standing = hip_y < shoulder_y and knee_y > hip_y and ankle_y > knee_y
    knee_bend = abs(knee_y - hip_y)

    if standing and knee_bend < 0.2:
        return 'squat'

    if standing and knee_bend >= 0.2:
        return 'lunge'


    return 'unknown'