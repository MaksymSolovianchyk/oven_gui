import sys

if sys.platform.startswith('linux'):
    import RPi.GPIO as GPIO

    relay = 14

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay, GPIO.OUT)


    def heater_on():
        GPIO.output(relay, GPIO.HIGH)

    def heater_off():
        GPIO.output(relay, GPIO.LOW)

else:
    def heater_on():
        print("Heater on")
    def heater_off():
        print("Heater off")