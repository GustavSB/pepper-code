"""
Class of methods to set different group of LEDs and to set them in different colors.

Eyes can be in RGB colors.
Ears can only be Blue color.
Chest can be only Red, Green or Blue.
"""

class LEDController:
    ## Led groups
    G_EYES_RED = "EyesRed"
    G_EYES_GREEN = "EyesGreen"
    G_EYES_BLUE = "EyesBlue"
    G_CHEST_RED = "ChestRed"
    G_CHEST_GREEN = "ChestGreen"
    G_CHEST_BLUE = "ChestBlue"

    def __init__(self, session):
        """Initialise services, create groups"""
        self.led_service = session.service("ALLeds")
        self.__create_all_groups()

    def reset_group(self, group_name):
        """Set a group of LEDs to their default state"""
        self.led_service.reset(group_name)

    def reset_all(self):
        """Reset all LEDs to their default state"""
        self.led_service.reset("AllLeds")

    def set_group_on(self, group_name):
        """Set a group of LEDs on (maximum intensity)"""
        #self.set_group_off("FaceLeds")
        self.led_service.on(group_name)

    def set_group_intensity(self, group_name, intensity):
        """Set the intensity of a group of LEDs"""
        if 0 < intensity < 1:
            self.led_service.setIntensity(group_name, intensity)
        else:
            print "Intensity value must be a float between 0 and 1"

    def set_group_off(self, group_name):
        """Set a group of LEDs off (minimum intensity"""
        self.led_service.off(group_name)

    def set_all_groups_off(self):
        """Set all group of LEDs off"""
        self.set_group_off("FaceLeds")
        self.set_group_off("EarLeds")
        self.set_group_off("ChestLeds")

    def __create_group_red_eyes(self, color="Red"):
        """Create group - eye LEDs, red color"""
        eyes = ["Face/Led/" + color + "/Left/45Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/0Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/315Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/270Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/225Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/180Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/135Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/90Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/45Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/0Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/315Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/270Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/225Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/180Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/135Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/90Deg/Actuator/Value"]
        self.led_service.createGroup(self.G_EYES_RED, eyes)

    def __create_group_green_eyes(self, color="Green"):
        """Create group - eye LEDs, green color"""
        eyes = ["Face/Led/" + color + "/Left/45Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/0Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/315Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/270Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/225Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/180Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/135Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/90Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/45Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/0Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/315Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/270Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/225Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/180Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/135Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/90Deg/Actuator/Value"]
        self.led_service.createGroup(self.G_EYES_GREEN, eyes)

    def __create_group_blue_eyes(self, color="Blue"):
        """Create group - eye LEDs, blue color"""
        eyes = ["Face/Led/" + color + "/Left/45Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/0Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/315Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/270Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/225Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/180Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/135Deg/Actuator/Value",
                "Face/Led/" + color + "/Left/90Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/45Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/0Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/315Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/270Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/225Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/180Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/135Deg/Actuator/Value",
                "Face/Led/" + color + "/Right/90Deg/Actuator/Value"]
        self.led_service.createGroup(self.G_EYES_BLUE, eyes)

    def __create_group_red_chest(self, color="Red"):
        """Create group - chest LEDs, red color"""
        chest = ["ChestBoard/Led/" + color + "/Actuator/Value"]
        self.led_service.createGroup(self.G_CHEST_RED, chest)

    def __create_group_green_chest(self, color="Green"):
        """Create group - chest LEDs, green color"""
        chest = ["ChestBoard/Led/" + color + "/Actuator/Value"]
        self.led_service.createGroup(self.G_CHEST_GREEN, chest)

    def __create_group_blue_chest(self, color="Blue"):
        """Create group - chest LEDs, blue color"""
        chest = ["ChestBoard/Led/" + color + "/Actuator/Value"]
        self.led_service.createGroup(self.G_CHEST_BLUE, chest)

    def __create_all_groups(self):
        """Create all the different LED groups listed"""
        self.__create_group_red_eyes()
        self.__create_group_green_eyes()
        self.__create_group_blue_eyes()
        self.__create_group_red_chest()
        self.__create_group_green_chest()
        self.__create_group_blue_chest()

    def sith_mode(self):
        """Enable sith mode"""
        self.set_all_groups_off()
        self.set_group_on("EyesRed")
        self.set_group_on("ChestRed")
        self.set_group_off("EarLeds")
