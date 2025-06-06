def get_feedback(angle):
    if angle < 90:
        return "Good form!"
    elif angle > 160:
        return "Go lower!"
    else:
        return "Keep going!"
