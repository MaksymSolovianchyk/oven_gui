from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


target_temp = 0
target_timer = 0
timer_minutes_first = 0
timer_minutes_second = 0
timer_hours_first = 0
timer_hours_second = 0
start_time = 0
apply = False
WATCHDOG_TIMEOUT = 5
# Global watchdogs
inc_temp_watchdog = None
dec_temp_watchdog = None
inc_timer_watchdog = None
dec_timer_watchdog = None

# Global event objects for control
inc_temp = None
dec_temp = None
inc_timer = None
dec_timer = None

class StandardScreen(Screen):
    timer_text = StringProperty(str(timer_hours_first) + str(timer_hours_second) + ':' + str(timer_minutes_first) + str(timer_minutes_second))
    temp_text = StringProperty(str(target_temp))

    def run(self):
        self.manager.transition = SlideTransition(direction='left')
        global apply
        apply = True
        self.manager.current = 'run_screen'
        self.manager.get_screen("run_screen").start_run()

    def graph_lookup(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'run_screen'

    def change_label_temp(self):
        self.temp_text = str(target_temp)

    def change_label_timer(self):
        self.timer_text = str(str(timer_hours_first) + str(timer_hours_second) + ':' + str(timer_minutes_first) + str(timer_minutes_second))

    def on_enter(self):
        Window.bind(on_touch_up=self.on_global_touch_up)

    def on_leave(self):
        Window.unbind(on_touch_up=self.on_global_touch_up)

    def on_touch_up(self, touch):
        # Local handling for touch-up within the screen
        self.stop_increase_temp()
        self.stop_decrease_temp()
        self.stop_increase_timer()
        self.stop_decrease_timer()
        return super().on_touch_up(touch)

    def on_global_touch_up(self, *args):
        # Global catch-all to make sure nothing keeps running
        self.stop_increase_temp()
        self.stop_decrease_temp()
        self.stop_increase_timer()
        self.stop_decrease_timer()

    def increase_temp(self):
        global target_temp
        target_temp += 1
        self.change_label_temp()

    def decrease_temp(self):
        global target_temp
        if target_temp > 5:
            target_temp -= 1
            self.change_label_temp()

    def increase_timer(self):
        global target_timer
        global timer_minutes_second
        global timer_minutes_first
        global timer_hours_second
        global timer_hours_first
        target_timer += 1
        timer_minutes_second += 1
        if timer_minutes_second == 10:
            timer_minutes_first += 1
            timer_minutes_second = 0
            if timer_minutes_first == 6:
                timer_hours_second += 1
                timer_minutes_first = 0
                if timer_hours_second == 10:
                    timer_hours_first += 1
                    timer_hours_second = 0
        self.change_label_timer()

    def decrease_timer(self):
        global target_timer
        global timer_minutes_second
        global timer_minutes_first
        global timer_hours_second
        global timer_hours_first
        if target_timer > 0:
            target_timer -= 1
            timer_minutes_second -= 1
            if timer_minutes_second < 0:
                timer_minutes_second = 9
                timer_minutes_first -= 1
                if timer_minutes_first < 0:
                    timer_minutes_first = 5
                    timer_hours_second -= 1
                    if timer_hours_second < 0:
                        timer_hours_second = 9
                        timer_hours_first -= 1
                        if timer_hours_first < 0:
                            # Prevent negative time values
                            timer_hours_first = 0
                            timer_hours_second = 0
                            timer_minutes_first = 0
                            timer_minutes_second = 0
                            target_timer = 0
        self.change_label_timer()

    # Temperature
    def start_increase_temp(self):
        global inc_temp, inc_temp_watchdog
        self.stop_increase_temp()  # Prevent duplicate schedules
        inc_temp = Clock.schedule_interval(lambda dt: self.increase_temp(), 0.1)
        inc_temp_watchdog = Clock.schedule_once(lambda dt: self.stop_increase_temp(), WATCHDOG_TIMEOUT)

    def stop_increase_temp(self):
        global inc_temp, inc_temp_watchdog
        if inc_temp:
            Clock.unschedule(inc_temp)
            inc_temp = None
        if inc_temp_watchdog:
            Clock.unschedule(inc_temp_watchdog)
            inc_temp_watchdog = None

    def start_decrease_temp(self):
        global dec_temp, dec_temp_watchdog
        self.stop_decrease_temp()
        dec_temp = Clock.schedule_interval(lambda dt: self.decrease_temp(), 0.1)
        dec_temp_watchdog = Clock.schedule_once(lambda dt: self.stop_decrease_temp(), WATCHDOG_TIMEOUT)

    def stop_decrease_temp(self):
        global dec_temp, dec_temp_watchdog
        if dec_temp:
            Clock.unschedule(dec_temp)
            dec_temp = None
        if dec_temp_watchdog:
            Clock.unschedule(dec_temp_watchdog)
            dec_temp_watchdog = None

    # Timer
    def start_increase_timer(self):
        global inc_timer, inc_timer_watchdog
        self.stop_increase_timer()
        inc_timer = Clock.schedule_interval(lambda dt: self.increase_timer(), 0.1)
        inc_timer_watchdog = Clock.schedule_once(lambda dt: self.stop_increase_timer(), WATCHDOG_TIMEOUT)

    def stop_increase_timer(self):
        global inc_timer, inc_timer_watchdog
        if inc_timer:
            Clock.unschedule(inc_timer)
            inc_timer = None
        if inc_timer_watchdog:
            Clock.unschedule(inc_timer_watchdog)
            inc_timer_watchdog = None

    def start_decrease_timer(self):
        global dec_timer, dec_timer_watchdog
        self.stop_decrease_timer()
        dec_timer = Clock.schedule_interval(lambda dt: self.decrease_timer(), 0.1)
        dec_timer_watchdog = Clock.schedule_once(lambda dt: self.stop_decrease_timer(), WATCHDOG_TIMEOUT)

    def stop_decrease_timer(self):
        global dec_timer, dec_timer_watchdog
        if dec_timer:
            Clock.unschedule(dec_timer)
            dec_timer = None
        if dec_timer_watchdog:
            Clock.unschedule(dec_timer_watchdog)
            dec_timer_watchdog = None

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'second'
