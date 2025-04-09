from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class SecondScreen(Screen):
    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'
    def go_to_standard(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'standard_screen'
    def go_to_program(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'program_screen'
    def go_to_settings(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'settings_screen'
