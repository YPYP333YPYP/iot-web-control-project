from common import get_system_info, sio  # common.py에서 get_system_info 함수, sio 변수를 가져옵니다.
from sensor.gpio_3_color_led import start_rgb_3color_leds, stop_rgb_3color_leds, rgb_3color_leds_state


@sio.event
async def connect(sid, environ):
    print('클라이언트 연결', sid)

@sio.event
async def disconnect(sid):
    print('클라이언트 종료', sid)

@sio.on('get_system_info')
async def on_get_system_info(sid, data):
    #print("클라이언트에서 받은 data", data)
    systemInfo = get_system_info()
    await sio.emit('ret_system_info', systemInfo, room=sid)

@sio.on('set_3color_led')
async def on_set_3color_led(sid, data):
    print("set_3color_led", data)
    if data['data'] == 'on':
        await start_rgb_3color_leds()
    elif data['data'] == 'off':
        print("led 스위치 off", data)
        await stop_rgb_3color_leds()
    data['state'] = await rgb_3color_leds_state()
    await sio.emit('ret_3color_led', data, room=sid)

@sio.on('get_3color_led')
async def on_get_3color_led(sid, data):
    data['state'] = await rgb_3color_leds_state()
    await sio.emit('ret_3color_led', data, room=sid)