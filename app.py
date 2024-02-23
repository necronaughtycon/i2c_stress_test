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
from components import ADCDialog, ADCResults, MCPDialog, MCPResults
from utility import ADC, MCP


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
    missed_requests = NumericProperty()
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
        self.adc = ADC()
        self.adc_task = Clock.schedule_interval(self.update_adc_information, 1/60)
        self.show_adc_dialog()

    def update_adc_information(self, *args):
        ''' Update the ADC info on screen. '''
        payload = self.adc.get_payload()
        if payload is not None:
            self.check_missed_payloads_adc()
            self.adc_dialog.update_information(self.requests, self.requests_filled, self.missed_requests, payload)
        else:
            self.bus_status = 'FAILED'
            self.stop_adc_test()

    def check_missed_payloads_adc(self, *args):
        ''' Check for missed payloads in the ADC test. '''
        total_requests = self.adc.get_requests_filled()
        duration = self.adc.get_duration()
        expected_total = (int(duration) / self.frequency) * self.requests
        difference = int(expected_total) - total_requests
        if expected_total > total_requests:
            self.missed_requests = difference
            self.requests_filled = int(total_requests)
        else:
            self.missed_requests = 0
            self.requests_filled = int(expected_total)

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
        self.adc_results.update_status(self.requests, self.requests_filled, self.missed_requests, self.bus_status)
        self.adc_results.open()

    def stop_adc_test(self, instance=None):
        ''' Stop and unschedule the ADC test. '''
        if self.adc_task:
            self.adc_task.cancel()
            self.adc_task = None
            if hasattr(self, 'adc_dialog'):
                self.adc_dialog.close()
        if hasattr(self, 'adc'):
            self.adc.stop()
        self.show_adc_results()


class MCPTestScreen(MDScreen):
    ''' MCP test screen. '''

    cycle_delay = NumericProperty()
    pin_delay = NumericProperty()
    function = StringProperty()
    bus_status = StringProperty('OK')
    mcp_task = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mcp = None

    def set_delays(self, pin_delay, cycle_delay):
        ''' Set custom delay times. '''
        self.convert_to_ms(pin_delay)
        self.cycle_delay = cycle_delay
        self.mcp.set_cycle_delay(self.cycle_delay)

    def convert_to_ms(self, pin_delay):
        ''' Convert seconds to milliseconds. '''
        self.pin_delay = int(pin_delay) / 1000
        self.mcp.set_pin_delay(self.pin_delay)

    def start_run_cycle(self, pin_delay, cycle_delay):
        ''' Start run cycle with custom delay. '''
        self.function = 'Run Cycle'
        self.mcp = MCP()
        self.set_delays(pin_delay, cycle_delay)
        self.schedule_mcp()
        self.mcp.run_cycle()

    def start_functionality_test(self, pin_delay, cycle_delay):
        ''' Start functionality test with custom delay. '''
        self.function = 'Functionality Test'
        self.mcp = MCP()
        self.set_delays(pin_delay, cycle_delay)
        self.schedule_mcp()
        self.mcp.functionality_test()

    def start_test_mode(self, pin_delay, cycle_delay):
        ''' Start test mode with custom delay. '''
        self.function = 'Test Mode'
        self.mcp = MCP()
        self.set_delays(pin_delay, cycle_delay)
        self.schedule_mcp()
        self.mcp.test_mode()

    def start_leak_test(self, pin_delay, cycle_delay):
        ''' Start leak test with custom delay. '''
        self.function = 'Leak Test'
        self.mcp = MCP()
        self.set_delays(pin_delay, cycle_delay)
        self.schedule_mcp()
        self.mcp.leak_test()

    def schedule_mcp(self):
        ''' Schedule the intervals for checking values of the MCP test. '''
        self.mcp_task = Clock.schedule_interval(self.update_mcp_information, 1)
        self.show_mcp_dialog()        

    def update_mcp_information(self, *args):
        ''' Get relay values in real time. '''
        mode = self.mcp.get_mode()
        motor, v1, v2, v5 = self.mcp.get_values()
        if mode is not None:
            if mode == 'Complete':
                self.bus_status = 'OK'
                self.stop_mcp_test()
            else:
                self.mcp_dialog.update_information(
                    self.function, mode.capitalize(),
                    self.pin_delay, 
                    self.cycle_delay,
                    motor, v1, v2, v5
                )
        else:
            self.bus_status = 'FAILED'
            self.stop_mcp_test()

    def show_mcp_dialog(self):
        ''' Display a dialog with live statistics for the ongoing MCP test. '''
        if not hasattr(self, 'mcp_dialog'):
            self.mcp_dialog = MCPDialog(self)
            self.mcp_dialog.button.bind(on_press=self.stop_mcp_test)
            self.mcp_dialog.dialog.bind(on_dismiss=self.stop_mcp_test)
        self.mcp_dialog.open()

    def show_mcp_results(self):
        ''' Display the results of the MCP test. '''
        if not hasattr(self, 'mcp_results'):
            self.mcp_results = MCPResults(self)
        self.mcp_results.update_status(self.function, self.bus_status)
        self.mcp_results.open()
   
    def stop_mcp_test(self, instance=None):
        ''' Stop and unschedule the MCP test. '''
        if self.mcp_task:
            self.mcp_task.cancel()
            self.mcp_task = None
            if hasattr(self, 'mcp_dialog'):
                self.mcp_dialog.close()
            if hasattr(self, 'mcp'):
                self.mcp.stop_cycle()
            self.show_mcp_results()


if __name__ == '__main__':
    StressTestApp().run()