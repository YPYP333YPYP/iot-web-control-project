import RPi.GPIO as GPIO
import time
# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
# 핀 번호 할당
TRIG = 23
ECHO = 24
LED = 17
# 입출력 설정
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
# PWM 설정
pwm = GPIO.PWM(LED, 100)  # 100Hz
pwm.start(0)  # 초기 듀티 사이클 0
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.5)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
try:
    while True:
        dist = get_distance()
        print("Distance:", dist, "cm")
       
        if dist > 100 :
            dist = 99
        pwm.ChangeDutyCycle(dist)
        time.sleep(0.1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()