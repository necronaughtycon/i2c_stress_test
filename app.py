import time
from collections import deque

from kivy.lang import Builder
from kivy.properties import (
    StringProperty, NumericProperty,
    DictProperty, ListProperty, ObjectProperty
)
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from kivy.utils import hex_colormap
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer
)
# from adafruit_mcp230xx.mcp23017 import MCP23017
# from digitalio import Direction
# Initialize I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)


class ADCTestScreen(MDScreen):
    pass


class MCPTestScreen(MDScreen):
    test_type = StringProperty('')


class StressTestApp(MDApp):
    ''' Main application class. '''

    adc_requests = NumericProperty(0)
    adc_stored = DictProperty({})
    adc_task = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())

    def build(self):
        ''' Create the application. '''
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Ghostwhite'
        self.setup_screens()
        # Clock.schedule_interval(self.change_theme_color, .5)
        return self.sm

    def screen_config(self):
        ''' Define the screens and their kv files. '''
        return {
            'adc_test_screen': {'path': 'adc_test_screen.kv', 'class': ADCTestScreen},
            'mcp_test_screen': {'path': 'mcp_test_screen.kv', 'class': MCPTestScreen}
        }

    def load_kv_file(self, info):
        ''' Load the kv file for a screen. '''
        Builder.load_file(f'views/{info["path"]}')

    def setup_screens(self):
        ''' Create the screens and add them to the screen manager. '''
        screens = self.screen_config()
        Builder.load_file('views/constants.kv')
        for name, info in screens.items():
            self.load_kv_file(info)
            self.sm.add_widget(info['class'](name=name))

    def start_adc_test(self, requests, frequency, stored):
        ''' Test to simulate ADC readings. '''
        self.stop_adc_test()  # Stop any existing ADC test.
        self.adc_requests = int(requests)
        data_held = deque(maxlen=int(stored))
        self.adc_task = Clock.schedule_interval(lambda dt: self.handle_adc_data(data_held), int(frequency))

    def handle_adc_data(self, data_held):
        ''' Handle the ADC data. '''
        requests_sent = 0
        for request in range(self.adc_requests):
            # Do something (print a number for now).
            requests_sent += 1
            data_held.append(requests_sent)
        self.adc_stored = list(data_held)
        print(f'Requests sent: {requests_sent}')
        print(f'Data held: {len(data_held)}')

    def stop_adc_test(self):
        ''' Stop and unschedule the ADC test. '''
        if self.adc_task:
            self.adc_task.cancel()
            self.adc_task = None
            self.adc_requests = 0
            self.adc_stored.clear()

    def show_adc_dialog(self):
        ''' Display a dialog with live statistics for the ongoing ADC test. '''
        MDDialog(
            MDDialogHeadLineText(
                text='Live ADC Test Statistics'
            ),  
        )

if __name__ == '__main__':
    StressTestApp().run()