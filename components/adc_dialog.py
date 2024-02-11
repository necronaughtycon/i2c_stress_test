from kivy.uix.widget import Widget
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




class ADCDialog:
    ''' This class handles the ADC test dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Container setup.
        self.container = MDDialogContentContainer(orientation='vertical')
        self.container.add_widget(MDDivider())
        self.payload = MDListItemSupportingText(text='Payload Size: 0', halign='center')
        self.requests_received = MDListItemSupportingText(text='Requests Received: 0', halign='center')
        self.container.add_widget(MDListItem(self.payload))
        self.container.add_widget(MDListItem(self.requests_received))
        self.container.add_widget(MDDivider())

        # Button setup.
        self.button_container = MDDialogButtonContainer()
        self.button = MDButton(
            style='elevated', theme_width='Custom', size_hint_y=None,
            height='48dp', radius=7, size_hint_x=.5,
            on_press=self.app.stop_adc_test
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
            MDDialogHeadlineText(
                text='Live ADC Test Statistics'
            ),
            self.container,
            self.button_container
        )
    
    def update_payload_size(self, size):
        self.payload.text = f'Payload Size: {size}'
    
    def update_requests_sent(self, requests):
        self.requests_received.text = f'Requests Sent: {requests}'
    
    def open(self):
        self.dialog.open()
    
    def close(self):
        self.dialog.dismiss()