
# import RPi.GPIO as GPIO
import time
import threading
import asyncio
import random

item_data = {
    "1" : {
        "name" : "coca-cola-zero",
        "price" : "32,000",
        "before_unit" : "50"
    }
}

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, red_led_pin, yellow_led_pin, green_led_pin, number):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.red_led_pin = red_led_pin
        self.yellow_led_pin = yellow_led_pin
        self.green_led_pin = green_led_pin
        self.number = number

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.red_led_pin, GPIO.OUT)
        GPIO.setup(self.yellow_led_pin, GPIO.OUT)
        GPIO.setup(self.green_led_pin, GPIO.OUT)



    def get_distance(self):
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.5)
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return int(distance)

    def control_led(self, distance):
        GPIO.output(self.red_led_pin, GPIO.LOW)
        GPIO.output(self.yellow_led_pin, GPIO.LOW)
        GPIO.output(self.green_led_pin, GPIO.LOW)
        if distance < 100:
            GPIO.output(self.red_led_pin, GPIO.HIGH)
        elif distance < 200:
            GPIO.output(self.yellow_led_pin, GPIO.HIGH)
        else:
            GPIO.output(self.green_led_pin, GPIO.HIGH)

    def sensor_loop(self):
        while True:
            dist = self.get_distance()
            self.control_led(dist)
            time.sleep(10)

    async def emit_distance(self, sio, sid):
        while True:
            dist = self.get_distance()
            if dist != 1200:
                self.control_led(dist)
                await sio.emit('distance_data', {'distance': dist}, room=sid)
                print(dist)
                await asyncio.sleep(3)

    async def start_sensors(self, sio, sid):
        loop = asyncio.get_event_loop()
        loop.create_task(self.emit_distance(sio, sid))
        await sio.emit('item', {'item_info': item_data["1"]}, room=sid)

        t = threading.Thread(target=self.sensor_loop)

        t.start()

    def stop_sensors(self):
        for t in self.threads:
            t.join()
        GPIO.cleanup()


