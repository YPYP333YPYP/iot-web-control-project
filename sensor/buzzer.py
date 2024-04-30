import RPi.GPIO as GPIO
import time

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# Buzzer 핀 설정
BUZZER_PIN = 17
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# PWM 인스턴스 생성 및 초기 주파수 설정
pwm = GPIO.PWM(BUZZER_PIN, 100)
pwm.start(0)

# 주요 음표의 주파수 (단위: Hz)
notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25  # 추가된 높은 도 음표
}

# 간단한 멜로디 (음표와 지속 시간)
melody = [('C4', 0.5), ('D4', 0.5), ('E4', 0.5), ('F4', 0.5),
          ('G4', 0.5), ('A4', 0.5), ('B4', 0.5), ('C5', 0.5)]  # 마지막 음을 높은 도로 변경

def play(note, duration):
    pwm.ChangeFrequency(notes[note])
    pwm.ChangeDutyCycle(50)  # 켜짐
    time.sleep(duration)  # 음표 지속 시간
    pwm.ChangeDutyCycle(0)  # 꺼짐

try:
    for note, duration in melody:
        play(note, duration)
        time.sleep(0.1)  # 음표 사이의 간격

finally:
    pwm.stop()
    GPIO.cleanup()