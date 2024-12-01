from pico2d import *
import gfw
import time  # 'time' 모듈 임포트 추가
from timer import Timer  # 타이머 클래스 임포트

class LevelBar:
    def __init__(self, bg_image_path, fg_image_path,max_exp, position):
        self.progress = 0
        self.max_exp = max_exp  # 레벨업에 필요한 최대 경험치
        self.bg_image = gfw.image.load(bg_image_path)
        self.fg_image = gfw.image.load(fg_image_path)
        self.position = position
        self.is_active = True  # 항상 활성화된 상태
        

    def update(self):
        pass

    def draw(self):
        
        x, y = self.position
        # 배경 이미지 그리기
        self.bg_image.draw(x, y)
        # 전경 이미지 그리기 (진행률에 따라 너비 조정)
        fg_width = self.fg_image.w * self.progress
        if fg_width > 0:
            self.fg_image.clip_draw(0, 0, int(fg_width), self.fg_image.h, x - (self.bg_image.w // 2) + (fg_width / 2), y)


    def add_exp(self, exp):
        self.progress += exp / self.max_exp
        if self.progress >= 1.0:
            self.progress = 1.0  # 최대치로 제한
            return True  # 레벨 업 발생
        return False
    
    def reset_for_level_up(self):
        self.progress = 0  # 게이지 초기화
        self.max_exp = int(self.max_exp * 1.5)  # 최대 경험치량 1.5배 증가
