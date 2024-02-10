from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import (
    ScreenManager,
    NoTransition
)

import time


from kivy.clock import Clock
from kivy.utils import hex_colormap



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

    current_theme = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())
        self.color_index = 0
        self.color_keys = list(hex_colormap.keys())
        self.current_theme = self.color_keys[self.color_index].capitalize()

    def build(self):
        ''' Create the application. '''
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = self.color_keys[self.color_index].capitalize()
        self.setup_screens()
        Clock.schedule_interval(self.change_theme_color, .5)
        return self.sm
    
    def change_theme_color(self, dt):
        ''' Cycles through themes. '''
        self.color_index = (self.color_index + 1) % len(self.color_keys)
        self.theme_cls.primary_palette = self.color_keys[self.color_index].capitalize()
        self.current_theme = self.color_keys[self.color_index].capitalize()

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