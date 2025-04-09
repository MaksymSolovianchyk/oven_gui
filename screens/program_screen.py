from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window


class CustomButton(ButtonBehavior, BoxLayout):
    def __init__(self, title, subtitle, description, image_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 150
        self.padding = [300, 10, 10, 10]  # [left, top, right, bottom]
        self.spacing = 10

        # Image on the left
        self.add_widget(Image(source=image_path, size_hint=(None, 1), width=100))

        # Text area on the right
        text_box = BoxLayout(orientation='vertical', spacing=5)
        text_box.add_widget(Label(text=title, font_size=18, bold=True, halign='left', valign='middle'))
        text_box.add_widget(Label(text=subtitle, font_size=14, halign='left', valign='middle'))
        text_box.add_widget(Label(text=description, font_size=12, halign='left', valign='middle'))

        for label in text_box.children:
            label.bind(size=label.setter('text_size'))

        self.add_widget(text_box)


class ProgramScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        layout.bind(minimum_height=layout.setter('height'))

        # 3 custom buttons, each with unique image
        btn1 = CustomButton(
            title="Standard Mode",
            subtitle="Check water quality",
            description="View detailed metrics including pH, turbidity, and conductivity.",
            image_path="images/water.png"
        )

        btn2 = CustomButton(
            title="Extended",
            subtitle="Manage flow rates",
            description="Adjust and monitor pump activity in real time.",
            image_path="images/pump.png"
        )

        btn3 = CustomButton(
            title="Low Temp",
            subtitle="Review system history",
            description="Access recorded data from previous sessions for analysis.",
            image_path="images/logs.png"
        )

        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(layout)

        self.add_widget(scroll_view)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'second'