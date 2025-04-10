from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
class RoundedButton(ButtonBehavior, Label):
    logo = StringProperty()
    pass

class RoundedSmallButton(ButtonBehavior, Label):
    logo = StringProperty()
<<<<<<< HEAD

=======
    pass
class BigButton(ButtonBehavior, Label):
    logo = StringProperty()
>>>>>>> c2d7a2e8bba2c3763d428c72c18ea88564ddfac5
    pass