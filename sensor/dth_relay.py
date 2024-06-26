import adafruit_dht
import threading
import RPi.GPIO as GPIO
import time
import asyncio

class DTHControlSensor:
    def __init__(self, dht_pin, relay_pin, proper_tmp, proper_humid):
        self.dht_device = adafruit_dht.DHT22(dht_pin)
        GPIO.setmode(GPIO.BCM)
        self.relay_pin = relay_pin
        GPIO.setup(self.relay_pin, GPIO.OUT)
        self.proper_tmp = proper_tmp
        self.proper_humid = proper_humid
        self.running = False
    async def read_dht_sensor(self, sio, sid):
        while self.running:
            try:
                temperature = self.dht_device.temperature
                humidity = self.dht_device.humidity
                if humidity is not None and temperature is not None:
                    print(f'온도: {temperature:.1f}°C, 습도: {humidity:.1f}%')
                    await sio.emit('sensor_data', {'temperature': temperature, 'humidity': humidity}, room=sid)
                    self.check_threshold(temperature, humidity)
                else:
                    print('읽기 실패. 데이터가 없습니다.')
            except RuntimeError as error:
                print(error.args[0])
            except Exception as error:
                self.dht_device.exit()
                raise error
            await asyncio.sleep(3)

    def check_threshold(self, temperature, humidity):
        if temperature >= self.proper_tmp or humidity >= self.proper_humid:
            GPIO.output(self.relay_pin, GPIO.HIGH)
            print("Relay ON")
        else:
            GPIO.output(self.relay_pin, GPIO.LOW)
            print("Relay OFF")

    def control_relay(self, sio, sid):
        @sio.on('relay_control')
        def handle_relay_control(sid, data):
            if data['action'] == 'on':
                GPIO.output(self.relay_pin, GPIO.HIGH)
                print("Relay ON")
            elif data['action'] == 'off':
                GPIO.output(self.relay_pin, GPIO.LOW)
                print("Relay OFF")

    async def start_sensors(self, sio, sid):
        self.running = True
        sensor_task = asyncio.create_task(self.read_dht_sensor(sio, sid))
        self.control_relay(sio, sid)

    def stop_sensors(self):
        self.running = False
        GPIO.cleanup()
