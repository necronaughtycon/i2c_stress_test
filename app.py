#!/venv/bin/python3
'''
This is a simple Kivy application to test the performance of the ADC and MCP23017.
'''


# Standard imports.
import time
from collections import deque

# Third-party imports.
from kivy.lang import Builder
from kivy.properties import (
    StringProperty, NumericProperty,
    DictProperty, ListProperty, ObjectProperty
)
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock

# from adafruit_mcp230xx.mcp23017 import MCP23017
# from digitalio import Direction
# Initialize I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)

# Local imports.
from components import ADCDialog, ADCResults

class ADCTestScreen(MDScreen):
    pass


class MCPTestScreen(MDScreen):
    pass


class StressTestApp(MDApp):
    ''' Main application class. '''

    adc_stored = ListProperty([])
    adc_requests = NumericProperty()
    adc_requests_received = NumericProperty()
    adc_bus_status = StringProperty('OK')
    adc_task = None
    adc_update_task = None

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
        self.stop_adc_test()
        self.adc_requests = int(requests)
        self.adc_requests_received = 0
        self.show_adc_dialog()
        self.schedule_adc_intervals(frequency, stored)
        
    def schedule_adc_intervals(self, frequency, list_size):
        data_held = deque(maxlen=int(list_size))
        self.adc_task = Clock.schedule_interval(
            lambda dt: self.handle_adc_data(data_held), 
            int(frequency)
        )

    
    def show_adc_dialog(self):
        ''' Display a dialog with live statistics for the ongoing ADC test. '''
        if not hasattr(self, 'adc_dialog'):
            self.adc_dialog = ADCDialog(self)
            self.adc_dialog.button.bind(on_press=self.stop_adc_test)
            self.adc_dialog.dialog.bind(on_dismiss=self.stop_adc_test)
        self.adc_dialog.open()

    def show_adc_results(self):
        ''' Display the results of the ADC test. '''
        if not hasattr(self, 'adc_results'):
            self.adc_results = ADCResults(self)
        self.adc_results.update_information(self.adc_requests, self.adc_requests_received, self.adc_bus_status)
        self.adc_results.open()

    def handle_adc_data(self, data_held):
        ''' Handle the ADC data. '''
        requests_sent = 0
        for request in range(self.adc_requests):
            # Do something (print a number for now).
            requests_sent += 1
            data_held.append(requests_sent)
            self.adc_requests_received += 1
        self.adc_dialog.update_information(self.adc_requests, self.adc_requests_received)
        self.adc_stored = list(data_held)

    def stop_adc_test(self, instance=None):
        ''' Stop and unschedule the ADC test. '''
        if self.adc_task:
            self.adc_task.cancel()
            self.adc_task = None
            # self.adc_requests = 0
            # self.adc_stored.clear()
        self.show_adc_results()


if __name__ == '__main__':
    StressTestApp().run()