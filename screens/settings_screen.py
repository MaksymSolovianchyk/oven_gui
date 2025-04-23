from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import csv
from kivy.properties import StringProperty

from scripts import usb_copy

class SettingsScreen(Screen):
    Instructions=StringProperty("To add custom presets insert flash drive and press Add")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Instructions="To add custom presets insert flash drive and press Add"
    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'

    def file_detect_and_copy(self):
        usb_copy.copy_usb_file("/home/sw/guii/oven_gui-save_branch/presets")
    #/home/sw/guii/oven_gui-save_branch/presets