from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from screens.program_screen import time, temp


class UpLadderScreen(Screen):
    temp_text = StringProperty("")
    time_text = StringProperty("")
    graph_source = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'program_screen'

    def run(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'run_screen'