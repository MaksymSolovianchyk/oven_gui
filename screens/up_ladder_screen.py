from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class UpLadderScreen(Screen):

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'