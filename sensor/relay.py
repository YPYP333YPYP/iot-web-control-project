import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 모드 설정 (BCM)
GPIO.setmode(GPIO.BCM)

# 릴레이 센서가 연결된 GPIO 핀 번호 (BCM 모드)
relay_pin = 19

# 릴레이 센서 핀을 출력으로 설정
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        # 릴레이 켜기
        GPIO.output(relay_pin, GPIO.HIGH)
        print("Relay ON")
        time.sleep(5)  # 5초 대기

        # 릴레이 끄기
        GPIO.output(relay_pin, GPIO.LOW)
        print("Relay OFF")
        time.sleep(5)  # 5초 대기

except KeyboardInterrupt:
    # 프로그램 종료시 GPIO 핀 초기화
    GPIO.cleanup()