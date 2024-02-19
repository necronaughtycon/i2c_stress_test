''' 
This module contains the classes for the MCP test dialog and the MCP test results dialog. 
'''

from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)
from kivymd.uix.progressindicator.progressindicator import MDCircularProgressIndicator


class MCPDialog:
    ''' This class handles the MCP test dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Content setup.
        self.function = MDListItemSupportingText(text='Function: None', halign='center')
        self.mode = MDListItemSupportingText(text='Mode: None', halign='center')
        self.delay = MDListItemSupportingText(text='Delay: 0', halign='center')
        self.pin_values = MDListItemSupportingText(text='MTR: off  |  V1: off  |  V2: off  |  V5: off', halign='center')
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
 
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.function))
        self.container.add_widget(MDListItem(self.mode))
        self.container.add_widget(MDListItem(self.pin_values))
        self.container.add_widget(MDListItem(self.delay))
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDBoxLayout(size_hint_y=None, height='20dp'))
        self.container.add_widget(self.progress)


        # Button setup.
        self.button_container = MDDialogButtonContainer()
        self.button = MDButton(
            style='elevated', theme_width='Custom', size_hint_y=None,
            height='48dp', radius=7, size_hint_x=.5, on_press=lambda x: self.close()
        )
        self.button_text = MDButtonText(
            text='Stop', font_style='Title', role='large',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.button.add_widget(self.button_text)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.button_container.add_widget(self.button)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        
        # Dialog setup.
        self.dialog = MDDialog(
            MDDialogHeadlineText(text='Live ADC Test Statistics'),
            self.container,
            self.button_container
        )

    def _create_container(self):
        container = MDDialogContentContainer(orientation='vertical')
        return container

    def update_information(self, function, mode, values, delay):
        self.function.text = f'Function: {function}'
        self.mode.text = f'Mode: {mode}'
        self.pin_values.text = values
        self.delay.text = f'Delay: {delay}'

    
    def open(self):
        self.dialog.open()
    
    def close(self):
        self.dialog.dismiss()


class MCPResults:
    ''' This class handles the MCP test results dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Content setup.
        self.function = MDListItemSupportingText(text='Function:', halign='center')
        self.bus_status = MDListItemSupportingText(text='Bus Status:', halign='center')
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
 
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.function))
        self.container.add_widget(MDListItem(self.bus_status))
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDBoxLayout(size_hint_y=None, height='20dp'))

        # Button setup.
        self.button_container = MDDialogButtonContainer()
        self.button = MDButton(
            style='elevated', theme_width='Custom', size_hint_y=None,
            height='48dp', radius=7, size_hint_x=.5, on_press=lambda x: self.close()
        )
        self.button_text = MDButtonText(
            text='Exit', font_style='Title', role='large',
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.button.add_widget(self.button_text)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.button_container.add_widget(self.button)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.result = MDDialogIcon(theme_icon_color='Custom')
        
        # Dialog setup.
        self.dialog = MDDialog(
            self.result,
            MDDialogHeadlineText(text='MCP Test Results'),
            self.container,
            self.button_container
        )
    
    def _create_container(self):
        container = MDDialogContentContainer(orientation='vertical')
        return container

    def update_status(self, function, status):
        self.function.text = f'Function: {function}'
        self.bus_status.text = f'Bus Status: {status}'
        if 'ok' in status.lower():
            self.result.icon = 'check-circle-outline'
            self.result.icon_color = 'green'
        else:
            self.result.icon = 'alert-circle-outline'
            self.result.icon_color = 'red'
    
    def open(self):
        self.dialog.open()
    
    def close(self):
        self.dialog.dismiss()