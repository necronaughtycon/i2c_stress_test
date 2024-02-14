#!/usr/bin/env python3
'''
This is a simple Kivy application to test the performance of the ADC1115 and MCP23017.
'''

# Standard imports.
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
    adc_requests_filled = NumericProperty()
    adc_bus_status = StringProperty('OK')
    adc_task = None

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

    def start_adc_test(self, requests, frequency):
        ''' Test to simulate ADC readings. '''
        self.adc_requests = int(requests)
        self.adc_requests_filled = 0
        clock = self.calculate_timing(frequency)
        self.schedule_adc_intervals(clock)

    def calculate_timing(self, frequency):
        ''' Calculate the timing for the ADC test. '''
        fps = 60
        delay = int(frequency) / self.adc_requests
        frames_per_request = fps / delay
        clock = 1 / fps * frames_per_request

    def get_adc_payload(self):
        ''' Get the ADC payload. '''
        value = self.adc.read_adc()
        if value != 'ERR':
            payload, requests_filled = self.get_adc_data()
            self.adc_dialog.update_information(self.adc_requests, requests_filled, payload)
        else:
            self.adc_bus_status = 'FAILED'
            self.stop_adc_test()
        payload, requests_filled = self.get_adc_data()
        self.adc_dialog.update_information(self.adc_requests, requests_filled, payload)

    def schedule_adc_intervals(self, clock):
        ''' Schedule the intervals for the ADC test. '''
        self.show_adc_dialog()
        self.adc_task = Clock.schedule_interval(self.get_adc_payload, clock)

    def show_adc_dialog(self):
        ''' Display a dialog with live statistics for the ongoing ADC test. '''
        if not hasattr(self, 'adc_dialog'):
            self.adc_dialog = ADCDialog(self)
            self.adc_dialog.button.bind(on_press=self.stop_adc_test)
            self.adc_dialog.dialog.bind(on_dismiss=self.stop_adc_test)
        self.adc_dialog.open()
        self.schedule_adc_intervals()

    def get_adc_data(self):
        ''' Get the ADC data. '''
        payload = self.adc.get_latest_payload()
        requests_filled = self.adc.get_requests_filled()
        return payload, requests_filled

    def show_adc_results(self):
        ''' Display the results of the ADC test. '''
        if not hasattr(self, 'adc_results'):
            self.adc_results = ADCResults(self)
        payload, requests_filled = self.get_adc_data()
        self.adc_results.update_status(self.adc_requests, requests_filled, self.adc_bus_status)
        self.adc_results.open()

    def stop_adc_test(self, instance=None):
        ''' Stop and unschedule the ADC test. '''
        requests_filled = self.adc.get_requests_filled()
        if self.adc_task:
            self.adc_task.cancel()
            self.adc_task = None
            if hasattr(self, 'adc_dialog'):
                self.adc_dialog.close()
        self.show_adc_results()


if __name__ == '__main__':
    StressTestApp().run()