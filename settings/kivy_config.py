''' Settings required to run on the Comfile. '''

from kivy.config import Config

# Uncomment the following lines for local testing.
Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'show_cursor', '1')
Config.set('graphics', 'width', '800')


# Uncomment the following lines for the Comfile.
# Config.set('graphics', 'borderless', '1')
# Config.set('graphics', 'height', '480')
# Config.set('graphics', 'resizable', '0')
# Config.set('graphics', 'show_cursor', '0')
# Config.set('graphics', 'width', '800')

Config.write()