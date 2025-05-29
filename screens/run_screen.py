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
from screens import standard_screen as sts
from kivy.uix.popup import Popup
from scripts import gpio
from screens import up_ladder_screen as uls
import math
from threading import Thread
current_temp = int(0)
time_left = int(0)


class RunScreen(Screen):
    cur_temp = StringProperty(str(int(current_temp)))
    cur_color = ListProperty([1, 1, 1, 1])
    time_left_text = StringProperty(str(time_left))

    def load_temp(self, temp):
        self.target_temp = temp

    def load_time(self, tme):
        self.target_time = tme

    def start_run(self):
        self.start_time = None
        self.live_time = []
        self.live_temp = []
        self.run_started = False
        self.time_left_text = "Reaching SetP..."


    def safe_get_temp(self):
        try:
            t1 = time.time()
            temp = sensor_read.get_average_temperature()
            t2 = time.time()
            #print(f"Sensor read: {temp}, took {t2 - t1:.3f} sec")
            if temp is None or math.isnan(temp) or temp > 500:
                print("Invalid temperature reading")
                return None
            return temp
        except Exception as e:
            print(f"Sensor read error: {e}")
            return None

    def sensor_polling_loop(self):
        while True:
            self.latest_temp = self.safe_get_temp()
            time.sleep(0.5)

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
        sts.apply = 0

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
        gpio.heater_off()
        #print("in runscreen")
        Thread(target=self.sensor_polling_loop, daemon=True).start()

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
        self.run_started = False
        self.start_time = None
        self.live_line = None
        self.target_line = None

        Clock.schedule_interval(self.update_plot, 1)
        Clock.schedule_interval(self.update_time_left, 1)

    def update_time_left(self, dt):
        if sts.apply and self.run_started:
            elapsed = time.time() - self.start_time
            global time_left
            target_time = sts.target_timer * 60
            time_left = max(0, target_time - elapsed)

            hours = int(time_left) // 3600
            minutes = (int(time_left) % 3600) // 60
            seconds = int(time_left) % 60
            self.time_left_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            if time_left == 0:
                self.pop_up_screen()
                sts.apply = False

        elif sts.apply and not self.run_started:
            self.time_left_text = "Reaching SetP..."

    def update_plot(self, dt):
        if uls.apply:
            return
        if not sts.apply:
            gpio.heater_off()
            print("in runscreen")
            return

        target_temp = self.target_temp
        target_time = self.target_time

        global current_temp
        current_temp = self.latest_temp
        self.cur_temp = str(int(current_temp))

        # Start countdown only once
        if abs(current_temp - target_temp) <= 1.5 and not self.run_started:
            self.start_time = time.time()
            self.run_started = True
            self.live_time.clear()
            self.live_temp.clear()

        # Temp label color
        if abs(current_temp - target_temp) <= 1:
            self.cur_color = [0, 1, 0, 1]  # Green
        elif current_temp > target_temp + 1.5:
            self.cur_color = [1, 0, 0, 1]  # Red
            gpio.heater_off()
            print("Heater off")
            print("in runscreen")

        elif current_temp < target_temp - 1.5:
            self.cur_color = [0, 0.5, 1, 1]  # Blue
            gpio.heater_on()
            print("Heater on")
            print("in runscreen")



        # Collect data
        if self.run_started:
            elapsed = time.time() - self.start_time
            self.live_time.append(elapsed)
            self.live_temp.append(current_temp)

            # Efficient sliding window (last 10 minutes only)
            window_seconds = 600
            while self.live_time and (self.live_time[-1] - self.live_time[0]) > window_seconds:
                self.live_time.pop(0)
                self.live_temp.pop(0)

            # Initialize lines only once
            if not self.live_line:
                self.target_line, = self.ax.plot([0, target_time * 60],
                                                 [target_temp, target_temp],
                                                 label='Target Temperature',
                                                 color='blue', linestyle='--')
                self.live_line, = self.ax.plot(self.live_time,
                                               self.live_temp,
                                               label='Live Sensor Temp',
                                               color='red')
                self.ax.legend()

            # Update data
            self.live_line.set_data(self.live_time, self.live_temp)
            self.target_line.set_data([0, target_time * 60], [target_temp, target_temp])

            # Axis limits
            if self.live_time:
                end_time = self.live_time[-1]
                if end_time < 60:
                    # Initial small range
                    self.ax.set_xlim(0, 60)
                else:
                    # Rolling window of the last 10 minutes
                    start_time = max(0, end_time - 600)
                    self.ax.set_xlim(start_time, end_time + 10)

            y_vals = self.live_temp + [target_temp]
            if y_vals:
                self.ax.set_ylim(min(y_vals) - 5, max(y_vals) + 5)

            self.fig.canvas.draw_idle()

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'standard_screen'


    def go_sensor_status(self):
        sensor_stat=self.manager.get_screen('sensor_status')
        sensor_stat.parse_last_screen('run_screen')
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'sensor_status'
