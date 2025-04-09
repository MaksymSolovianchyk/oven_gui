from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
class RoundedButton(ButtonBehavior, Label):
    logo = StringProperty()
    pass

class RoundedSmallButton(ButtonBehavior, Label):
    logo = StringProperty()
    pass