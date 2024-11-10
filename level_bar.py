from pico2d import *
import gfw
import time  # 'time' 모듈 임포트 추가
from timer import Timer  # 타이머 클래스 임포트

class LevelBar:
    def __init__(self, bg_image_path, fg_image_path, max_time, position):
        self.progress = 0
        self.bg_image = gfw.image.load(bg_image_path)
        self.fg_image = gfw.image.load(fg_image_path)
        self.max_time = max_time
        self.position = position
        self.start_time = time.time()

    def update(self):
        # 경과 시간 계산
        self.elapsed_time = time.time() - self.start_time
        # 프로그레스 바 진행률 계산 (0 ~ 1 사이 값)
        self.progress = min(1.0, self.elapsed_time / self.max_time)

    def draw(self):
        
        x, y = self.position
        # 배경 이미지 그리기
        self.bg_image.draw(x, y)
        # 전경 이미지 그리기 (진행률에 따라 너비 조정)
        fg_width = self.fg_image.w * self.progress
        if fg_width > 0:
            self.fg_image.clip_draw(0, 0, int(fg_width), self.fg_image.h, x - (self.bg_image.w // 2) + (fg_width / 2), y)
