import cv2
from pose_detector import PoseDetector
from angle_utils import calculate_angle
from rep_counter import RepCounter
from feedback import get_feedback
from exercise_detector import detect_exercise_type

def main():
    cap = cv2.VideoCapture("/Users/gowthamyarramaddi/Documents/cvip project/pose_estimation_webapp/data/istockphoto-994036364-640_adpp_is.mp"4)  # Your push-up video
    detector = PoseDetector()

    detected_type = 'unknown'
    counter = None
    frame_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame, results = detector.detect_pose(frame)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            if frame_count % 30 == 0 or detected_type == 'unknown':
                detected_type = detect_exercise_type(lm)
                if detected_type != 'unknown' and counter is None:
                    counter = RepCounter(detected_type)

            if detected_type != 'unknown' and counter:
                if detected_type == 'plank':
                    y1 = lm[11].y  # shoulder
                    y2 = lm[23].y  # hip
                    y3 = lm[27].y  # ankle
                    form_ok = abs(y1 - y2) < 0.05 and abs(y2 - y3) < 0.05

                    _, _, duration = counter.count_reps(form_ok=form_ok)

                    cv2.putText(frame, f'Plank: {duration} sec', (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f'Form: {"Good" if form_ok else "Fix posture"}', (30, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                else:
                    if detected_type in ['squat', 'lunge']:
                        a = [lm[23].x, lm[23].y]
                        b = [lm[25].x, lm[25].y]
                        c = [lm[27].x, lm[27].y]
                    elif detected_type == 'pushup':
                        a = [lm[11].x, lm[11].y]
                        b = [lm[13].x, lm[13].y]
                        c = [lm[15].x, lm[15].y]

                    angle = calculate_angle(a, b, c)
                    count, stage, _ = counter.count_reps(angle)
                    feedback = get_feedback(angle)

                    cv2.putText(frame, f'{detected_type.capitalize()} Reps: {count}', (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f'Feedback: {feedback}', (30, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Pose Estimation with Plank Timer', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()