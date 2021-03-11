"""
Library of methods to set awareness, stimulus, engagement -and body tracking mode.

Types of stimulus
<People> is triggered by <Human detected by the camera>. Based on ALPeoplePerception. Priority 1
<Touch> is triggered by <A touch on the head, arm or bumper>. Based on ALTouch. Priority 2
<TabletTouch> is triggered by <A tablet touch>. Based on ALTabletService. Priority 3
<Sound> is triggered by <Any perceived sound>. Based on ALSoundLocalization. Priority 4
<Movement> is triggered by <Any perceived movement>. Based on ALMovementDetection. Priority 5
<NavigationMotion> is triggered by <Any movement in front of the robot base>. Based on MotionDetected(). Priority 6

Types of engagement modes
<Unengaged>. Can be distracted by any stimulus, or engage with another person.
<FullyEngaged>. Stops listening to stimulus and stays engaged with the same person.
<SemiEngaged>. Listen to stimulus and reacts, but will always go back to the engaged person.

Types of Tracking modes
<Head>. The tracking uses the head.
<BodyRotation>. The tracking uses the head and the rotation of the body.
<WholeBody>. The tracking uses the whole body, but doesn't make it rotate.
<MoveContextually. Tracking uses the head and autonomously performs smalls moves such as approaching the tracked person.
"""


class Awareness:
    def __init__(self, session):
        """Initialise service"""
        self.awareness_service = session.service("ALBasicAwareness")

    def print_status_stimulus(self):
        """Check state of basic awareness and stimulus"""
        print "Basic awareness enabled: " + str(self.awareness_service.isEnabled())
        print "Basic awareness running: " + str(self.awareness_service.isRunning())
        print "People stimulus enabled: " + str(self.awareness_service.isStimulusDetectionEnabled("People"))
        print "Touch stimulus enabled: " + str(self.awareness_service.isStimulusDetectionEnabled("Touch"))
        print "TabletTouch stimulus enabled: " + str(self.awareness_service.isStimulusDetectionEnabled("TabletTouch"))
        print "Sound stimulus enabled: " + str(self.awareness_service.isStimulusDetectionEnabled("Sound"))
        print "Movement stimulus enabled: " + str(self.awareness_service.isStimulusDetectionEnabled("Movement"))
        print "NavigationMotion stimulus enabled: " + str(self.awareness_service.isStimulusDetectionEnabled("NavigationMotion"))

    # print methods
    def print_status_engagement_mode(self):
        """Print which engagement mode is enabled"""
        print str(self.awareness_service.getEngagementMode()) + ": is enabled"

    def print_status_tracking_mode(self):
        """Print which tracking mode is enabled"""
        print str(self.awareness_service.getTrackingMode()) + ": is enabled"

    # set basic awareness
    def set_basic_awareness(self, state):
        """Enable/disable basic awareness"""
        self.awareness_service.setEnabled(state)

    # set stimulus - individual
    def set_people_stimulus(self, state):
        """Enable/disable people stimulus"""
        self.awareness_service.setStimulusDetectionEnabled("People", state)

    def set_touch_stimulus(self, state):
        """Enable/disable touch stimulus"""
        self.awareness_service.setStimulusDetectionEnabled("Touch", state)

    def set_tablet_touch_stimulus(self, state):
        """Enable/disable tablet touch stimulus"""
        self.awareness_service.setStimulusDetectionEnabled("TabletTouch", state)

    def set_sound_stimulus(self, state):
        """Enable/disable sound stimulus"""
        self.awareness_service.setStimulusDetectionEnabled("Sound", state)

    def set_movement_stimulus(self, state):
        """Enable/disable movement stimulus"""
        self.awareness_service.setStimulusDetectionEnabled("Movement", state)

    def set_navigation_motion_stimulus(self, state):
        """Enable/disable navigation motion stimulus"""
        self.awareness_service.setStimulusDetectionEnabled("NavigationMotion", state)

    # set stimulus - all at once
    def set_all_stimulus(self, people, touch, t_touch, sound, movement, n_motion):
        """Enable/disable all stimulus in one method"""
        self.awareness_service.setStimulusDetectionEnabled("People", people)
        self.awareness_service.setStimulusDetectionEnabled("Touch", touch)
        self.awareness_service.setStimulusDetectionEnabled("TabletTouch", t_touch)
        self.awareness_service.setStimulusDetectionEnabled("Sound", sound)
        self.awareness_service.setStimulusDetectionEnabled("Movement", movement)
        self.awareness_service.setStimulusDetectionEnabled("NavigationMotion", n_motion)

    # set engagement mode
    def set_un_engaged_mode(self):
        """Enable unengaged mode"""
        self.awareness_service.setEngagementMode("Unengaged")

    def set_fully_engaged_mode(self):
        """Enable fully engaged mode"""
        self.awareness_service.setEngagementMode("FullyEngaged")

    def set_semi_engaged_mode(self):
        """Enable semi engaged mode"""
        self.awareness_service.setEngagementMode("SemiEngaged")

    # set tracking mode
    def set_head_tracking_mode(self):
        """Enable head tracking mode"""
        self.awareness_service.setTrackingMode("Head")

    def set_body_rotation_mode(self):
        """Enable body rotation mode"""
        self.awareness_service.setTrackingMode("BodyRotation")

    def set_whole_body_tracking_mode(self):
        """Enable whole body rotation mode"""
        self.awareness_service.setTrackingMode("WholeBody")

    def set_move_contextually_tracking_mode(self):
        """Enable move contextually mode"""
        self.awareness_service.setTrackingMode("MoveContextually")



