from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

target_temp = 0
target_timer = 0
timer_minutes_first =0
timer_minutes_second =0
timer_hours_first =0
timer_hours_second =0


class StandardScreen(Screen):
    timer_text=StringProperty(str(timer_hours_first)+str(timer_hours_second)+':'+ str(timer_minutes_first)+str(timer_minutes_second))
    temp_text=StringProperty(str(target_temp))

    def run(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'run_screen'

    def change_label_temp(self):
        self.temp_text = str(target_temp)
        print("from standard_screen")
        print(self.temp_text)

    def change_label_timer(self):
        self.timer_text = str(str(timer_hours_first)+str(timer_hours_second)+':'+ str(timer_minutes_first)+str(timer_minutes_second))
        print("from standard_screen")
        print(self.timer_text)

    def increase_temp(self):
        global target_temp
        target_temp += 1
        self.change_label_temp()

    def decrease_temp(self):
        global target_temp
        if target_temp >5:
            target_temp -= 1
            self.change_label_temp()

    def increase_timer(self):
        global target_timer
        global timer_minutes_second
        global timer_minutes_first
        global timer_hours_second
        global timer_hours_first
        target_timer += 1
        timer_minutes_second +=1
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
        self._inc_temp_ev = Clock.schedule_interval(lambda dt: self.increase_temp(), 0.1)

    def stop_increase_temp(self):
        Clock.unschedule(self._inc_temp_ev)

    def start_decrease_temp(self):
        self._dec_temp_ev = Clock.schedule_interval(lambda dt: self.decrease_temp(), 0.1)

    def stop_decrease_temp(self):
        Clock.unschedule(self._dec_temp_ev)

    # Timer
    def start_increase_timer(self):
        self._inc_timer_ev = Clock.schedule_interval(lambda dt: self.increase_timer(), 0.1)

    def stop_increase_timer(self):
        Clock.unschedule(self._inc_timer_ev)

    def start_decrease_timer(self):
        self._dec_timer_ev = Clock.schedule_interval(lambda dt: self.decrease_timer(), 0.1)

    def stop_decrease_timer(self):
        Clock.unschedule(self._dec_timer_ev)

    def go_back(self):
       self.manager.transition = SlideTransition(direction='right')
       self.manager.current = 'second'