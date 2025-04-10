from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import csv
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'

    def open_file_picker(self):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_selection=lambda *x: self.on_file_selected(file_chooser.selection))

        # Layouts
        layout = BoxLayout(orientation='vertical')
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, padding=10, spacing=10)

        # Buttons
        open_button = Button(
            text="Open",
            font_size=12,
            size_hint=(None, None),
            size=(80, 30)
        )
        close_button = Button(
            text="Close",
            font_size=12,
            size_hint=(None, None),
            size=(80, 30)
        )

        # Popup reference needs to be defined before it's used in lambda
        popup = Popup(title="Select a file", size_hint=(0.8, 0.8))
        open_button.bind(on_press=lambda instance: self.confirm_selection(file_chooser.selection, popup))
        close_button.bind(on_press=lambda instance: self.close_popup(popup))

        # Assemble layout
        button_layout.add_widget(close_button)
        button_layout.add_widget(open_button)
        layout.add_widget(file_chooser)
        layout.add_widget(button_layout)

        popup.content = layout
        popup.open()

    def confirm_selection(self, selection, popup):
        if selection:
            file_path = selection[0]
            if not file_path.lower().endswith('.csv'):
                error_popup = Popup(
                    title="Invalid File",
                    content=Label(text="Please select a CSV file."),
                    size_hint=(0.6, 0.3)
                )
                error_popup.open()
            else:
                self.parse_file(file_path)
                popup.dismiss()

    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, temp1, temp2, time1, time2 = row
                self.create_button(name, temp1, temp2, time1, time2)

    def create_button(self, name, temp1, temp2, time1, time2):
        new_button = Button(
            text=name,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            size=(600, 250),
            font_size=16
        )
        new_button.bind(on_press=lambda instance: self.on_button_pressed(name, temp1, temp2, time1, time2))
        self.ids.program_screen_container.add_widget(new_button)

    def on_button_pressed(self, name, temp1, temp2, time1, time2):
        print(f"{name} pressed! Temp1: {temp1}, Temp2: {temp2}, Time1: {time1}, Time2: {time2}")

    def close_popup(self, popup):
        popup.dismiss()
