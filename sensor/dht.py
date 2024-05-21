import time
import board
import adafruit_dht
# DHT22 센서 설정 (GPIO 18)
dht_device = adafruit_dht.DHT22(board.D18)
while True:
    try:
        # 센서에서 온도와 습도 읽기
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        # 데이터 출력
        if humidity is not None and temperature is not None:
            print(f'온도: {temperature:.1f}°C')
            print(f'습도: {humidity:.1f}%')
        else:
            print('읽기 실패. 데이터가 없습니다.')
    except RuntimeError as error:
        # 센서에서 데이터를 읽는 중 오류 발생 처리
        print(error.args[0])
   
    except Exception as error:
        dht_device.exit()
        raise error
    # 10초 동안 대기
    time.sleep(10)