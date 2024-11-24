from input_base import InputBase
from input_base import Keys
from enum import Enum
from time import sleep
from sense_hat import SenseHat

class InputSenseHat(InputBase):
    """
    Input handler for Sense HAT joystick input.
    """
    def __init__(self):
        super().__init__()
        self.sense = SenseHat()
        self.last_event = None

    def key_pressed(self) -> bool:
        """
        Check if a key has been pressed.

        Returns:
            bool: True if a key is pressed, False otherwise.
        """
        events = self.sense.stick.get_events()
        if events:
            self.last_event = events[-1]  # Store the last event
            return True
        return False

    def read_key(self) -> Enum:
        """
        Map joystick actions to corresponding key codes.

        Returns:
            Enum: The key code corresponding to the joystick action.
        """
        if self.last_event:
            event = self.last_event
            if event.action == "pressed":
                if event.direction == "left":
                    return Keys.LEFT
                elif event.direction == "right":
                    return Keys.RIGHT
                elif event.direction == "middle":
                    return Keys.ENTER
        return None