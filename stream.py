import cv2
import logging
import threading
from time import sleep

class Stream():
    def __init__(self, source = 0, live = True):
        logging.info('Setting up stream')
        self.source = source
        self.live = live
        self.live_frame = None
        self.stream = None
        self.thread = None
        self.running = False       

    def __del__(self):
        logging.info('Cleaning up stream')
        self.stop()
        cv2.destroyAllWindows()

    def _start_background_thread(self):
        self.thread = threading.Thread(name = 'camera_buffer', target = self._camera_buffer_thread, daemon = True)
        self.thread.start()

    def _camera_buffer_thread(self):
        while self.running:
            ret, frame = self.stream.read()
            if ret:
                self.live_frame = frame
            else:
                self.reconnect()

    def is_frame_empty(self, frame):
        return str(type(frame)) == str(type(None))
    
    def reconnect(self):
        self.stop()
        self.start()

    def get_frame(self):
        if self.live:
            if not self.is_frame_empty(self.live_frame):
                return self.live_frame
            else:
                return None
        else:
            _, frame = self.stream.read()
            return frame

    def view(self, frame):
        cv2.imshow('Camera Preview', frame)
        cv2.waitKey(1)

    def start(self):
        self.live_frame = None
        self.stream = cv2.VideoCapture(self.source)
        self.running = True
        if self.live:
            self._start_background_thread()

    def stop(self):
        self.running = False
        # Give stream thread time to stop
        sleep(0.1)
        if self.stream:
            self.stream.release()
        self.live_frame = None
        self.stream = None
        self.thread = None
