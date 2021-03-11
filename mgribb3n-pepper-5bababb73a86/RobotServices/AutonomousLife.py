"""
Library of methods to set autonomous abilities.

List of autonomous abilities
<AutonomousBlinking>. Enables the robot to make its eye LEDs blink when it sees someone.
<BackGroundMovement>. Defines which slight movements the robot does autonomously.
<BasicAwareness>. Allows the robot to react to the environment.
<ListeningMovement>. Enables some slight movements showing that the robot is listening.
<SpeakingMovement>- Enables to start autonomously movements during the speech of the robot.
"""

from pprint import pprint


class AutonomousLife:
    def __init__(self, session):
        """Initialise services"""
        self.autonomous_life_service = session.service("ALAutonomousLife")

    # print methods
    def print_status_autonomous_abilities(self):
        """Pretty print the status of all autonomous abilities"""
        pprint(self.autonomous_life_service.getAutonomousAbilitiesStatus())

    # set autonomous abilities - individual
    def set_autonomous_blinking(self, state):
        """Enable/disable autonomous blinking"""
        self.autonomous_life_service.setAutonomousAbilityEnabled("AutonomousBlinking", state)

    def set_background_movement(self, state):
        """Enable/disable background movement """
        self.autonomous_life_service.setAutonomousAbilityEnabled("BackgroundMovement", state)

    def set_listening_movement(self, state):
        """Enable/disable listening movement"""
        self.autonomous_life_service.setAutonomousAbilityEnabled("ListeningMovement", state)

    def set_speaking_movement(self, state):
        """Enable/disable speaking movement"""
        self.autonomous_life_service.setAutonomousAbilityEnabled("SpeakingMovement", state)

    # set autonomous abilities - all at once
    def set_all_autonomous_abilities(self, blinking, bac_movement, lis_movement, spk_movement):
        """Enable/disable all autonomous abilities in one method"""
        self.autonomous_life_service.setAutonomousAbilityEnabled("AutonomousBlinking", blinking)
        self.autonomous_life_service.setAutonomousAbilityEnabled("BackgroundMovement", bac_movement)
        self.autonomous_life_service.setAutonomousAbilityEnabled("ListeningMovement", lis_movement)
        self.autonomous_life_service.setAutonomousAbilityEnabled("SpeakingMovement", spk_movement)

    def set_static(self, state):
        self.set_all_autonomous_abilities(state, state, state, state)

