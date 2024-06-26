from common import get_system_info, sio  # common.py에서 get_system_info 함수, sio 변수를 가져옵니다.
from sensor.gpio_3_color_led import start_rgb_3color_leds, stop_rgb_3color_leds, rgb_3color_leds_state
from sensor.ultra_sonic import UltrasonicSensor, item_data
from sensor.dth_relay import DTHControlSensor
import board
import asyncio

from sensor.sensor_test import TestSonic,TestDTH

# testsonic = TestSonic()
# test_dth = TestDTH(32, 70)

ultrasonic = UltrasonicSensor(23,24,17,27,22, "1")
dth_relay = DTHControlSensor(board.D18, 19, 30, 80)


@sio.event
async def connect(sid, environ):
    print("클라이언트 연결", sid)

    # test_dth = TestDTH(proper_tmp=30, proper_humid=60)
    # testsonic = TestSonic()

    # await test_dth.start_test(sio, sid)
    # await test_dth.handle_relay_control(sio)
    # await testsonic.start_sensors(sio, sid)
    tasks = [
        asyncio.create_task(ultrasonic.start_sensors(sio, sid)),
        asyncio.create_task(dth_relay.start_sensors(sio, sid))
    ]

    await asyncio.gather(*tasks)

@sio.event
async def disconnect(sid):
    print('클라이언트 종료', sid)
    ultrasonic.stop_sensors()
    dth_relay.stop_sensors()

    # test_dth.stop_test()
    # testsonic.stop_sensors()

@sio.on('get_system_info')
async def on_get_system_info(sid, data):
    #print("클라이언트에서 받은 data", data)
    systemInfo = get_system_info()
    await sio.emit('ret_system_info', systemInfo, room=sid)

