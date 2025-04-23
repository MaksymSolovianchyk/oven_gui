import sys

if sys.platform.startswith('linux'):
    import board
    import digitalio

    # Use BCM pin 14 (TXD) ? make sure it's not being used by serial!
    relay = digitalio.DigitalInOut(board.D14)
    relay.direction = digitalio.Direction.OUTPUT

    def heater_on():
        relay.value = False  # LOW

    def heater_off():
        relay.value = True  # High

else:
    def heater_on():
        print("Heater on")

    def heater_off():
        print("Heater off")
