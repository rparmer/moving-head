import config
import logging
from operator import attrgetter
from stream import Stream
from object_detector import ObjectDetector
from servo_controller import ServoController

class MovingHead():
    def __init__(self):
        self.config = config.Config()
        self.stream = None
        self.object_detector = None
        self.servo_controller = None
        self._setup_stream()
        self._setup_object_detector()
        self._setup_servo_controller()
    
    def __del__(self):
        if self.stream != None:
            self.stream.stop()

    def _setup_stream(self):
        self.stream = Stream(
            source = self.config.stream.source,
            live = self.config.stream.live,
        )
        self.view = self.config.stream.view
        self.stream.start()

    def _setup_object_detector(self):
        self.object_detector = ObjectDetector(
            model_file = self.config.object_detector.model_file,
            confidence_threshold = self.config.object_detector.confidence_threshold,
            verbose = self.config.object_detector.verbose
        )

    def _setup_servo_controller(self):
        if self.config.servo.enabled == True:
            self.servo_controller = ServoController(
                gpip_pin = self.config.servo.gpio_pin
            )

    def calculate_position_value(self, detection):
        _, frame_width = detection.frame.shape[:2]
        frame_center = frame_width / 2
        offset = frame_center - detection.x_center
        # position = self._round_nearest(offset / frame_center, 0.05) * -1 # reverse position since servo is mounted upside down
        position = (offset / frame_center) * -1 # reverse position since servo is mounted upside down
        return position

    def _round_nearest(self, num, to):
        return round(num / to) * to

    def handle_detection(self, detection):
        if self.config.servo.enabled == True:
            position = self.calculate_position_value(detection)
            self.servo_controller.set_servo_position(position)

    def process_frames_from_stream(self):
        while True:
            frame = self.stream.get_frame()
            
            if self.stream.is_frame_empty(frame):
                continue
            
            results, frame = self.object_detector.process_frame(frame)

            if len(results) > 0:
                highest_confidence = max(results, key=attrgetter('confidence'))
                self.handle_detection(highest_confidence)

            if self.view == True:
                self.stream.view(frame)

    def run(self):
        logging.info('Running moving head application')
        try:
            self.process_frames_from_stream()
        except KeyboardInterrupt:
            pass

def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    mh = MovingHead()
    mh.run()

if __name__ == '__main__':
    main()
