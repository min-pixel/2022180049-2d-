from pico2d import *
import gfw

class Timer:
    def __init__(self, total_time, font, on_time_up_callback):
        self.total_time = total_time  # 제한 시간 (초)
        self.remaining_time = total_time  # 남은 시간
        self.font = font
        self.position = (530, 630)  # 화면 중앙 상단
        self.color = (255, 255, 255)  # 흰색
        self.is_active = True  # 타이머 활성화 여부
        self.on_time_up_callback = on_time_up_callback  # 시간 종료 시 호출될 콜백 함수

    def update(self):
        if not self.is_active:
            return
        self.remaining_time -= gfw.frame_time
        if self.remaining_time <= 0:  # 시간이 종료되었을 경우
            self.remaining_time = 0
            self.is_active = False
            self.on_time_up_callback()  # 콜백 호출

    def draw(self):
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        time_text = f'Time: {minutes:02}:{seconds:02}'
        x, y = self.position
        self.font.draw(x, y, time_text, self.color)

    def reset(self):
        """타이머를 재설정"""
        self.remaining_time = self.total_time
        self.is_active = True
