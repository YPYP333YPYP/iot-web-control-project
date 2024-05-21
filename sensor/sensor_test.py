import time
import asyncio
import threading
import random

class TestSonic:
    def __init__(self):
        self.is_running = False

    def get_distance(self):
        return random.randint(0, 100)

    async def emit_distance(self, sio, sid):
        while self.is_running:
            distance = self.get_distance()
            await sio.emit('distance_data', {'distance': distance}, callback=self.on_emit_success)
            print('Distance data sent:', distance)
            await asyncio.sleep(10)

    def on_emit_success(self):
        print('Emit successful!')

    async def start_sensors(self, sio, sid):
        self.is_running = True
        asyncio.create_task(self.emit_distance(sio, sid))  # Use create_task to ensure the task runs concurrently

    def stop_sensors(self):
        self.is_running = False

class TestDTH:
    def __init__(self, proper_tmp, proper_humid):
        self.proper_tmp = proper_tmp
        self.proper_humid = proper_humid
        self.relay_on = False
        self.is_running = False

    async def generate_data(self, sio, sid):
        while self.is_running:
            temperature = random.uniform(20, 40)
            humidity = random.uniform(30, 80)
            print(f'테스트 온도: {temperature:.1f}°C, 습도: {humidity:.1f}%')
            await sio.emit('sensor_data', {'temperature': temperature, 'humidity': humidity}, room=sid)

            if temperature >= self.proper_tmp or humidity >= self.proper_humid:
                print("Relay ON")
            else:
                print("Relay OFF")

            await asyncio.sleep(10)

    async def start_test(self, sio, sid):
        self.is_running = True
        asyncio.create_task(self.generate_data(sio, sid))

    def stop_test(self):
        self.is_running = False

    async def handle_relay_control(self, sio):
        @sio.on('relay_control')
        async def control(sid, data):
            if data['action'] == 'on':
                self.relay_on = True
                print("Relay ON (User)")
            elif data['action'] == 'off':
                self.relay_on = False
                print("Relay OFF (User)")