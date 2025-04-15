import kivy
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.clock import Clock
import time
from scripts import sensor_read
from screens import up_ladder_screen as uls
from kivy.uix.popup import Popup

current_temp = int(0)
time_left = int(0)


class ProgramRunScreen(Screen):
    cur_temp = StringProperty(str(int(current_temp)))
    cur_color = ListProperty([1, 1, 1, 1])
    time_left_text = StringProperty(str(time_left))
    graph_mode_text = StringProperty('Profile')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Temperature (°C)')

        self.graph_widget = FigureCanvasKivyAgg(self.fig)
        self.graph_widget.width = 640
        self.graph_widget.height = 480
        self.graph_widget.pos = [0, 20]
        self.ids.canvas_widget.add_widget(self.graph_widget)

        self.live_time = []
        self.live_temp = []
        self.program_time = []
        self.program_temp = []
        self.run_started = False
        self.start_time = None
        self.live_line = None
        self.target_line = None
        self.total_program_time = 0

        self.graph_mode = 'live'
        self.position_dot = None
        self.button_freeze = False

        Clock.schedule_interval(self.update_plot, 1)
        Clock.schedule_interval(self.update_time_left, 1)

    def load_program(self, steps):
        self.program_steps = steps
        self.program_time.clear()
        self.program_temp.clear()

        cumulative_time = 0
        for step in self.program_steps:
            temp = step['temp']
            duration = step['time'] * 60  # minutes to seconds

            self.program_time.append(cumulative_time)
            self.program_temp.append(temp)

            cumulative_time += duration
            self.program_time.append(cumulative_time)
            self.program_temp.append(temp)

        self.total_program_time = cumulative_time
        self.plot_target_profile()



    def plot_target_profile(self):
        self.ax.cla()
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Temperature (°C)')

        if self.program_time and self.program_temp:
            self.target_line, = self.ax.plot(self.program_time, self.program_temp,
                                             label='Target Program', color='blue', linestyle='--')

        self.ax.legend()
        self.fig.canvas.draw_idle()

    def start_run(self):
        self.start_time = None
        self.live_time.clear()
        self.live_temp.clear()
        self.run_started = False
        self.time_left_text = "Reaching SetP..."
        if self.live_line in self.ax.lines:
            self.live_line.remove()
        self.live_line = None

        if self.position_dot:
            self.position_dot.remove()
            self.position_dot = None

    def update_plot(self, dt):
        if not uls.apply:
            return

        global current_temp
        current_temp = sensor_read.get_temperature()
        self.cur_temp = str(int(current_temp))

        if self.run_started:
            elapsed = time.time() - self.start_time
        else:
            elapsed = 0

        target_temp = self.get_target_temp_at(elapsed)

        if abs(current_temp - target_temp) <= 3 and not self.run_started:
            self.start_time = time.time()
            self.run_started = True
            self.live_time.clear()
            self.live_temp.clear()

        if not self.run_started:
            return

        self.live_time.append(elapsed)
        self.live_temp.append(current_temp)

        window_seconds = 600
        while self.live_time and (self.live_time[-1] - self.live_time[0]) > window_seconds:
            self.live_time.pop(0)
            self.live_temp.pop(0)

        if self.graph_mode == 'live':
            if not self.live_line:
                self.live_line, = self.ax.plot(self.live_time, self.live_temp, label='Live Temp', color='red')
                self.ax.legend()

            self.live_line.set_data(self.live_time, self.live_temp)

            if self.live_time:
                end_time = self.live_time[-1]
                start_time = max(0, end_time - window_seconds)
                self.ax.set_xlim(start_time, end_time + 10)

            y_vals = self.live_temp + self.program_temp
            if y_vals:
                self.ax.set_ylim(min(y_vals) - 5, max(y_vals) + 5)

        if abs(current_temp - target_temp) <= 3:
            self.cur_color = [0, 1, 0, 1]
        elif current_temp > target_temp + 3:
            self.cur_color = [1, 0, 0, 1]
        elif current_temp < target_temp - 3:
            self.cur_color = [0, 0.5, 1, 1]

        self.fig.canvas.draw_idle()

    def get_target_temp_at(self, elapsed_time):
        if not self.program_time:
            return 0

        for i in range(len(self.program_time) - 1):
            if self.program_time[i] <= elapsed_time < self.program_time[i + 1]:
                return self.program_temp[i]

        return self.program_temp[-1]

    def update_time_left(self, dt):
        if uls.apply and self.run_started:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.total_program_time - elapsed)

            global time_left
            time_left = remaining

            hours = int(remaining) // 3600
            minutes = (int(remaining) % 3600) // 60
            seconds = int(remaining) % 60
            self.time_left_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            if remaining == 0:
                self.pop_up_screen()
                uls.apply = False

        elif uls.apply and not self.run_started:
            self.time_left_text = "Reaching SetP..."

    def change_graph(self):
        if self.button_freeze:
            return
        self.button_freeze = True
        Clock.schedule_once(self.unfreeze_button, 1)
        if self.graph_mode == 'live':
            self.graph_mode = 'full'
            self.graph_mode_text = 'Live'
        else:
            self.graph_mode = 'live'
            self.graph_mode_text = 'Profile'

        self.ax.cla()

        if self.graph_mode == 'full':
            self.ax.set_xlabel('Time (min)')
            self.ax.set_ylabel('Temperature (°C)')

            if self.program_time and self.program_temp:
                self.ax.plot([t / 60 for t in self.program_time], self.program_temp,
                             label='Target Program', color='blue', linestyle='--')

            if self.run_started:
                elapsed = time.time() - self.start_time
            else:
                elapsed = 0

            if self.position_dot and self.position_dot in self.ax.lines:
                self.ax.lines.remove(self.position_dot)
                self.position_dot = None

            self.position_dot, = self.ax.plot([elapsed / 60], [current_temp],
                                              'ro', markersize=8, label='Current Position')

            self.ax.legend()

        elif self.graph_mode == 'live':
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Temperature (°C)')

            if self.program_time and self.program_temp:
                self.target_line, = self.ax.plot(self.program_time, self.program_temp,
                                                 label='Target Program', color='blue', linestyle='--')

            if self.live_time and self.live_temp:
                self.live_line, = self.ax.plot(self.live_time, self.live_temp,
                                               label='Live Temp', color='red')

            self.ax.legend()

        self.fig.canvas.draw_idle()

    def show_yes_no_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        message = Label(text="Cancel the process?")
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        yes_button = Button(text="Yes")
        no_button = Button(text="No")
        popup = Popup(title="Confirmation", content=content, size_hint=(0.7, 0.4), auto_dismiss=False)
        yes_button.bind(on_press=lambda *args: self.on_yes(popup))
        no_button.bind(on_press=popup.dismiss)
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(message)
        content.add_widget(button_layout)
        popup.open()

    def on_yes(self, popup):
        popup.dismiss()
        uls.apply = 0

    def pop_up_screen(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        message = Label(text="Execution Complete")
        close_button = Button(text="OK", size_hint=(1, 0.4))
        popup = Popup(title="Alert", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(message)
        content.add_widget(close_button)
        popup.open()

    def unfreeze_button(self, dt):
        self.button_freeze = False

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'up_ladder_screen'
