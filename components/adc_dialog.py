''' 
This module contains the classes for the ADC test dialog and the ADC test results dialog. 
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


class ADCDialog:
    ''' This class handles the ADC test dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Content setup.
        self.requests = MDListItemSupportingText(text='Payload Size: 0', halign='center')
        self.requests_filled = MDListItemSupportingText(text='Requests Received: 0', halign='center')
        self.last_payload = MDListItemSupportingText(text='Last Payload: None', halign='center')
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
 
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.requests))
        self.container.add_widget(MDListItem(self.requests_filled))
        self.container.add_widget(MDListItem(self.last_payload))
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

    def update_information(self, requests, requests_filled, last_payload):
        self.requests.text = f'Payload Size: {requests}'
        self.requests_filled.text = f'Requests Received: {requests_filled}'
        self.last_payload.text = f'Last Payload: {last_payload}'
    
    def open(self):
        self.dialog.open()
    
    def close(self):
        self.dialog.dismiss()


class ADCResults:
    ''' This class handles the ADC test results dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Content setup.
        self.payload = MDListItemSupportingText(text='Payload Size:', halign='center')
        self.requests_filled = MDListItemSupportingText(text='Requests Received:', halign='center')
        self.bus_status = MDListItemSupportingText(text='Bus Status:', halign='center')
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
 
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.payload))
        self.container.add_widget(MDListItem(self.requests_filled))
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
            MDDialogHeadlineText(text='ADC Test Results'),
            self.container,
            self.button_container
        )
    
    def _create_container(self):
        container = MDDialogContentContainer(orientation='vertical')
        return container

    def update_status(self, payload, requests_filled, status):
        self.payload.text = f'Payload Size: {payload}'
        self.requests_filled.text = f'Requests Received: {requests_filled}'
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