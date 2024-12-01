from pico2d import *
import time

class Timer:
    def __init__(self, start_time, font):
        self.start_time = start_time
        self.font = font
        self.position = (530, 630)  # 화면 정중앙 좌표 (canvas_width / 2, canvas_height / 2)
        self.color = (255, 255, 255)  # 흰색
        self.is_active = True  # 항상 활성화 상태로 설정

    def update(self):
        if not self.is_active:
            return





    def draw(self):
        # 현재 경과 시간 계산
        
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f'Time: {minutes:02}:{seconds:02}'
        
        # 타이머 텍스트를 화면 정중앙에 그리기
        x, y = self.position
        self.font.draw(x, y, time_text, self.color)
