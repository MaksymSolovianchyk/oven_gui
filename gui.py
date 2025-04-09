from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

from widgets.rounded_button import RoundedButton

from screens.main_screen import MainScreen
from screens.second_screen import SecondScreen
from screens.standard_screen import StandardScreen
from screens.program_screen import ProgramScreen
from screens.settings_screen import SettingsScreen
from screens.run_screen import RunScreen

Window.size = (800, 480)

class MyScreenApp(App):
    def build(self):
        # Load the RoundedButton widget first
        Builder.load_file("widgets/rounded_button.kv")

        # Load all screen layout .kv files
        Builder.load_file("screens/main_screen.kv")
        Builder.load_file("screens/second_screen.kv")
        Builder.load_file("screens/standard_screen.kv")
        Builder.load_file("screens/program_screen.kv")
        Builder.load_file("screens/settings_screen.kv")
        Builder.load_file("screens/run_screen.kv")

        # Load the main layout (after screens are defined)
        Builder.load_file("main.kv")

        # Set up screen manager and add screens
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(SecondScreen(name='second'))
        screen_manager.add_widget(StandardScreen(name='standard_screen'))
        screen_manager.add_widget(ProgramScreen(name='program_screen'))
        screen_manager.add_widget(SettingsScreen(name='settings_screen'))
        screen_manager.add_widget(RunScreen(name='run_screen'))

        return screen_manager

if __name__ == '__main__':
    MyScreenApp().run()