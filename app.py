from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import (
    ScreenManager,
    NoTransition
)
from kivy.clock import Clock

# import busio
# import board
# from adafruit_ads1x15.ads1115 import ADS1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
# from adafruit_mcp230xx.mcp23017 import MCP23017
# from digitalio import Direction

# Initialize I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)



class MainScreen(MDScreen):
    pass


class ConfigScreen(MDScreen):
    test_type = StringProperty('')


class StressTestApp(MDApp):
    ''' Main application class. '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())


    def build(self):
        ''' Create the application. '''
        self.theme_cls.theme_style = 'Dark'
        self.setup_screens()
        return self.sm

    def screen_config(self):
        ''' Define the screens and their kv files. '''
        return {
            'main_screen': {'path': 'main_screen.kv', 'class': MainScreen},
            'config_screen': {'path': 'config_screen.kv', 'class': ConfigScreen}
        }

    def load_kv_file(self, info):
        ''' Load the kv file for a screen. '''
        Builder.load_file(f'views/{info["path"]}')

    def setup_screens(self):
        ''' Create the screens and add them to the screen manager. '''
        screens = self.screen_config()
        for name, info in screens.items():
            self.load_kv_file(info)
            self.sm.add_widget(info['class'](name=name))


if __name__ == '__main__':
    StressTestApp().run()
