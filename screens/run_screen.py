import kivy
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.clock import Clock
import matplotlib.pyplot as plt
from screens import standard_screen as sts
from matplotlib.figure import Figure
#from kivy.garden.matplotlib import FigureCanvasKivyAgg

# Create a custom widget to embed the Matplotlib figur
import random

class RunScreen(Screen):


    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'standard_screen'
