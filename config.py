import os
import yaml

try: 
    config = yaml.safe_load(open(os.environ.get('CONFIG_FILE', 'config.yml')))
except:
    config = {}

class Config():
    def __init__(self):
        self.stream = _Stream(**config.get('stream', {}))
        self.object_detector = _ObjectDetector(**config.get('object_detector', {}))
        self.servo = _Servo(**config.get('servo', {}))

class _Stream():
    def __init__(self, **kwargs):
        self.live = kwargs.get('live', True)
        self.source = kwargs.get('source', 0)
        self.view = kwargs.get('view', False)

class _ObjectDetector():
    def __init__(self, **kwargs):
        self.model_file = kwargs.get('model_file', 'models/yolo11n.pt')
        self.verbose = kwargs.get('verbose', False)
        self.confidence_threshold = kwargs.get('confidence_threshold', 0.4)

class _Servo():
    def __init__(self, **kwargs):
        self.enabled = kwargs.get('enabled', True)
        self.gpio_pin = kwargs.get('gpio_pin', 17)
