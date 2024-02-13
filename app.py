#!/usr/bin/env python3
'''
This is a simple Kivy application to test the performance of the ADC1115 and MCP23017.
'''

# Standard imports.
from collections import deque
import time

# Third-party imports.
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import settings.kivy_config

# Local imports.
from components import ADCDialog, ADCResults
from utility import ADC

# from adafruit_mcp230xx.mcp23017 import MCP23017
# from digitalio import Direction
# Initialize I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)


class ADCTestScreen(MDScreen):
    ''' ADC test screen. '''
    pass


class MCPTestScreen(MDScreen):
    ''' MCP test screen. '''
    pass


class StressTestApp(MDApp):
    ''' Main application class. '''

    adc_requests = NumericProperty()
    adc_requests_received = NumericProperty()
    adc_payload = StringProperty()
    adc_bus_status = StringProperty('OK')
    adc_stored = ListProperty([])
    adc_task = None
    adc_update_task = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adc = ADC()
        self.sm = ScreenManager(transition=NoTransition())

    def build(self):
        ''' Create the application. '''
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Darkblue'
        self.setup_screens()
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

    def switch_screen(self, screen_name):
        ''' Switch to the specified screen. '''
        self.sm.current = screen_name

    def start_adc_test(self, requests, frequency, stored):
        ''' Test to simulate ADC readings. '''
        self.adc_requests = int(requests)
        self.adc_requests_received = 0
        self.adc_stored = []
        delay = int(frequency) / self.adc_requests
        self.schedule_adc_intervals()
        self.show_adc_dialog()
        self.get_adc_data(delay, stored)
        
    def get_adc_data(self, delay, stored):
        ''' Get the ADC payload. '''
        data_held = deque(maxlen=int(stored))
        for _ in range(self.adc_requests):
            self.adc_payload = self.adc.read_adc(delay)
            if self.adc_payload != 'ERR':
                self.adc_requests_received += 1
                data_held.append(self.adc_payload)
                self.adc_bus_status = 'OK'
                self.adc_stored = list(data_held)
            else:
                self.adc_bus_status = 'FAILED'
                self.stop_adc_test()
                break
        
    def schedule_adc_intervals(self):
        ''' Schedule the intervals for the ADC test. '''
        self.adc_task = Clock.schedule_interval(self.update_adc_information, 1 / 30)
        
    def update_adc_information(self, dt):
        ''' Update the ADC information. '''
        self.adc_dialog.update_information(self.adc_requests, self.adc_requests_received, len(self.adc_stored), self.adc_payload)

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
        self.adc_results.update_status(self.adc_requests, self.adc_requests_received, self.adc_bus_status)
        self.adc_results.open()

    def stop_adc_test(self, instance=None):
        ''' Stop and unschedule the ADC test. '''
        if self.adc_task:
            self.adc_task.cancel()
            self.adc_task = None
            self.adc_stored.clear()
            if hasattr(self, 'adc_dialog'):
                self.adc_dialog.close()
            self.show_adc_results()


if __name__ == '__main__':
    StressTestApp().run()