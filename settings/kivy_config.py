''' Settings required to run on the Comfile. '''

from kivy.config import Config

Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'show_cursor', '1')
Config.set('graphics', 'width', '800')

Config.write()