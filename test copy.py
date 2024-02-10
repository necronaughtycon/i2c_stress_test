from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup

class ADCDialog(BoxLayout):
    def __init__(self, **kwargs):
        super(ADCDialog, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.add_widget(Label(text='Live ADC Test Statistics'))
        
        self.payload_size = Label(text='Payload Size: 0')
        self.add_widget(self.payload_size)
        
        self.requests_sent = Label(text='Requests Sent: 0')
        self.add_widget(self.requests_sent)
        
        self.bus_status = Spinner(text='Bus Status: OK', values=('OK', 'Failed'))
        self.add_widget(self.bus_status)
        
        self.progress = ProgressBar(max=100)
        self.add_widget(self.progress)
        
        self.stop_button = Button(text='Stop')
        self.stop_button.bind(on_release=self.stop_adc_test)
        self.add_widget(self.stop_button)

    def stop_adc_test(self, instance):
        # Add your stop_adc_test logic here
        pass

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        button = Button(text="Show Dialog")
        button.bind(on_release=self.show_adc_dialog)
        main_layout.add_widget(button)
        return main_layout

    def show_adc_dialog(self, instance):
        dialog = ADCDialog()
        popup = Popup(title='ADC Test', content=dialog, size_hint=(0.5, 0.5))
        popup.open()

if __name__ == "__main__":
    MainApp().run()