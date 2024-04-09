import RPi.GPIO as GPIO
import time
# 핀 번호 설정
BUTTON_PIN = 18  # 버튼이 연결될 GPIO 핀 번호
BLUE_PIN = 17
GREEN_PIN = 27
RED_PIN = 22
# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
# 글로벌 변수
led_state = 0  # LED 상태 (0: 모두 꺼짐, 1: 파란색, 2: 초록색, 3: 빨간색)
# 모든 LED 끄는 함수
def turn_off_leds():
    global led_state
    led_state = 0
    GPIO.output(BLUE_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(RED_PIN, GPIO.LOW)
# 프로그램 시작 시 모든 LED 끄기
turn_off_leds()
# LED 상태 변경 함수
def change_led_state():
    global led_state
    led_state += 1
    if led_state > 3:
        led_state = 1
    if led_state == 1:
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif led_state == 2:
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif led_state == 3:
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)
# 버튼 이벤트 콜백 함수
def button_callback(channel):
    start_time = time.time()
    # 버튼이 눌린 상태 유지 확인
    while GPIO.input(BUTTON_PIN) == GPIO.LOW:
        time.sleep(0.01)  # 디바운싱 대기
    button_press_duration = time.time() - start_time
    if button_press_duration >= 1:  # 1초 이상 누르면 LED 끄기
        turn_off_leds()
    else:  # 짧게 누르면 LED 색상 변경 
        change_led_state()
# 버튼 이벤트 감지 설정
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()