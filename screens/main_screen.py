from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock
from datetime import datetime


class MainScreen(Screen):
    def on_enter(self):
        # Start updating time when screen is entered
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        now = datetime.now().strftime("%H:%M")
        self.ids.time_label.text = f"{now}"

    def go_to_next(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'second'

