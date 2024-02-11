import time
from collections import deque

from kivy.lang import Builder
from kivy.properties import (
    StringProperty, NumericProperty,
    DictProperty, ListProperty, ObjectProperty
)
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)
# from adafruit_mcp230xx.mcp23017 import MCP23017
# from digitalio import Direction
# Initialize I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)


class ADCTestScreen(MDScreen):
    pass


class MCPTestScreen(MDScreen):
    pass


class ADCDialog:
    ''' This class is a dialog that displays live statistics for an ongoing ADC test. '''
    def __init__(self, **kwargs):
        super(ADCDialog, self).__init__(**kwargs)
        
        # Dialog content layout
        self.content = MDDialog(MDDialogHeadlineText(text='Live ADC Test Statistics'))
        self.container = MDDialogContentContainer(orientation='vertical')
        self.container.add_widget(MDDivider())
        self.payload = MDListItemSupportingText(
            text='Payload Size: 0', 
            halign='center'
            )
        self.container.add_widget(MDListItem(self.payload))
        self.requests_received = MDListItem(
            MDListItemSupportingText(
                text='Requests Received: 0',
                halign='center'
            )
        )
        self.container.add_widget(self.requests_received)
        self.container.add_widget(MDDivider())
        self.content.add_widget(self.container)
        self.button_container = MDDialogButtonContainer()
        self.button = MDButton(
            style='elevated',
            theme_width='Custom',
            size_hint_y=None,
            height='48dp',
            radius=7,
            size_hint_x=.5
        )
        self.button.bind(on_release=self.stop_adc_test)
        self.button_text = MDButtonText(
            text='Stop',
            font_style='Title',
            role='large',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.button.add_widget(self.button_text)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.button_container.add_widget(self.button)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.content.add_widget(self.button_container)
    
    def update_payload_size(self, size):
        self.payload.text = f'Payload Size: {size}'
    
    def update_requests_sent(self, requests):
        self.requests_received.text = f'Requests Sent: {requests}'
    
    def open(self):
        self.content.open()
    
    def close(self):
        self.content.dismiss()
    
    def stop_adc_test(self, instance):
        # Implement stopping logic here, possibly using a callback to the parent app
        self.close()
    


class StressTestApp(MDApp):
    ''' Main application class. '''

    adc_requests = NumericProperty(0)
    adc_stored = ListProperty([])
    adc_task = None
    adc_requests_received = NumericProperty(0)

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
        self.adc_requests_received = 0
        # self.show_adc_dialog()
        self.show_adc_dialog_new()
        self.adc_task = Clock.schedule_interval(lambda dt: self.handle_adc_data(data_held), int(frequency))
    
    def show_adc_dialog_new(self):
        if not hasattr(self, 'adc_dialog'):
            self.adc_dialog = ADCDialog()
            self.adc_dialog.button.bind(on_release=self.stop_adc_test)
    
        self.adc_dialog.update_payload_size(self.adc_requests)
        self.adc_dialog.update_requests_sent(self.adc_requests_received)
        self.adc_dialog.open()





    def handle_adc_data(self, data_held):
        ''' Handle the ADC data. '''
        requests_sent = 0
        for request in range(self.adc_requests):
            # Do something (print a number for now).
            requests_sent += 1
            data_held.append(requests_sent)
            self.adc_requests_received += 1
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
            MDDialogHeadlineText(text="Live ADC Test Statistics"),
            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemSupportingText(
                        text=f'Payload Size: {self.adc_requests}',
                        halign='center'
                        )
                ),
                MDListItem(
                    MDListItemSupportingText(text=f'Requests Sent: {self.adc_requests_received}')
                ),
                MDDivider(),
                orientation = 'vertical'
            ),
            MDDialogButtonContainer(
                Widget(size_hint_x=.25),
                MDButton(
                    MDButtonText(
                        text='Stop',
                        font_style='Title',
                        role='large',
                        pos_hint={'center_x': .5, 'center_y': .5}
                        ),
                    style='elevated',
                    theme_width='Custom',
                    size_hint_y=None,
                    height='48dp',
                    radius=7,
                    size_hint_x=.5
                ),
                Widget(size_hint_x=.25)
            ),
        ).open()

if __name__ == '__main__':
    StressTestApp().run()