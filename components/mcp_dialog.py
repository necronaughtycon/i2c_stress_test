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
from kivymd.uix.label import MDLabel  # Add this line
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)


class MCPDialog:
    ''' This class handles the MCP test dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Content setup.
        self.function = MDListItemSupportingText(text='Function: None', halign='center')
        self.mode = MDListItemSupportingText(text='Mode: None', halign='center')
        self.pin_delay = MDListItemSupportingText(text='Pin Delay: 0', halign='center')
        self.cycle_delay = MDListItemSupportingText(text='Cycle Delay: 0', halign='center')
        self.motor = MDLabel(text='MOTOR', halign='center', theme_text_color='Custom', text_color='white', opacity=0.5)
        self.v1 = MDLabel(text='V1', halign='center', theme_text_color='Custom', text_color='white', opacity=0.5)
        self.v2 = MDLabel(text='V2', halign='center', theme_text_color='Custom', text_color='white', opacity=0.5)
        self.v5 = MDLabel(text='V5', halign='center', theme_text_color='Custom', text_color='white', opacity=0.5)
        
 
        # Pin value setup.
        self.value_container = MDBoxLayout(orientation='horizontal', size_hint_y=None, height='20dp')
        self.value_container.add_widget(self.motor)
        self.value_container.add_widget(self.v1)
        self.value_container.add_widget(self.v2)
        self.value_container.add_widget(self.v5)
        
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.function))
        self.container.add_widget(MDListItem(self.mode))
        self.container.add_widget(MDListItem(self.pin_delay))
        self.container.add_widget(MDListItem(self.cycle_delay))
        self.container.add_widget(MDDivider())
        self.container.add_widget(Widget(size_hint_x=.25))
        self.container.add_widget(self.value_container)
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDBoxLayout(size_hint_y=None, height='20dp'))

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
            MDDialogHeadlineText(text='Live MCP Test Statistics'),
            self.container,
            self.button_container
        )

    def _create_container(self):
        container = MDDialogContentContainer(orientation='vertical')
        return container

    def update_information(self, function, mode, pin_delay, cycle_delay, motor, v1, v2, v5):
        self.function.text = f'Function: {function}'
        self.mode.text = f'Mode: {mode}'
        self.pin_delay.text = f'Pin Delay: {pin_delay}'
        self.cycle_delay.text = f'Cycle Delay: {cycle_delay}'
        if motor:
            self.motor.text_color = 'green'
            self.motor.opacity = 1
        else:
            self.motor.text_color = 'white'
            self.motor.opacity = 0.2
        if v1:
            self.v1.text_color = 'green'
            self.v1.opacity = 1
        else:
            self.v1.text_color = 'white'
            self.v1.opacity = 0.2
        if v2:
            self.v2.text_color = 'green'
            self.v2.opacity = 1
        else:
            self.v2.text_color = 'white'
            self.v2.opacity = 0.2
        if v5:
            self.v5.text_color = 'green'
            self.v5.opacity = 1
        else:
            self.v5.text_color = 'white'
            self.v5.opacity = 0.2


    
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