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
from scripts import sensor_read   # This is your module that has get_temperature()
from screens import standard_screen as sts
from kivy.uix.popup import Popup

current_temp = int(0)
time_left = int(0)

class RunScreen(Screen):
    cur_temp = StringProperty(str(int(current_temp)))
    cur_color = ListProperty([1, 1, 1, 1])
    time_left_text = StringProperty(str(time_left))

    def start_run(self):
        self.start_time = None  # Set to None until actual start
        self.live_time = []
        self.live_temp = []
        self.run_started = False  # Flag to start timer only once
        self.time_left_text = "HEATING"

    def show_yes_no_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Message
        message = Label(text="Cancel the process?")

        # Button layout
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')

        # Yes button
        yes_button = Button(text="Yes")
        # No button
        no_button = Button(text="No")

        # Create popup
        popup = Popup(title="Confirmation",
                      content=content,
                      size_hint=(0.7, 0.4),
                      auto_dismiss=False)

        # Bind buttons
        yes_button.bind(on_press=lambda *args: self.on_yes(popup))
        no_button.bind(on_press=popup.dismiss)

        # Add widgets
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(message)
        content.add_widget(button_layout)

        # Show the popup
        popup.open()

    def on_yes(self, popup):
        popup.dismiss()
        sts.apply=0


    def pop_up_screen(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        message = Label(text="Execution Complete")
        close_button = Button(text="OK", size_hint=(1, 0.4))
        popup = Popup(title="Alert", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(message)
        content.add_widget(close_button)
        popup.open()

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

        self.live_time = []
        self.live_temp = []
        self.run_started = False
        self.start_time = None

        Clock.schedule_interval(self.update_plot, 1)
        Clock.schedule_interval(self.update_time_left, 1)

    def update_time_left(self, dt):
        if sts.apply and self.run_started:
            elapsed = time.time() - self.start_time
            global time_left
            target_time = sts.target_timer * 60  # Convert minutes to seconds
            time_left = max(0, target_time - elapsed)

            hours = int(time_left) // 3600
            minutes = (int(time_left) % 3600) // 60
            seconds = int(time_left) % 60

            self.time_left_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            if time_left == 0:
                self.pop_up_screen()
                sts.apply = False

        elif sts.apply and not self.run_started:
            self.time_left_text = "HEATING..."

    def update_plot(self, dt):
        if sts.apply:
            target_temp = sts.target_temp
            target_time = sts.target_timer

            global current_temp
            current_temp = sensor_read.get_temperature()
            self.cur_temp = str(int(current_temp))

            # Start countdown only once
            if abs(current_temp - target_temp) <= 3 and not self.run_started:
                self.start_time = time.time()
                self.run_started = True

            # Temp label color
            if abs(current_temp - target_temp) <= 3:
                self.cur_color = [0, 1, 0, 1]  # Green
            elif current_temp > target_temp + 3:
                self.cur_color = [1, 0, 0, 1]  # Red
            elif current_temp < target_temp - 3:
                self.cur_color = [0, 0.5, 1, 1]  # Blue

            # Collect data
            if current_temp is not None and self.run_started:
                elapsed = time.time() - self.start_time
                self.live_time.append(elapsed)
                self.live_temp.append(current_temp)

                # Keep only the last 10 minutes
                window_seconds = 600
                while self.live_time and (self.live_time[-1] - self.live_time[0]) > window_seconds:
                    self.live_time.pop(0)
                    self.live_temp.pop(0)

            # === Only initialize lines once ===
            if not hasattr(self, 'live_line'):
                # Target line
                self.target_line, = self.ax.plot(
                    [0, target_time * 60],
                    [target_temp, target_temp],
                    label='Target Temperature',
                    color='blue',
                    linestyle='--'
                )

                # Live sensor line
                self.live_line, = self.ax.plot(
                    self.live_time,
                    self.live_temp,
                    label='Live Sensor Temp',
                    color='red'
                )

                self.ax.set_xlabel('Time (s)')
                self.ax.set_ylabel('Temperature (°C)')
                self.ax.legend()

            # === Update the existing lines ===
            self.live_line.set_data(self.live_time, self.live_temp)
            self.target_line.set_data([0, target_time * 60], [target_temp, target_temp])

            # Update axis limits
            if self.live_time:
                end_time = self.live_time[-1]
                start_time = max(0, end_time - 600)
                self.ax.set_xlim(start_time, end_time + 10)

            y_vals = self.live_temp + [target_temp]
            if y_vals:
                self.ax.set_ylim(min(y_vals) - 5, max(y_vals) + 5)

            self.fig.canvas.draw_idle()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'standard_screen'
