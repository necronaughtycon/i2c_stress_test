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
        self.payload = MDListItemSupportingText(text='Payload Size:', halign='center')
        self.requests_received = MDListItemSupportingText(text='Requests Received:', halign='center')
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
 
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.payload))
        self.container.add_widget(MDListItem(self.requests_received))
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

    def update_information(self, payload, received):
        self.payload.text = f'Payload Size: {payload}'
        self.requests_received.text = f'Requests Received: {received}'
    
    def open(self):
        self.dialog.open()
    
    def close(self):
        print('Closing dialog')
        self.dialog.dismiss()


class ADCResults:
    ''' This class handles the ADC test results dialog. '''
    def __init__(self, app, **kwargs):
        self.app = app
        
        # Content setup.
        self.payload = MDListItemSupportingText(text='Payload Size:', halign='center')
        self.requests_received = MDListItemSupportingText(text='Requests Received:', halign='center')
        self.bus_status = MDListItemSupportingText(text='Bus Status:', halign='center')
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )
 
        # Container setup.
        self.container = self._create_container()
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.payload))
        self.container.add_widget(MDListItem(self.requests_received))
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
        self.result = MDDialogIcon()
        
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

    def update_information(self, payload, received, status):
        self.payload.text = f'Payload Size: {payload}'
        self.requests_received.text = f'Requests Received: {received}'
        self.bus_status.text = f'Bus Status: {status}'
        if 'ok' in status.lower():
            self.result.icon = 'check-circle-outline'
    
    def open(self):
        self.dialog.open()
    
    def close(self):
        print('Closing dialog')
        self.dialog.dismiss()