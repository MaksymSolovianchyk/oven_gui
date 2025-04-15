from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.animation import Animation
from widgets.rounded_button import RoundedSmallButton
from kivy.uix.screenmanager import SlideTransition
from screens import program_screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

WATCHDOG_TIMEOUT = 5  # seconds
from widgets.preset import save_preset as preset_save, load_preset as preset_load, get_preset_names

apply = False

class StepData(Widget):
    target_temp = NumericProperty(50)
    target_time = NumericProperty(30)

    inc_temp = ObjectProperty(None, allownone=True)
    dec_temp = ObjectProperty(None, allownone=True)
    inc_time = ObjectProperty(None, allownone=True)
    dec_time = ObjectProperty(None, allownone=True)

    inc_temp_watchdog = ObjectProperty(None, allownone=True)
    dec_temp_watchdog = ObjectProperty(None, allownone=True)
    inc_time_watchdog = ObjectProperty(None, allownone=True)
    dec_time_watchdog = ObjectProperty(None, allownone=True)

class UpLadderScreen(Screen):
    temp_text = StringProperty("")
    time_text = StringProperty("")
    graph_source = StringProperty("")
    current_mode = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps = []

    def set_mode(self, mode, temp, time, graph):
        # Set mode-specific properties
        self.clear_steps()
        self.temp_text = str(temp)
        self.time_text = str(time)
        self.graph_source = graph

        # Based on the mode, add steps
        if mode == 'up_ladder':
            self.add_custom_steps_up()
            self.current_mode = 'up_ladder'
        elif mode == 'down_ladder':
            self.add_custom_steps_down()
            self.current_mode = 'down_ladder'
        elif mode == 'heating_ladder':
            self.add_custom_steps_heat()
            self.current_mode = 'heating_ladder'

    def clear_steps(self):
        # Clear the list of steps
        self.steps.clear()

        # Optionally, remove widgets from the UI (e.g., removing all children of the panel_content container)
        container = self.ids.panel_content
        container.clear_widgets()

    def add_custom_steps_up(self):
        self.add_step(65, 40)
        self.add_step(70, 50)

    def add_custom_steps_down(self):
        self.add_step(70, 50)
        self.add_step(40, 40)

    def add_custom_steps_heat(self):
        self.add_step(20, 40)
        self.add_step(50, 50)

    def add_step(self, target_temp, target_time):
        # Create and add steps (same as before)
        pass

    def add_custom_steps(self, preset):
        for step_info in preset:
            self.add_step(step_info['temp'], step_info['time'])

    def add_step(self, target_temp=20, target_time=30):
        step_data = StepData()
        step_data.target_temp = target_temp
        step_data.target_time = target_time
        self.steps.append(step_data)

        step_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=30,
                                padding=[20, 20, 0, 0])

        # Temp
        temp_box = BoxLayout(orientation='vertical', size_hint_x=None, width=100, spacing=5)
        temp_label = Label(text=str(step_data.target_temp), font_size=20, halign='center', valign='middle',
                           text_size=(100, None))
        temp_box.add_widget(
            Label(text="Target °C", font_size=24, halign='left', valign='middle', text_size=(100, None)))
        temp_box.add_widget(temp_label)
        temp_label.bind(text=step_data.setter('target_temp'))

        def update_temp_label():
            temp_label.text = str(step_data.target_temp)

        def increase_temp(dt=None):
            step_data.target_temp += 1
            update_temp_label()

        def decrease_temp(dt=None):
            if step_data.target_temp > 5:
                step_data.target_temp -= 1
                update_temp_label()

        def start_increase_temp(instance=None, touch=None):
            stop_increase_temp()
            step_data.inc_temp = Clock.schedule_interval(increase_temp, 0.1)
            step_data.inc_temp_watchdog = Clock.schedule_once(lambda dt: stop_increase_temp(), WATCHDOG_TIMEOUT)

        def stop_increase_temp():
            if step_data.inc_temp:
                Clock.unschedule(step_data.inc_temp)
                step_data.inc_temp = None
            if step_data.inc_temp_watchdog:
                Clock.unschedule(step_data.inc_temp_watchdog)
                step_data.inc_temp_watchdog = None

        def start_decrease_temp(instance=None, touch=None):
            stop_decrease_temp()
            step_data.dec_temp = Clock.schedule_interval(decrease_temp, 0.1)
            step_data.dec_temp_watchdog = Clock.schedule_once(lambda dt: stop_decrease_temp(), WATCHDOG_TIMEOUT)

        def stop_decrease_temp():
            if step_data.dec_temp:
                Clock.unschedule(step_data.dec_temp)
                step_data.dec_temp = None
            if step_data.dec_temp_watchdog:
                Clock.unschedule(step_data.dec_temp_watchdog)
                step_data.dec_temp_watchdog = None

        temp_btns = BoxLayout(orientation='vertical', size_hint_x=None, width=50, spacing=5)
        temp_btns.add_widget(RoundedSmallButton(text="+1", size_hint=(None, None), size=(50, 50),
                                                on_press=start_increase_temp,
                                                on_release=lambda x: stop_increase_temp()))
        temp_btns.add_widget(RoundedSmallButton(text="-1", size_hint=(None, None), size=(50, 50),
                                                on_press=start_decrease_temp,
                                                on_release=lambda x: stop_decrease_temp()))

        def format_time(minutes):
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours:02}:{mins:02}"

        # Timer
        time_box = BoxLayout(orientation='vertical', size_hint_x=None, width=100, spacing=5)
        # Time label
        time_label = Label(
            text=format_time(step_data.target_time),
            font_size=20, halign='center', valign='middle', text_size=(100, None)
        )
        time_box.add_widget(
            Label(text="Time", font_size=24, halign='left', valign='middle', text_size=(100, None)))
        time_box.add_widget(time_label)

        # Bind label text to formatted time string
        step_data.bind(target_time=lambda instance, value: setattr(time_label, 'text', format_time(value)))

        def update_time_label():
            time_label.text = str(step_data.target_time)

        def increase_time(instance=None, touch=None):
            step_data.target_time += 1  # the bind handles the label update

        def decrease_time(dt=None):
            if step_data.target_time > 0:
                step_data.target_time -= 1

        def start_increase_time(instance=None, touch=None):
            stop_increase_time()
            step_data.inc_time = Clock.schedule_interval(increase_time, 0.1)
            step_data.inc_time_watchdog = Clock.schedule_once(lambda dt: stop_increase_time(), WATCHDOG_TIMEOUT)

        def stop_increase_time():
            if step_data.inc_time:
                Clock.unschedule(step_data.inc_time)
                step_data.inc_time = None
            if step_data.inc_time_watchdog:
                Clock.unschedule(step_data.inc_time_watchdog)
                step_data.inc_time_watchdog = None

        def start_decrease_time(instance=None, touch=None):
            stop_decrease_time()
            step_data.dec_time = Clock.schedule_interval(decrease_time, 0.1)
            step_data.dec_time_watchdog = Clock.schedule_once(lambda dt: stop_decrease_time(), WATCHDOG_TIMEOUT)

        def stop_decrease_time():
            if step_data.dec_time:
                Clock.unschedule(step_data.dec_time)
                step_data.dec_time = None
            if step_data.dec_time_watchdog:
                Clock.unschedule(step_data.dec_time_watchdog)
                step_data.dec_time_watchdog = None

        time_btns = BoxLayout(orientation='vertical', size_hint_x=None, width=50, spacing=5)
        time_btns.add_widget(RoundedSmallButton(text="+1", size_hint=(None, None), size=(50, 50),
                                                on_press=start_increase_time,
                                                on_release=lambda x: stop_increase_time()))
        time_btns.add_widget(RoundedSmallButton(text="-1", size_hint=(None, None), size=(50, 50),
                                                on_press=start_decrease_time,
                                                on_release=lambda x: stop_decrease_time()))

        # Add to step layout
        step_layout.add_widget(temp_box)
        step_layout.add_widget(temp_btns)
        step_layout.add_widget(time_box)
        step_layout.add_widget(time_btns)

        self.ids.panel_content.add_widget(step_layout)

    def run(self):
        steps_info = [{'temp': step.target_temp, 'time': step.target_time} for step in self.steps]
        run_screen = self.manager.get_screen('program_run_screen')

        run_screen.load_program(steps_info)
        run_screen.start_run()  # Reset timers, graph, etc.

        self.manager.transition.direction = 'left'
        self.manager.current = 'program_run_screen'

        global apply
        apply = True
        print(steps_info)

    def delete_step(self):
        container = self.ids.panel_content
        if len(container.children) > 0:
            container.remove_widget(container.children[0])

    def graph_lookup(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'program_run_screen'

    def open_panel(self):
        panel = self.ids.sliding_panel
        new_x = 0 if panel.x < 0 else -panel.width  # toggle open/close
        Animation(x=new_x, duration=0.3, t='out_quad').start(panel)

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'program_screen'



    def save_current_preset(self):
        mode = self.current_mode  # assuming you store it when calling set_mode()
        preset_save(self, mode)

    def load_preset(self):
        from widgets.preset import get_preset_details
        import os

        preset_details = get_preset_details(self.current_mode)

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Scrollable area for preset buttons
        scrollview = ScrollView(size_hint=(1, 1))
        presets_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        presets_box.bind(minimum_height=presets_box.setter('height'))
        scrollview.add_widget(presets_box)

        if not preset_details:
            presets_box.add_widget(Label(text="No presets available.", size_hint_y=None, height=50))
        else:
            for detail in preset_details:
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

                # Load button
                load_btn = Button(
                    text=f"{detail['name']}",
                    size_hint_x=0.7
                )
                load_btn.bind(
                    on_release=lambda btn_instance, fname=detail['file_name']: self.load_selected_preset(fname))
                row.add_widget(load_btn)

                # Delete button
                delete_btn = Button(
                    text="Delete",
                    size_hint_x=0.3,
                    background_color=(1, 0, 0, 1)
                )
                delete_btn.bind(
                    on_release=lambda btn_instance, fname=detail['file_name']: self.delete_preset(fname, presets_box))
                row.add_widget(delete_btn)

                presets_box.add_widget(row)

        # Add scrollview to main content layout
        content.add_widget(scrollview)

        # Close button at the bottom
        close_btn = Button(text="Close", size_hint_y=None, height=50)
        content.add_widget(close_btn)

        self.popup = Popup(title="Load Preset", content=content, size_hint=(None, None), size=(450, 500))
        close_btn.bind(on_release=self.popup.dismiss)
        self.popup.open()
    def popup_dismiss(self, *args):
        self.popup.dismiss()

    def delete_preset(self, preset_name, presets_box):
        import os

        filepath = os.path.join("presets", preset_name)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted preset: {preset_name}")

        # Refresh popup UI after deletion
        self.popup.dismiss()
        self.load_preset()

    def load_selected_preset(self, preset_name):
        preset_load(self, preset_name)
        self.popup.dismiss()

    def delete_selected_preset(self, preset_name):
        from widgets.preset import delete_preset

        delete_preset(preset_name)
        self.popup.dismiss()  # Close the popup
        self.load_preset()  # Reopen to refresh list
