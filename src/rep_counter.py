import time

class RepCounter:
    def __init__(self, exercise='squat'):
        self.count = 0
        self.stage = None
        self.exercise = exercise
        self.plank_start_time = None
        self.plank_duration = 0

    def count_reps(self, angle=None, form_ok=True):
        if self.exercise in ['squat', 'lunge']:
            if angle > 160:
                self.stage = "down"
            if angle < 90 and self.stage == "down":
                self.stage = "up"
                self.count += 1

        elif self.exercise == 'pushup':
            if angle > 150:
                self.stage = "up"
            if angle < 90 and self.stage == "up":
                self.stage = "down"
                self.count += 1

        elif self.exercise == 'plank':
            if form_ok:
                if self.plank_start_time is None:
                    self.plank_start_time = time.time()
                self.plank_duration = int(time.time() - self.plank_start_time)
            else:
                self.plank_start_time = None
                self.plank_duration = 0

        return self.count, self.stage, self.plank_duration
