from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window

simple_mode_temp = 190
extended_mode_temp = 50
low_mode_temp = 20

class CustomButton(ButtonBehavior, BoxLayout):
    def __init__(self, title, subtitle, description, image_path,temperature,time, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 150
        self.padding = [300, 10, 10, 10]
        self.spacing = 10
        self.title = title
        self.time = time
        self.temperature = temperature

        self.add_widget(Image(source=image_path, size_hint=(None, 1), width=100))

        text_box = BoxLayout(orientation='vertical', spacing=5)
        text_box.add_widget(Label(text=title, font_size=22, bold=True, halign='left', valign='middle'))
        text_box.add_widget(Label(text=subtitle, font_size=18, halign='left', valign='middle'))
        text_box.add_widget(Label(text=description, font_size=18, halign='left', valign='middle'))

        for label in text_box.children:
            label.bind(size=label.setter('text_size'))

        self.add_widget(text_box)

class ProgramScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.buttons = [
            CustomButton(
                title="Simple Mode",
                subtitle="Max Temperature: " + str(simple_mode_temp) + " °C",
                description="Total Duration: ",
                image_path="images/water.png",
                temperature=simple_mode_temp,
                time=12
            ),
            CustomButton(
                title="Extended",
                subtitle="Max Temperature: " + str(extended_mode_temp) + " °C",
                description="Total Duration: ",
                image_path="images/pump.png",
                temperature = extended_mode_temp,
                time = 20
            ),
            CustomButton(
                title="Low Temp",
                subtitle="Max Temperature: " + str(low_mode_temp) + " °C",
                description="Total Duration: ",
                image_path="images/logs.png",
                temperature = low_mode_temp,
                time = 3
            )
        ]

        for btn in self.buttons:
            self.layout.add_widget(btn)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)
        self.counter = 0
    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'second'

    def reorder(self):
            #By capital letter
        if self.counter == 0:
            self.buttons.sort(key=lambda btn: btn.title.lower())
            self.counter += 1
            self.layout.clear_widgets()
            for btn in self.buttons:
                self.layout.add_widget(btn)
            #By time ascending
        elif self.counter == 1:
            self.buttons.sort(key=lambda btn: btn.time)
            self.counter += 1
            self.layout.clear_widgets()
            for btn in self.buttons:
                self.layout.add_widget(btn)
            # By time descending
        elif self.counter == 2:
            self.buttons.sort(key=lambda btn: btn.time, reverse=True)
            self.counter +=1
            self.layout.clear_widgets()
            for btn in self.buttons:
                self.layout.add_widget(btn)
            # By temp ascending
        elif self.counter == 3:
            self.buttons.sort(key=lambda btn: btn.temperature)
            self.counter =+ 1
            self.layout.clear_widgets()
            for btn in self.buttons:
                self.layout.add_widget(btn)
            # By temp descending
        elif self.counter == 4:
            self.buttons.sort(key=lambda btn: btn.temperature,reverse=True)
            self.counter = 0
            self.layout.clear_widgets()
            for btn in self.buttons:
                self.layout.add_widget(btn)