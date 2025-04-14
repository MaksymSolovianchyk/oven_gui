from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.widget import Widget
from widgets.rounded_button import RoundedSmallButton
from kivy.animation import Animation

WATCHDOG_TIMEOUT = 2  # seconds


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps = []

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'program_screen'

    def run(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'run_screen'

    def open_panel(self):
        panel = self.ids.sliding_panel
        new_x = 0 if panel.x < 0 else -panel.width  # toggle open/close
        Animation(x=new_x, duration=0.3, t='out_quad').start(panel)

    def add_step(self):
        step_data = StepData()
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

    def delete_step(self):
        container = self.ids.panel_content
        if len(container.children) > 0:
            container.remove_widget(container.children[0])
