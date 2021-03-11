"""
Library of methods to set head tracking and recognition.
"""


class HeadTracking:
    def __init__(self, session):
        """Initialise service"""
        self.face_detection_service = session.service("ALFaceDetection")

    # print methods
    def print_status_head_tracking(self):
        """Print status of head tracking"""
        print self.face_detection_service.isTrackingEnabled()

    def print_status_recognition(self):
        """Print status of face recognition"""
        print self.face_detection_service.isRecognitionEnabled()

    # set methods
    def set_tracking(self, state):
        """Enable/disable head tracking"""
        self.face_detection_service.setTrackingEnabled(state)

    def set_recognition(self, state):
        """Enable/disable face recognition"""
        self.face_detection_service.setRecognitionEnabled(state)

    def set_static(self, state):
        """Disable or re-enable according to state"""
        self.set_tracking(state)
        self.set_recognition(state)







