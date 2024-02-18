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


class StressTestApp(MDApp):
    ''' Main application class. '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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


class ADCTestScreen(MDScreen):
    ''' ADC test screen. '''

    requests = NumericProperty()
    frequency = NumericProperty()
    requests_filled = NumericProperty()
    bus_status = StringProperty('OK')
    last = NumericProperty()
    adc_task = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adc = None

    def start_adc_test(self, requests, frequency):
        ''' Test to simulate ADC readings. '''
        self.requests = int(requests)
        self.frequency = int(frequency)
        self.schedule_adc()

    def schedule_adc(self):
        ''' Schedule the intervals for the ADC test. '''
        self.show_adc_dialog()
        delay = self.frequency / self.requests
        self.adc = ADC(delay=delay)
        self.adc_task = Clock.schedule_interval(self.update_adc_information, 1)
        self.show_adc_dialog()

    def update_adc_information(self, *args):
        ''' Update the ADC info on screen. '''
        payload = self.adc.get_payload()
        if payload is not None:
            self.requests_filled = self.adc.get_requests_filled()
            self.check_missed_payloads_adc()
            self.adc_dialog.update_information(self.requests, self.requests_filled, payload)
        else:
            self.bus_status = 'FAILED'
            self.stop_adc_test()

    def check_missed_payloads_adc(self, *args):
        ''' Check for missed payloads in the ADC test. '''
        total_requests = self.adc.get_requests_filled()
        duration = self.adc.get_duration()
        expected_total = (int(duration) / self.frequency) * self.requests
        difference = int(expected_total) - total_requests
        if difference > 1:
            print(f'Missed Payloads: {difference}')
        else:
            print(f'Missed Payloads: 0')

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
        self.adc_results.update_status(self.requests, self.requests_filled, self.bus_status)
        self.adc_results.open()

    def stop_adc_test(self, instance=None):
        ''' Stop and unschedule the ADC test. '''
        if self.adc_task:
            self.adc_task.cancel()
            self.adc_task = None
            if hasattr(self, 'adc_dialog'):
                self.adc_dialog.close()
        if self.adc_missed_task:
            self.adc_missed_task.cancel()
            self.adc_missed_task = None
            self.adc_last = 0
        if hasattr(self, 'adc'):
            self.adc.stop()
        self.show_adc_results()


class MCPTestScreen(MDScreen):
    ''' MCP test screen. '''
    pass


if __name__ == '__main__':
    StressTestApp().run()