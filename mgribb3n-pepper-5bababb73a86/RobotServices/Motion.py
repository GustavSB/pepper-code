"""
Library class to access motion methods
"""

import pprint


class Motion:
    def __init__(self, session):
        """Initialise service for motion"""
        self.motion_service = session.service("ALMotion")

    def rotate(self, angle):
        """Rotates the given angle in degrees"""
        x = 0
        y = 0
        degree_in_rad = 0.0174532925
        angle_in_rad = degree_in_rad * angle
        return self.motion_service.moveTo(x, y, angle_in_rad)

    def rotate_async(self, angle):
        """Rotates the given angle in degrees"""
        x = 0
        y = 0
        degree_in_rad = 0.0174532925
        angle_in_rad = degree_in_rad * angle
        return self.motion_service.moveTo(x, y, angle_in_rad, _async=True)

    def go_to(self, x, y, angle):
        """Go to given position in x,y coordinates"""
        degree_in_rad = 0.0174532925
        angle_in_rad = degree_in_rad * angle
        return self.motion_service.moveTo(x, y, angle_in_rad)

    def go_to_normalized(self, x, y, angle):
        """Move with normalized velocity along x, y, angle axis"""
        return self.motion_service.moveToward(x, y, angle)

    def go_to_async(self, x, y, angle):
        """Go to given position in x,y coordinates"""
        degree_in_rad = 0.0174532925
        angle_in_rad = degree_in_rad * angle
        return self.motion_service.moveTo(x, y, angle_in_rad, _async=True)

    def wait_until_move_is_finished(self):
        """Wait until the movement has been finished"""
        self.motion_service.waitUntilMoveIsFinished()

    def close_hand(self, hand_name):
        """Close the given hand"""
        self.motion_service.closeHand(hand_name)

    def open_hand(self, hand_name):
        """Open the given hand"""
        self.motion_service.openHand(hand_name)

    def lock_hand(self, hand_name, stiffness=1.0):
        """Lock the given hand"""
        self.motion_service.setStiffnesses(hand_name, stiffness)

    def wake_up(self):
        """Wake up the robot and put into initial position"""
        self.motion_service.wakeUp()

    def rest(self):
        """Rest the robot and put into crouch position"""
        self.motion_service.rest()

    # get methods
    def get_angles(self, names, use_sensors):
        """Prints the current angles of the arm/joints provided"""
        print self.motion_service.getAngles(names, use_sensors)

    # set methods
    def set_angles(self, names, angles, speed):
        """Sets the angles of the arm/joints provided"""
        self.motion_service.setAngles(names, angles, speed)

    def set_angles_async(self, names, angles, speed):
        """Sets the angles of the arm/joints provided"""
        self.motion_service.setAngles(names, angles, speed, _async=True)

    def set_stiffness(self, names, stiffness):
        """Set stiffness if the arm/joints provided"""
        self.motion_service.setStiffnesses(names, stiffness)

    def set_arms(self, left_arm_enable, right_arm_enable):
        """Enable/disable arms"""
        self.motion_service.setMoveArmsEnabled(left_arm_enable, right_arm_enable)

    def set_external_collision_protection_enabled(self, name, state):
        """Enable the given external collision protection"""
        self.motion_service.setExternalCollisionProtectionEnabled(name, state)

    def set_orthogonal_security_distance(self, distance):
        """Set the orthogonal security collision distance, default is 0.4m"""
        self.motion_service.setOrthogonalSecurityDistance(distance)

    def set_tangential_security_distance(self, distance):
        """Set the tangential security collision distance, default is 0.1m"""
        self.motion_service.setTangentialSecurityDistance(distance)

    def enable_collision_detection(self, state):
        self.set_external_collision_protection_enabled("All", state)
        self.set_external_collision_protection_enabled("Move", state)

    # print methods
    def print_status_arms(self):
        """Prints status if arms are enabled"""
        print self.motion_service.getMoveArmsEnabled("RArm")
        print self.motion_service.getMoveArmsEnabled("LArm")

    def print_status_breath(self, chain_name):
        """Prints status of breath of given chain_name"""
        print self.motion_service.getBreathEnabled(chain_name)

    def print_status_idle_posture_enabled(self, chain_name):
        """Prints status of the given idle posture"""
        print self.motion_service.getIdlePostureEnabled(chain_name)

    def print_status_external_collision_protection_enabled(self, name):
        """Prints status of the given external collision protection
            All, Move, Arms, LArm or RArm"""
        print self.motion_service.getExternalCollisionProtectionEnabled(name)

    def print_status_orthogonal_security_distance(self):
        """Prints the length of the orthogonal security distance"""
        print self.motion_service.getOrthogonalSecurityDistance()

    def print_status_tangential_security_distance(self):
        """Prints the length of the tangential security distance"""
        print self.motion_service.getTangentialSecurityDistance()

    def print_body_names(self, name):
        pprint.pprint(self.motion_service.getBodyNames(name))





