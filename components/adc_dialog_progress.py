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
from kivymd.uix.progressindicator.progressindicator import MDCircularProgressIndicator


class BaseDialog:
    '''Base class for dialogs with common functionalities.'''
    def __init__(self, app, header_text, btn_text, progress=None, result=None, **kwargs):
        self.app = app

        # Content setup.
        self.payload = MDListItemSupportingText(text='Payload Size:', halign='center')
        self.requests_received = MDListItemSupportingText(text='Requests Received:', halign='center')

        # Container setup.
        self.container = MDDialogContentContainer(orientation='vertical')
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDListItem(self.payload))
        self.container.add_widget(MDListItem(self.requests_received))
        self.container.add_widget(MDDivider())
        self.container.add_widget(MDBoxLayout(size_hint_y=None, height='20dp'))
        if progress:
            self.container.add_widget(progress)

        # Button setup.
        self.button_container = MDDialogButtonContainer()
        self.create_button(btn_text)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.button_container.add_widget(self.button)
        self.button_container.add_widget(Widget(size_hint_x=.25))
        self.result = MDDialogIcon()
        
        # Dialog setup.
        self.dialog = MDDialog()
        if result:
            self.dialog.add_widget(result)
        self.dialog.add_widget(MDDialogHeadlineText(text=header_text))
        self.dialog.add_widget(self.container)
        self.dialog.add_widget(self.button_container)

    def create_button(self, btn_txt):
        self.button = MDButton(
            MDButtonText(
                text=btn_txt,
                font_style='Title',
                role='large',
                pos_hint={'center_x': .5, 'center_y': .5}    
            ),
            style='elevated',
            theme_width='Custom',
            size_hint_y=None,
            height='48dp',
            radius=7,
            on_press=lambda x: self.close()
        )

    def update_information(self, payload, received, bus_status=None):
        self.payload.text = f'Payload Size: {payload}'
        self.requests_received.text = f'Requests Received: {received}'
        if bus_status:
            self.bus_status.text = f'Bus Status: {bus_status}'

    def open(self):
        self.dialog.open()

    def close(self):
        self.dialog.dismiss()


class ADCDialog(BaseDialog):
    ''' This class handles the ADC test dialog. '''
    def __init__(self, app, **kwargs):
        super().__init__(app, 'Live ADC Test Statistics', 'Stop', **kwargs)
        self.setup_content()

    def setup_content(self):
        self.progress = MDCircularProgressIndicator(
            size_hint=(None, None), size=('40dp', '40dp'),
            pos_hint={'center_x': .5, 'center_y': .1}
        )


class ADCResults(BaseDialog):
    ''' This class handles the ADC test results dialog. '''
    def __init__(self, app, **kwargs):
        super().__init__(app, 'ADC Test Results', 'Exit', **kwargs)
        self.setup_content()

    def setup_content(self):
        self.bus_status = MDListItemSupportingText(text='Bus Status:', halign='center')
        self.result = MDDialogIcon()