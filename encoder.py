import time
from gpiozero import Button

class Encoder():
    def __init__(self, PIN_A, PIN_B, PIN_C):
        self.rotate_up = False
        self.rotate_down = False
        self.button_selected = False

        self._sl_button = Button(PIN_A, pull_up=True)
        self._up_button = Button(PIN_B, pull_up=True)
        self._dn_button = Button(PIN_C, pull_up=True)

        # is there a difference between when_pressed and when_activated?
        # self._sl_button.when_pressed = self._sl_button_selected
        self._sl_button.when_activated = self._sl_button_selected
        self._up_button.when_activated = self._knob_rotated

    def _knob_rotated(self):
        if not self._dn_button.is_pressed:
            self.rotate_up = True
            time.sleep(0.1)
            self.rotate_up = False
        else:
            self.rotate_down = True
            time.sleep(0.1)
            self.rotate_down= False

    def _sl_button_selected(self):
        self.button_selected = True
        time.sleep(0.1)
        self.button_selected = False