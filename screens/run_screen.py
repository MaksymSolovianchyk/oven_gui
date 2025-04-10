import kivy
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.clock import Clock
from matplotlib.animation import FuncAnimation
import time
from scripts import sensor_read   # This is your module that has get_temperature()
# Assuming 'sts' is imported from the standard_screen module
from screens import standard_screen as sts

current_temp=int(0)
time_left=int(0)

class RunScreen(Screen):
    cur_temp = StringProperty(str(int(current_temp)))
    cur_color = ListProperty([1, 1, 1, 1])
    time_left_text = StringProperty(str(time_left))

    def start_run(self):
        self.start_time = time.time()
        self.live_time = []
        self.live_temp = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Temperature')

        self.graph_widget = FigureCanvasKivyAgg(self.fig)
        self.graph_widget.width = 640
        self.graph_widget.height = 480
        self.graph_widget.pos = [0, 20]
        self.ids.canvas_widget.add_widget(self.graph_widget)

        # For live data plotting

        #self.start_time = time.time()
        self.live_time = []
        self.live_temp = []

        Clock.schedule_interval(self.update_plot, 1)
        Clock.schedule_interval(self.update_time_left, 1)    # Update time_left once a minute

    def update_time_left(self, dt):
        if sts.apply and hasattr(self, "start_time"):
            elapsed = time.time() - self.start_time
            global time_left
            target_time = sts.target_timer * 60  # Convert minutes to seconds
            time_left = max(0, target_time - elapsed)

            hours = int(time_left) // 3600
            minutes = (int(time_left) % 3600) // 60
            seconds = int(time_left) % 60

            self.time_left_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_plot(self, dt):
        if sts.apply:
            target_temp = sts.target_temp
            target_time = sts.target_timer



            # === Live Sensor Reading ===
            global current_temp
            current_temp = sensor_read.get_temperature()
            self.cur_temp = str(int(current_temp))

            if abs(current_temp - target_temp) <= 3:
                self.cur_color = [0, 1, 0, 1]  # Green: within ±3°C of target
            elif current_temp > target_temp + 3:
                self.cur_color = [1, 0, 0, 1]  # Red: above target by more than 3°C
            elif current_temp < target_temp - 3:
                self.cur_color = [0, 0.5, 1, 1]  # Blue: below target by more than 3°C

            if current_temp is not None:
                elapsed = time.time() - self.start_time
                self.live_time.append(elapsed)
                self.live_temp.append(current_temp)

            # === Clear and Redraw Plot ===
            self.ax.clear()

            # Plot target temperature line
            self.ax.plot([0, target_time* 60], [target_temp, target_temp],
                         label='Target Temperature', color='blue', linestyle='--')

            # Plot live temperature readings
            if self.live_time:
                self.ax.plot(self.live_time, self.live_temp,
                             label='Live Sensor Temp', color='red')

            # Axis settings
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Temperature (°C)')
            self.ax.set_xlim(0, max(target_time, self.live_time[-1] if self.live_time else 0) + 10)

            y_vals = self.live_temp + [target_temp]
            if y_vals:
                self.ax.set_ylim(min(y_vals) - 5, max(y_vals) + 5)


            self.ax.legend()
            self.fig.canvas.draw()

    def go_back(self):
        # Transition back to the standard screen
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'standard_screen'

