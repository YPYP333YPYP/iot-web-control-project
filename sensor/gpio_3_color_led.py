#gpio_3_color_led.py
import RPi.GPIO as GPIO
import time
import threading

# 핀 번호 설정
BLUE_PIN = 17
GREEN_PIN = 27
RED_PIN = 22

GPIO.setwarnings(False)

# GPIO 핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# LED 핀의 모드를 출력으로 설정
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

# 스레드 중지를 위한 플래그
is_rgb_3color_led = False
rgb_3color_led_thread = None

def cycle_rgb_3color_leds():
    global is_rgb_3color_led, rgb_3color_led_thread
   
    while is_rgb_3color_led:
        print("LEDs cycling...", is_rgb_3color_led, rgb_3color_led_thread)
        # 파란색 LED 켜기
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        # 초록색 LED 켜기
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        # 빨간색 LED 켜기
        GPIO.output(RED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(RED_PIN, GPIO.LOW)
    print("LEDs cycling stopped.")

async def start_rgb_3color_leds():
    global rgb_3color_led_thread, is_rgb_3color_led
    if rgb_3color_led_thread is None or not rgb_3color_led_thread.is_alive():
        is_rgb_3color_led = True
        rgb_3color_led_thread = threading.Thread(target=cycle_rgb_3color_leds)
        rgb_3color_led_thread.start()

async def stop_rgb_3color_leds():
    global rgb_3color_led_thread, is_rgb_3color_led
   
    print("led 스레드 종료", rgb_3color_led_thread)
    if rgb_3color_led_thread is not None:
        is_rgb_3color_led = False
        rgb_3color_led_thread.join(timeout=5)  # 5초 후에 강제 종료
        if rgb_3color_led_thread.is_alive():
            print("스레드가 제시간에 종료되지 않았습니다.")
        else:
            print("스레드가 성공적으로 종료되었습니다.")

async def rgb_3color_leds_state():
    global is_rgb_3color_led
    return is_rgb_3color_led